from Utils.Estoque import Estoque

class Produto:

    def __init__(self, codigo, nome, preco_custo, preco_venda, quantidade):
        self.codigo = codigo
        self.nome = nome
        self.preco_custo = preco_custo
        self.preco_venda = preco_venda
        self.quantidade = quantidade
        

    def __str__(self):
        return f"Código: {self.codigo} - Produto: {self.nome} | Preço: R${self.preco_venda} | Quantidade no estoque: {self.quantidade}"

    def editar_produto(self, atributo: str, novo_valor):
        #atributo vai ser o que ele deseja mudar, por exemplo: nome, código ou valor
        #quando for implementar interface, vou fazer botões que enviam automaticamente qual atributo vai ser, para que ele nao precise digitar

        setattr(self, atributo, novo_valor)


