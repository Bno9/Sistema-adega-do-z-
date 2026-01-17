class Produto:
    """Classe molde para criar produtos"""

    def __init__(self, codigo, nome, tipo, preco_custo, preco_venda, quantidade, id_produto_pai=None, qtf_fardo=None,):
        self.codigo = codigo
        self.nome = nome
        self.tipo = tipo
        self.preco_custo = preco_custo
        self.preco_venda = preco_venda
        self.quantidade = quantidade

        self.id_produto_pai = id_produto_pai
        self.qtd_fardo = qtf_fardo

    def __str__(self):
        """Formatação base do objeto"""
        return f"Código: {self.codigo} - Produto: {self.nome} | Preço: R${self.preco_venda} | Quantidade no estoque: {self.quantidade}"