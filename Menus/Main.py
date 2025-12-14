import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))



from Utils.Caixa import Caixa
from Utils.Estoque import Estoque

class Main:

    def __init__(self):
        self.running = True
        self.state = self
        self.estoque = Estoque()
        self.caixa = Caixa(self.estoque)

    
    def Menu(self):
        print("""
        Adega do zé

        1- Abrir caixa
        2- Conferir estoque
        3- Cadastrar / Alterar produto
        4- Fechar
        """)

        try:
            escolha = int(input("Digite o numero do que deseja acessar: "))
        
        except ValueError:
            print("Digite apenas numeros")
            return

        if escolha == 1:
            from Menus.CaixaMenu import CaixaMenu
            self.change_state(CaixaMenu(self))

        elif escolha == 2:
            from Menus.EstoqueMenu import EstoqueMenu
            self.change_state(EstoqueMenu(self))

        elif escolha == 3:
            from Menus.ProdutoMenu import ProdutoMenu
            self.change_state(ProdutoMenu(self))
        
        elif escolha == 4:
            print("Fechando...")
            self.running = False

        else:
            print("Opção inválida")


    def change_state(self, novo_estado):
        self.state = novo_estado

    

m = Main()

while m.running:
    m.state.Menu()
