# QUADROS - REIS | Loja Online de Roupas

## Estrutura do projeto

```
quadros_reis/
├── app.py                    # Flask — rotas e lógica
├── quadros_reis_models.py    # Classes Python
├── requirements.txt
├── templates/
│   ├── base.html             # Layout base
│   ├── index.html            # Página inicial + grid de produtos
│   ├── produto.html          # Detalhe do produto
│   ├── carrinho.html         # Carrinho de compras
│   ├── checkout.html         # Finalizar compra
│   ├── pedido_ok.html        # Confirmação de pedido
│   ├── cadastro.html         # Cadastro de cliente
│   ├── login.html            # Login
│   └── minha_conta.html      # Histórico e dados do cliente
└── static/
    └── css/
        └── style.css         # CSS completo
```

## Como rodar

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o servidor:
```bash
python app.py
```

3. Acesse no navegador:
```
http://localhost:5000
```

## Fluxo de uso

1. Acesse a home → veja os produtos do drop atual
2. Clique em um produto → veja detalhes e adicione ao carrinho
3. Vá ao carrinho → revise os itens
4. Clique em "Finalizar compra" → será redirecionado para cadastro/login se necessário
5. No checkout → escolha a forma de pagamento e confirme
6. Pedido confirmado → veja o histórico em "Minha Conta"

