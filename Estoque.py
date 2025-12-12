from Produto import Produto

class Estoque:

    def __init__(self):
        self.estoque = {}

    def adicionar_produto(self, produto: Produto, quantidade: int):
        self.estoque[produto.codigo] = {"nome": produto.nome,
                                        "preço de custo": produto.preco_custo,
                                        "preço de venda": produto.preco_venda,
                                        "quantidade": quantidade}

    def alterar_quantidade(self, produto: Produto, quantidade: int):
        self.estoque[produto.codigo][quantidade] = quantidade

    def remover_produto(self, produto: Produto):
        del self.estoque[produto.codigo]

    