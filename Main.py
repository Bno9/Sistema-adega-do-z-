class Main:

    def __init__(self):
        self.running = True
        self.state = self

    
    def Menu(self):
        print("""
        Adega do zé

        1- Abrir caixa
        2- Conferir estoque
        3- Alterar produto
        4- Fechar
        """)

        escolha = int(input("Digite o numero do que deseja acessar: "))

        if escolha == 1:
            from CaixaMenu import CaixaMenu
            self.change_state(CaixaMenu(self))

        elif escolha == 2:
            from EstoqueMenu import EstoqueMenu
            self.change_state(EstoqueMenu(self))

        elif escolha == 3:
            from ProdutoMenu import ProdutoMenu
            self.change_state(ProdutoMenu(self))
        
        elif escolha == 4:
            print("Fechando...")
            self.running = False


    def change_state(self, novo_estado):
        self.state = novo_estado

    

m = Main()

while m.running:
    m.state.Menu()
