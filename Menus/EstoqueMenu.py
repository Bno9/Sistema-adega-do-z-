class EstoqueMenu:

    def __init__(self, referencia_main):
        self.referencia_main = referencia_main


    def Menu(self):
        print("""
        Menu do estoque
        
        1- Ver estoque
        2- Remover produto 
        3- Sair
        """)

        try:
            escolha = int(input("Digite a opção desejada: "))
        except ValueError:
            print("Digite apenas numeros")
            return

        if escolha == 1:
            self.referencia_main.estoque.listar_itens()

        elif escolha == 2:
            try:
                codigo = int(input("Digite o codigo do produto que deseja remover: "))
                self.referencia_main.estoque.remover_produto(codigo)
            except ValueError:
                print("Digite apenas numeros")
                return

        elif escolha == 3:
            self.referencia_main.change_state(self.referencia_main)

        else:
            print("Escolha uma das opções disponiveis")