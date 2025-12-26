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

    def __init__(self, root):
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

    def __init__(self, root, main):
        super().__init__(root, padding=(3, 3, 12, 12))
        self.main = main

        self.error = StringVar()
        self.mapa = {
            1:CaixaMenu,
            2:EstoqueMenu,
            3:ProdutoMenu,
            4:None
        }
           
        ttk.Label(self, text="""
                Adega do zé


                """).grid(column=0, row=0, sticky=W)

        ttk.Label(self, textvariable=self.error).grid(column=2, row=2, sticky=(W, E))
     
        ttk.Button(self, text="Abrir caixa", command=lambda: self.escolher(1)).grid(column=1, row=1, sticky=W)

        ttk.Button(self, text="Estoque", command=lambda: self.escolher(2)).grid(column=1, row=2, sticky=W)

        ttk.Button(self, text="Cadastrar / Editar produto", command=lambda: self.escolher(3)).grid(column=1, row=3, sticky=W)

        ttk.Button(self, text="Sair", command=lambda: self.escolher(4)).grid(column=1, row=4, sticky=W)

    def escolher(self, opcao):
        try:
            opcao = int(opcao)

        except ValueError:
            self.error.set("Digite apenas numeros inteiros")
            return

        escolhido = self.mapa.get(opcao)

        if escolhido is None:
            self.master.quit()
            return
            
        self.main.trocar_frame(escolhido(self.master, self.main))

root = Tk()
root.title("Menu principal")

m = Main(root)


root.mainloop()
