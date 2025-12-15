class CaixaMenu:

    def __init__(self, referencia_main):
        self.referencia_main = referencia_main

    def Menu(self):
        print("""
        Menu do caixa
        
        1- Ler código (quando tiver interface vai mudar completamente)
        2- Finalizar compra
        3- Sair
        """)

        try:
            escolha = int(input("Escolha a opção desejada: "))
        except ValueError:
            print("Digite apenas numeros")
            return


        if escolha == 1:

            try:
                codigo_produto = int(input("Leia o codigo do produto: "))
            except ValueError:
                print("Digite apenas numeros")
                return

            if codigo_produto in self.referencia_main.estoque.itens:

                produto = self.referencia_main.estoque.itens[codigo_produto]
                self.referencia_main.caixa.carrinho(produto)

            else:
                print("Produto não encontrado")
                return

        elif escolha == 2:
            self.referencia_main.caixa.finalizar_compra()
            

        elif escolha == 3:
            if self.referencia_main.caixa.validar_compra_existente():
                return
            self.referencia_main.change_state(self.referencia_main)

        else:
            print("Opção inválida")