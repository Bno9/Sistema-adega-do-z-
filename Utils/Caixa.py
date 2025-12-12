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

    def finalizar_compra(self):
        if not self.calculo:
            print("Nenhum item no carrinho")
            return

        total = self.total()
        print(f"Total: {total:.2f}")

        valor_pago = float(input("Valor recebido do cliente R$: "))

        if valor_pago < total:
            print("Valor insuficiente!")
            return

        troco = valor_pago - total

        print(f"Troco: {troco:.2f}")
        
        for item, quantidade in self.calculo:
            self.estoque.itens[item.codigo].quantidade -= quantidade

        self.vendas.append({
            "itens": [{"codigo": p.codigo, "nome": p.nome, "quantidade": q, "total_produto": p.preco_venda*q} for p, q in self.calculo],
            "total": total,
            "recebido": valor_pago,
            "troco": troco
        })

        self.calculo.clear()

        print("Compra finalizada com sucesso")


    def total(self):
        return sum(item.preco_venda * quantidade for item, quantidade in self.calculo)
    

    def listar_vendas(self): #Isso é uma função que vai ficar na parte de adm depois
        for d in self.vendas:
            print(d)

    def validar_compra_existente(self):
        if self.calculo:
            print("Finalize a compra primeiro")
            return True