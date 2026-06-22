"""
============================================================
  QUADROS - REIS | Sistema de Loja Online de Roupas
============================================================
  Classes:
    - Pessoa (base)
      - Cliente (herda Pessoa)
    - Produto (base)
      - Roupa (herda Produto)
    - Pedido
    - CarrinhoDeCompras
    - Pagamento
============================================================
"""

from datetime import datetime
from typing import Optional


# ─────────────────────────────────────────────
# CLASSE BASE: Pessoa
# ─────────────────────────────────────────────
class Pessoa:
    """Classe base para Cliente e Funcionario."""

    def __init__(self, nome: str, cpf: str, email: str, telefone: str):
        self._nome: str = nome
        self._cpf: str = cpf
        self._email: str = email
        self._telefone: str = telefone

    def get_nome(self) -> str:
        return self._nome

    def get_cpf(self) -> str:
        return self._cpf

    def get_email(self) -> str:
        return self._email

    def get_telefone(self) -> str:
        return self._telefone

    def set_email(self, email: str) -> None:
        self._email = email

    def set_telefone(self, telefone: str) -> None:
        self._telefone = telefone

    def apresentar(self) -> str:
        return f"Pessoa: {self._nome} | CPF: {self._cpf}"

    def __str__(self) -> str:
        return self.apresentar()


# ─────────────────────────────────────────────
# SUBCLASSE: Cliente (herda Pessoa)
# ─────────────────────────────────────────────
class Cliente(Pessoa):

    def __init__(self, nome: str, cpf: str, email: str,
                 telefone: str, endereco: str):
        super().__init__(nome, cpf, email, telefone)
        self._endereco: str = endereco
        self._historico_pedidos: list["Pedido"] = []

    def get_endereco(self) -> str:
        return self._endereco

    def set_endereco(self, endereco: str) -> None:
        self._endereco = endereco

    def adicionar_pedido(self, pedido: "Pedido") -> None:
        self._historico_pedidos.append(pedido)

    def get_historico(self) -> list:
        return self._historico_pedidos

    # Polimorfismo: sobrescreve Pessoa.apresentar()
    def apresentar(self) -> str:
        return (f"[CLIENTE] {self._nome} | CPF: {self._cpf} "
                f"| Email: {self._email} | Endereço: {self._endereco}")

    def __str__(self) -> str:
        return self.apresentar()


# ─────────────────────────────────────────────
# CLASSE BASE: Produto
# ─────────────────────────────────────────────
class Produto:

    _contador_id: int = 0

    def __init__(self, nome: str, preco: float, estoque: int,
                 descricao: str):
        Produto._contador_id += 1
        self._id: int = Produto._contador_id
        self._nome: str = nome
        self._preco: float = preco
        self._estoque: int = estoque
        self._descricao: str = descricao

    def get_id(self) -> int:
        return self._id

    def get_nome(self) -> str:
        return self._nome

    def get_preco(self) -> float:
        return self._preco

    def get_estoque(self) -> int:
        return self._estoque

    def get_descricao(self) -> str:
        return self._descricao

    def set_preco(self, preco: float) -> None:
        self._preco = preco

    def reduzir_estoque(self, quantidade: int) -> bool:
        if quantidade <= self._estoque:
            self._estoque -= quantidade
            return True
        return False

    def repor_estoque(self, quantidade: int) -> None:
        self._estoque += quantidade

    def exibir_detalhes(self) -> str:
        return (f"[ID:{self._id}] {self._nome} | "
                f"R$ {self._preco:.2f} | Estoque: {self._estoque}")

    def __str__(self) -> str:
        return self.exibir_detalhes()


# ─────────────────────────────────────────────
# SUBCLASSE: Roupa (herda Produto)
# ─────────────────────────────────────────────
class Roupa(Produto):

    TAMANHOS_VALIDOS = ["PP", "P", "M", "G", "GG", "XGG"]

    def __init__(self, nome: str, preco: float, estoque: int,
                 descricao: str, tamanho: str, cor: str, categoria: str):
        super().__init__(nome, preco, estoque, descricao)
        self._tamanho: str = tamanho.upper()
        self._cor: str = cor
        self._categoria: str = categoria  # Ex: camiseta, calça, vestido...

    def get_tamanho(self) -> str:
        return self._tamanho

    def get_cor(self) -> str:
        return self._cor

    def get_categoria(self) -> str:
        return self._categoria

    def exibir_detalhes(self) -> str:
        return (f"[ID:{self._id}] {self._nome} ({self._categoria}) | "
                f"Cor: {self._cor} | Tam: {self._tamanho} | "
                f"R$ {self._preco:.2f} | Estoque: {self._estoque}")

    def __str__(self) -> str:
        return self.exibir_detalhes()


