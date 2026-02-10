class Produto:
    """Classe molde para criar produtos"""
    
    def __init__(self, **dados: dict):
        self.codigo = dados.get("codigo", None)
        self.nome = dados.get("nome", None)
        self.tipo = dados.get("tipo", None)
        self.preco_custo = dados.get("preco_custo", None)
        self.preco_venda = dados.get("preco_venda", None)
        self.quantidade = dados.get("quantidade", None)
        self.id_produto_pai = dados.get("id_produto_pai", None)
        self.qtd_fardo = dados.get("quantidade_fardo", None)


    def __str__(self):
        """Formatação base do objeto"""
        return f"Código: {self.codigo} - Produto: {self.nome} | Preço: R${self.preco_venda} | Quantidade no estoque: {self.quantidade}"