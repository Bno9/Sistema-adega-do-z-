class Estoque:
    """Classe que armazena os produtos cadastrados e suas informações"""

    def __init__(self):
        self.itens = {}

    def criar_produto(self, *args):
        from Utils.Produto import Produto

        obj_produto = Produto(*args) #Cria o objeto produto usando a classe Produto

        if self.conferir_se_existe_no_estoque(obj_produto.codigo):
            return "Um item já está cadastrado com esse código"
                 
        self.itens[obj_produto.codigo] = obj_produto #Salva no dicionario a chave (código) e o valor (objeto)
        
        return f"item {obj_produto.nome} criado"
      
    def remover_produto(self, codigo_produto):
        if codigo_produto in self.itens:
            del self.itens[codigo_produto]
            return "Produto removido com sucesso"

        return "Produto não encontrado"

    def dar_baixa(self, item, quantidade_baixa):
        self.itens[item.codigo].quantidade -= quantidade_baixa

    def conferir_se_existe_no_estoque(self, codigo_produto):
        for codigo, dados in self.itens.items():
            if codigo_produto == codigo:
                return True

        return False