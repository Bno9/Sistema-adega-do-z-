class Caixa:
    
    def __init__(self, estoque):
        self.estoque = estoque
        self.vendas = []
        self.calculo = []

    def carrinho(self, produto):
        for i, (item, quantidade) in enumerate(self.calculo):
            if produto.codigo == item.codigo:
                self.calculo[i] = (item, quantidade + 1)

                print("Produto adicionado ao carrinho")
                print(f"Total: {self.total()}")
                return

        self.calculo.append((produto, 1))
        print("Produto adicionado ao carrinho")
        print(f"Total: {self.total()}")

    def finalizar_compra(self, valor_pago):
        if not self.calculo:
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
        
        for item, quantidade in self.calculo:
            self.estoque.itens[item.codigo].quantidade -= quantidade

        self.vendas.append({
            "itens": [{"codigo": p.codigo, "nome": p.nome, "quantidade": q, "total_produto": p.preco_venda*q} for p, q in self.calculo],
            "total": total,
            "recebido": valor_pago,
            "troco": troco
        })

        self.calculo.clear()

        return{
                    "sucesso": True,
                    "mensagem": "Compra finalizada com sucesso",
                    "total": total,
                    "troco": troco
                }

    def total(self):
        return sum(item.preco_venda * quantidade for item, quantidade in self.calculo)
    

    def listar_vendas(self): #Isso é uma função que vai ficar na parte de adm depois
        for d in self.vendas:
            print(d) #ainda incompleto

    def validar_compra_existente(self):
        if self.calculo:
            return {"sucesso": False,
            "mensagem": "Finalize a compra primeiro"}

        return {"sucesso": True,
        "mensagem": "Nada"}

    def validar_codigo(self, codigo_produto):
        if codigo_produto in self.estoque.itens:

            produto = self.estoque.itens[codigo_produto]
            self.carrinho(produto)
            return True

        else:
            print("Produto não encontrado")
            return False
