from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from quadros_reis_models import Cliente, Roupa, CarrinhoDeCompras, Pagamento, Pedido
import json

app = Flask(__name__)
app.secret_key = "quadros_reis_secret_2025"

# ── Banco de dados em memória ──────────────────────────
clientes: list[Cliente]     = []
produtos: list[Roupa]       = []

# Dados de demonstração
produtos.append(Roupa("Camiseta Drop Noise", 89.90, 12,
    "Oversized 100% algodão fio 30.1", "M", "Off-White", "Camiseta"))
produtos.append(Roupa("Moletom Heavy Arch", 259.90, 6,
    "Fleece 380g com capuz estruturado", "G", "Preto", "Moletom"))
produtos.append(Roupa("Calça Cargo Utility", 219.90, 8,
    "Ripstop com bolsos laterais", "G", "Verde Militar", "Calça"))
produtos.append(Roupa("Camiseta Washed Logo", 99.90, 15,
    "Lavagem especial vintage", "P", "Cinza Chumbo", "Camiseta"))
produtos.append(Roupa("Jaqueta Coach QR", 349.90, 4,
    "Nylon impermeável, forro mesh", "M", "Preto", "Jaqueta"))
produtos.append(Roupa("Calça Jeans", 149.90, 10,
    "Elástico + cordão, bolso lateral", "M", "Bege", "Shorts"))


# ── Helpers ───────────────────────────────────────────
def get_carrinho_session():
    """Retorna {id_produto: quantidade} da sessão."""
    return session.get("carrinho", {})

def save_carrinho(carrinho_dict):
    session["carrinho"] = carrinho_dict
    session.modified = True

def get_produto_by_id(pid: int):
    return next((p for p in produtos if p.get_id() == pid), None)

def get_cliente_logado():
    cpf = session.get("cliente_cpf")
    if not cpf:
        return None
    return next((c for c in clientes if c.get_cpf() == cpf), None)

def carrinho_para_display():
    """Retorna lista de dicts para renderização."""
    cart = get_carrinho_session()
    items = []
    total = 0.0
    for id_str, qtd in cart.items():
        prod = get_produto_by_id(int(id_str))
        if prod:
            subtotal = prod.get_preco() * qtd
            total += subtotal
            items.append({
                "produto": prod,
                "quantidade": qtd,
                "subtotal": subtotal
            })
    return items, total


# ── Rotas ─────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html",
                           produtos=produtos,
                           cliente=get_cliente_logado(),
                           qtd_carrinho=sum(get_carrinho_session().values()))

@app.route("/produto/<int:pid>")
def produto_detalhe(pid):
    prod = get_produto_by_id(pid)
    if not prod:
        flash("Produto não encontrado.", "error")
        return redirect(url_for("index"))
    return render_template("produto.html",
                           produto=prod,
                           cliente=get_cliente_logado(),
                           qtd_carrinho=sum(get_carrinho_session().values()))

@app.route("/carrinho")
def carrinho():
    items, total = carrinho_para_display()
    return render_template("carrinho.html",
                           items=items,
                           total=total,
                           cliente=get_cliente_logado(),
                           qtd_carrinho=sum(get_carrinho_session().values()))

@app.route("/carrinho/add/<int:pid>", methods=["POST"])
def add_carrinho(pid):
    prod = get_produto_by_id(pid)
    if not prod:
        flash("Produto não encontrado.", "error")
        return redirect(url_for("index"))
    qtd = int(request.form.get("quantidade", 1))
    cart = get_carrinho_session()
    atual = cart.get(str(pid), 0)
    if atual + qtd > prod.get_estoque():
        flash(f"Estoque insuficiente para '{prod.get_nome()}'.", "error")
    else:
        cart[str(pid)] = atual + qtd
        save_carrinho(cart)
        flash(f"'{prod.get_nome()}' adicionado ao carrinho!", "success")
    return redirect(request.referrer or url_for("index"))

@app.route("/carrinho/remove/<int:pid>")
def remove_carrinho(pid):
    cart = get_carrinho_session()
    cart.pop(str(pid), None)
    save_carrinho(cart)
    return redirect(url_for("carrinho"))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cliente = get_cliente_logado()
    if not cliente:
        flash("Faça login ou cadastre-se para finalizar a compra.", "info")
        return redirect(url_for("cadastro"))

    items, total = carrinho_para_display()
    if not items:
        flash("Seu carrinho está vazio.", "error")
        return redirect(url_for("carrinho"))

    if request.method == "POST":
        forma = request.form.get("forma_pagamento", "pix")

        # Monta carrinho de objeto
        carrinho_obj = CarrinhoDeCompras(cliente)
        for item in items:
            carrinho_obj.adicionar_item(item["produto"], item["quantidade"])

        pagamento = Pagamento(total, forma)
        pedido = Pedido(cliente, carrinho_obj, pagamento)

        if pedido.finalizar():
            save_carrinho({})
            flash(f"Pedido #{pedido.get_numero():04d} confirmado! Obrigado ♛", "success")
            return redirect(url_for("pedido_confirmado", numero=pedido.get_numero()))
        else:
            flash("Pagamento recusado. Tente outra forma.", "error")

    return render_template("checkout.html",
                           cliente=cliente,
                           items=items,
                           total=total,
                           qtd_carrinho=sum(get_carrinho_session().values()))

@app.route("/pedido/<int:numero>")
def pedido_confirmado(numero):
    cliente = get_cliente_logado()
    if not cliente:
        return redirect(url_for("index"))
    pedido = next((p for p in cliente.get_historico()
                   if p.get_numero() == numero), None)
    return render_template("pedido_ok.html",
                           pedido=pedido,
                           cliente=cliente,
                           qtd_carrinho=0)

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome     = request.form["nome"].strip()
        cpf      = request.form["cpf"].strip()
        email    = request.form["email"].strip()
        telefone = request.form["telefone"].strip()
        endereco = request.form["endereco"].strip()

        if any(c.get_cpf() == cpf for c in clientes):
            flash("CPF já cadastrado.", "error")
        else:
            c = Cliente(nome, cpf, email, telefone, endereco)
            clientes.append(c)
            session["cliente_cpf"] = cpf
            flash(f"Bem-vindo(a), {nome}! ♛", "success")
            return redirect(url_for("index"))

    return render_template("cadastro.html",
                           cliente=get_cliente_logado(),
                           qtd_carrinho=sum(get_carrinho_session().values()))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        cpf = request.form["cpf"].strip()
        c = next((c for c in clientes if c.get_cpf() == cpf), None)
        if c:
            session["cliente_cpf"] = cpf
            flash(f"Bem-vindo de volta, {c.get_nome()}!", "success")
            return redirect(url_for("index"))
        flash("CPF não encontrado. Cadastre-se primeiro.", "error")
    return render_template("login.html",
                           cliente=get_cliente_logado(),
                           qtd_carrinho=sum(get_carrinho_session().values()))

@app.route("/logout")
def logout():
    session.pop("cliente_cpf", None)
    flash("Até logo! ♛", "info")
    return redirect(url_for("index"))

@app.route("/minha-conta")
def minha_conta():
    cliente = get_cliente_logado()
    if not cliente:
        return redirect(url_for("login"))
    return render_template("minha_conta.html",
                           cliente=cliente,
                           pedidos=cliente.get_historico(),
                           qtd_carrinho=sum(get_carrinho_session().values()))


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)