# ─────────────────────────────────────────────
# CLASSE: CarrinhoDeCompras
# ─────────────────────────────────────────────
class CarrinhoDeCompras:

    def __init__(self, cliente: Cliente):
        self._cliente: Cliente = cliente
        self._itens: dict[Roupa, int] = {}  # produto -> quantidade

    def adicionar_item(self, roupa: Roupa, quantidade: int) -> bool:
        if roupa.get_estoque() >= quantidade:
            if roupa in self._itens:
                self._itens[roupa] += quantidade
            else:
                self._itens[roupa] = quantidade
            return True
        print(f"  ⚠ Estoque insuficiente para '{roupa.get_nome()}'.")
        return False

    def remover_item(self, roupa: Roupa) -> bool:
        if roupa in self._itens:
            del self._itens[roupa]
            return True
        return False

    def calcular_total(self) -> float:
        return sum(r.get_preco() * q for r, q in self._itens.items())

    def get_itens(self) -> dict:
        return self._itens

    def limpar(self) -> None:
        self._itens.clear()

    def exibir_carrinho(self) -> None:
        if not self._itens:
            print("  Carrinho vazio.")
            return
        print(f"\n  {'─'*50}")
        print(f"  🛒 Carrinho de {self._cliente.get_nome()}")
        print(f"  {'─'*50}")
        for roupa, qtd in self._itens.items():
            subtotal = roupa.get_preco() * qtd
            print(f"  • {roupa.get_nome()} (x{qtd}) "
                  f"= R$ {subtotal:.2f}")
        print(f"  {'─'*50}")
        print(f"  TOTAL: R$ {self.calcular_total():.2f}")
        print(f"  {'─'*50}")

    def __str__(self) -> str:
        return (f"Carrinho de {self._cliente.get_nome()} | "
                f"Itens: {len(self._itens)} | "
                f"Total: R$ {self.calcular_total():.2f}")


# ─────────────────────────────────────────────
# CLASSE: Pagamento
# ─────────────────────────────────────────────
class Pagamento:

    FORMAS_VALIDAS = ["pix", "cartao_credito", "cartao_debito", "boleto"]

    def __init__(self, valor: float, forma: str):
        self._valor: float = valor
        self._forma: str = forma.lower()
        self._status: str = "pendente"
        self._data: Optional[str] = None

    def get_valor(self) -> float:
        return self._valor

    def get_forma(self) -> str:
        return self._forma

    def get_status(self) -> str:
        return self._status

    def processar(self) -> bool:
        if self._forma in self.FORMAS_VALIDAS:
            self._status = "aprovado"
            self._data = datetime.now().strftime("%d/%m/%Y %H:%M")
            return True
        self._status = "recusado"
        return False

    def exibir_comprovante(self) -> str:
        return (f"  Pagamento: R$ {self._valor:.2f} | "
                f"Forma: {self._forma.upper()} | "
                f"Status: {self._status.upper()} | "
                f"Data: {self._data or 'não processado'}")

    def __str__(self) -> str:
        return self.exibir_comprovante()


# ─────────────────────────────────────────────
# CLASSE: Pedido
# ─────────────────────────────────────────────
class Pedido:

    _contador_pedido: int = 0

    def __init__(self, cliente: Cliente, carrinho: CarrinhoDeCompras,
                 pagamento: Pagamento):
        Pedido._contador_pedido += 1
        self._numero: int = Pedido._contador_pedido
        self._cliente: Cliente = cliente
        self._itens: dict = dict(carrinho.get_itens())
        self._total: float = carrinho.calcular_total()
        self._pagamento: Pagamento = pagamento
        self._status: str = "aguardando_pagamento"
        self._data: str = datetime.now().strftime("%d/%m/%Y %H:%M")

    def get_numero(self) -> int:
        return self._numero

    def get_total(self) -> float:
        return self._total

    def get_status(self) -> str:
        return self._status

    def finalizar(self) -> bool:
        if self._pagamento.processar():
            self._status = "confirmado"
            # Baixa no estoque
            for roupa, qtd in self._itens.items():
                roupa.reduzir_estoque(qtd)
            self._cliente.adicionar_pedido(self)
            return True
        self._status = "pagamento_recusado"
        return False

    def exibir_pedido(self) -> None:
        print(f"\n  {'═'*50}")
        print(f"  📦 PEDIDO #{self._numero:04d} | {self._data}")
        print(f"  Cliente: {self._cliente.get_nome()}")
        print(f"  {'─'*50}")
        for roupa, qtd in self._itens.items():
            subtotal = roupa.get_preco() * qtd
            print(f"  • {roupa.get_nome()} x{qtd} "
                  f"→ R$ {subtotal:.2f}")
        print(f"  {'─'*50}")
        print(f"  TOTAL: R$ {self._total:.2f}")
        print(self._pagamento.exibir_comprovante())
        print(f"  Status: {self._status.upper()}")
        print(f"  {'═'*50}")

    def __str__(self) -> str:
        return (f"Pedido #{self._numero:04d} | "
                f"Cliente: {self._cliente.get_nome()} | "
                f"Total: R$ {self._total:.2f} | "
                f"Status: {self._status}")


