import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tkinter import ttk
from tkinter import *

from Utils.Caixa import Caixa
from Utils.Estoque import Estoque

from Menus.CaixaMenu import CaixaMenu
from Menus.EstoqueMenu import EstoqueMenu
from Menus.ProdutoMenu import ProdutoMenu

class Main:
    """
    Controla o fluxo principal da aplicação.

    - Recebe o root do tkinter para ter controle da interface gráfica
    - Possui métodos para trocar de tela
    - Permite retornar ao menu principal
    """

    def __init__(self, root):
        """
        Inicializa a aplicação principal

        Cria instâncias de Caixa e Estoque
        e mantém o controle do frame atual
        """
        self.root = root
        self.frame_atual = None
        self.estoque = Estoque()
        self.caixa = Caixa(self.estoque)

        self.trocar_frame(MenuPrincipal(self.root, self))

    def trocar_frame(self, novo_frame):
        if self.frame_atual:
            self.frame_atual.destroy()

        self.frame_atual = novo_frame
        self.frame_atual.grid(column=0, row=0, sticky="nsew")
    
    def voltar_menu_principal(self):
        self.trocar_frame(MenuPrincipal(self.root, self))

class MenuPrincipal(ttk.Frame):
    """Classe principal que controla toda interface e herda da classe ttk.Frame"""

    def __init__(self, root, main):
        """
        Inicializa o menu principal.

        Args:
            root (Tk): Instância principal do Tkinter.
            main (Main): Controlador principal da aplicação.
        """

        super().__init__(root, padding=(3, 3, 12, 12)) #instancia o root usando o init da classe pai
        self.main = main

        self.error = StringVar()

        #mapa das classes
        self.mapa = {
            1:CaixaMenu,
            2:EstoqueMenu,
            3:ProdutoMenu,
            4:None
        }

        #ajustando coluna para centralizar interface
        self.columnconfigure(0, weight=1)
           
        ttk.Label(
            self, 
            text="Adega do zé",
            font=("Arial", 16, "bold"),
            anchor="center",
            padding=20
            ).grid(column=0, row=0, sticky="ew", pady=20)

        ttk.Label(
            self,
            textvariable=self.error
            ).grid(column=0, row=5, sticky=(S,N), pady=20)
     
        ttk.Button(
            self, 
            text="Abrir caixa", 
            width=50, 
            padding=30,  
            command=lambda: self.escolher(1)
            ).grid(column=0, row=1, sticky=(S,N), pady=20)

        ttk.Button(self, 
            text="Estoque", 
            width=50, 
            padding=30, 
            command=lambda: self.escolher(2)
            ).grid(column=0, row=2, sticky=(S,N), pady=20)

        ttk.Button(self, 
            text="Cadastrar / Editar produto", 
            width=50, 
            padding=30, 
            command=lambda: self.escolher(3)
            ).grid(column=0, row=3, sticky=(S,N), pady=20)

        ttk.Button(self, 
            text="Sair", 
            width=50, 
            padding=30, 
            command=lambda: self.escolher(4)
            ).grid(column=0, row=4, sticky=(S,N), pady=20)

    def escolher(self, opcao):
        """Recebe a opção escolhida,
         Converte a opção em int, busca a tela correspondente no mapa
         Chama o metodo da classe main para trocar de interface, enviando o root e a classe main"""
        try:
            opcao = int(opcao)

        except ValueError:
            self.error.set("Digite apenas numeros inteiros")
            return

        escolhido = self.mapa.get(opcao)

        if escolhido is None:
            self.error.set("Finalizando programa...")
            self.master.after(2000, self.master.quit)
            return
            
        self.main.trocar_frame(escolhido(self.master, self.main))

root = Tk()
root.title("Adega do zé")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

m = Main(root) #Instanciando a main

root.mainloop() #Loop de eventos do tkinter
