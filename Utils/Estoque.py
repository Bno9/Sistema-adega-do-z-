class Estoque:

    def __init__(self):
        self.itens = {}

    def adicionar_produto(self, produto):
        self.itens[produto.codigo] = produto

    def remover_produto(self, codigo_produto):
        if codigo_produto in self.itens:
            del self.itens[codigo_produto]
        else:
            print("Produto não encontrado")

    def listar_itens(self):
        if not self.itens:
            print("Estoque vazio. Cadastre algum item")
            return
            
        for item, valor in self.itens.items():
            print(valor)
    