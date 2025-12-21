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

        self.opcao = StringVar()
        self.error = StringVar()
        self.mapa = {
            1:CaixaMenu,
            2:EstoqueMenu,
            3:ProdutoMenu,
            4:None
        }
           
        ttk.Label(self, text="""
                Adega do zé

                1- Abrir caixa
                2- Conferir estoque
                3- Cadastrar / Alterar produto
                4- Fechar""").grid(column=0, row=0, sticky=W)


        ttk.Entry(self, width=10, textvariable=self.opcao).grid(row=0, column=1, sticky=(W, E))

        ttk.Label(self, textvariable=self.error).grid(column=1, row=2, sticky=(W, E))
     
        ttk.Button(self, text="Escolher", command=self.escolher).grid(column=3, row=0, sticky=W)

    def escolher(self):
        try:
            opcao = int(self.opcao.get())

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
