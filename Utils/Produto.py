class Produto:
    """Classe molde para criar produtos"""

    def __init__(self, codigo, nome, preco_custo, preco_venda, quantidade):
        self.codigo = codigo
        self.nome = nome
        self.preco_custo = preco_custo
        self.preco_venda = preco_venda
        self.quantidade = quantidade
        

    def __str__(self):
        """Formatação base do objeto"""
        return f"Código: {self.codigo} - Produto: {self.nome} | Preço: R${self.preco_venda} | Quantidade no estoque: {self.quantidade}"