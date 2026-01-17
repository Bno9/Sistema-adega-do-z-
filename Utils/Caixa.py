from Utils.Recibo import Recibo, ImpressoraBase, ImpressoraTxt, ImpressoraWindows

class Caixa:
    
    def __init__(self, estoque, iniciar_impressora, con):
        self.recibo = Recibo()
        self.iniciar_impressora = iniciar_impressora
        self.estoque = estoque
        self.con = con
        self.vendas = []
        self.itens_no_carrinho = [] #aqui eu mantive objetos produto porque ficou mais facil e nao precisei mexer muito no codigo
        self.desconto = 0

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

        if valor_pago < total or valor_pago > 100000:
            return{
                "sucesso": False,
                "mensagem": "Valor recebido inválido"
            }

        troco = valor_pago - total
        
        for item, quantidade in self.itens_no_carrinho:
            self.estoque.dar_baixa(item.codigo, quantidade)

        self.vendas.append({
            "itens": [{"codigo": p.codigo, "nome": p.nome, "quantidade": q, "total_produto": p.preco_venda*q} for p, q in self.itens_no_carrinho],
            "total": total,
            "recebido": valor_pago,
            "troco": troco
        })

        linhas = self.recibo.gerar_linhas(self.itens_no_carrinho, valor_pago) #acho que vou precisar mudar isso pra parte de imprimir recibo depois, porque vou ter que adicionar o cpf pro sat

        self.itens_no_carrinho.clear()

        return{
                    "sucesso": True,
                    "mensagem": "Compra finalizada com sucesso",
                    "total": total,
                    "troco": troco,
                    "linhas": linhas
                }
    
    def aplicar_desconto(self, valor):
        self.desconto = valor
        #aqui é pra atualizar a tela
        return self.total()

    def imprimir_recibo(self, linhas, cpf=None):
        if cpf == "":
            return
        
        impressora = self.iniciar_impressora()
        impressora.imprimir(linhas)

    def total(self):
        if self.desconto:
            return sum(item.preco_venda * quantidade for item, quantidade in self.itens_no_carrinho) - self.desconto
    
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
        if self.estoque.conferir_se_existe_no_estoque(codigo_produto):
            cursor_estoque = self.estoque.cur
            cursor_estoque.execute("SELECT codigo, nome, tipo, preco_custo, preco_venda, quantidade FROM produtos WHERE codigo=?", (codigo_produto,))
            row = cursor_estoque.fetchone()

            from Utils.Produto import Produto
            produto = Produto(*row)
        
            self.carrinho_caixa(produto, quantidade) 
            return True

        return False

    def excluir_do_carrinho(self, produto_codigo):
        for i, (item, _) in enumerate(self.itens_no_carrinho):
            if produto_codigo == item.codigo:
                del self.itens_no_carrinho[i]
                return True