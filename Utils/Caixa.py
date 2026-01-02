class Caixa:
    
    def __init__(self, estoque):
        self.estoque = estoque
        self.vendas = []
        self.itens_no_carrinho = []

    def carrinho_caixa(self, produto, quantidade=1):
        """Método que adiciona os produtos a tela de soma do caixa"""

        for i, (item, quantidade_atual) in enumerate(self.itens_no_carrinho):
            if produto.codigo == item.codigo:
                self.itens_no_carrinho[i] = (item, quantidade_atual + quantidade)
                return

        self.itens_no_carrinho.append((produto, quantidade))

    def finalizar_compra(self, valor_pago):
        """Método que finaliza a compra e da baixa no estoque"""
        
        if not self.itens_no_carrinho:
            return {
                "sucesso": False,
                "mensagem": "Nenhum item registrado"
            }

        total = self.total()

        try:
            valor_pago = float(valor_pago)
        except ValueError:
            return{
                "sucesso": False,
                "mensagem": "Erro de processamento"
            }

        if valor_pago < total:
            return{
                "sucesso": False,
                "mensagem": "Valor recebido menor que total"
            }

        troco = valor_pago - total
        
        for item, quantidade in self.itens_no_carrinho:
            self.estoque.dar_baixa(item, quantidade)

        self.vendas.append({
            "itens": [{"codigo": p.codigo, "nome": p.nome, "quantidade": q, "total_produto": p.preco_venda*q} for p, q in self.itens_no_carrinho],
            "total": total,
            "recebido": valor_pago,
            "troco": troco
        })

        self.itens_no_carrinho.clear()

        return{
                    "sucesso": True,
                    "mensagem": "Compra finalizada com sucesso",
                    "total": total,
                    "troco": troco
                }

    def total(self):
        return sum(item.preco_venda * quantidade for item, quantidade in self.itens_no_carrinho)
    
    def listar_vendas(self): 
        for venda in self.vendas:
            print(venda) #ainda incompleto (pretendo fazer uma tela ou um bloco de notas para exibir essa parte)

    def validar_compra_existente(self):
        """Método para validar se existe uma compra pendente
        Usado para evitar o fechamento do caixa sem finalizar a compra"""

        if self.itens_no_carrinho:
            return {"sucesso": True,
            "mensagem": "Finalize a compra primeiro"}

        return {"sucesso": False}

    def validar_codigo(self, codigo_produto, quantidade=1):
        if codigo_produto in self.estoque.itens:
            produto = self.estoque.itens[codigo_produto]

            self.carrinho_caixa(produto, quantidade) 
            return True

        return False

    def excluir_do_carrinho(self, produto_codigo):
        for i, (item, _) in enumerate(self.itens_no_carrinho):
            if produto_codigo == item.codigo:
                del self.itens_no_carrinho[i]
                return True