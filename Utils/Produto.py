class Produto:
    """Classe molde para criar produtos"""
    
    def __init__(self, **dados: dict):
        self.codigo = dados["codigo"]
        self.nome = dados["nome"]
        self.tipo = dados["tipo"]
        self.preco_custo = dados["preco_custo"]
        self.preco_venda = dados["preco_venda"]
        self.quantidade = dados["quantidade"]
        self.id_produto_pai = dados.get("id_produto_pai")
        self.qtd_fardo = dados.get("quantidade_fardo")


    def __str__(self):
        """Formatação base do objeto"""
        return f"Código: {self.codigo} - Produto: {self.nome} | Preço: R${self.preco_venda} | Quantidade no estoque: {self.quantidade}"