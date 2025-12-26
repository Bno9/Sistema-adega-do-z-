class Estoque:

    def __init__(self):
        self.itens = {}

    def criar_produto(self, *args):
        from Utils.Produto import Produto
        obj_produto = Produto(*args)

        if self.conferir_se_existe(obj_produto.codigo):
            return{"sucesso": "Um item já está cadastrado com esse código"}
                 
        self.itens[obj_produto.codigo] = obj_produto
        return {"sucesso": f"item {obj_produto.nome} criado"}
      
    def remover_produto(self, codigo_produto):
        if codigo_produto in self.itens:
            del self.itens[codigo_produto]
            return "Produto removido com sucesso"
        else:
            return "Produto não encontrado"

    def conferir_se_existe(self, chave):
        for codigo, dados in self.itens.items():
            if chave == codigo:
                return True

        return False