import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tkinter import ttk
from tkinter import *
import customtkinter as ctk
from PIL import Image, UnidentifiedImageError


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
        self.root.bind_all("<Key>", self.tecla_apertada)

        #produtos criados para teste
        self.estoque.criar_produto(1,"Whisky",2.20,5,10)
        self.estoque.criar_produto(34,"Red label",50,80,2)
        self.estoque.criar_produto(913495182,"Cigarro",10,30,10)
        self.estoque.criar_produto(2,"Agua sem gas",1,3,100)
        for i in range(2000):
             self.estoque.criar_produto(i,"Teste",20,150,10)


        #mapa das classes
        self.mapa = {
            1:CaixaMenu,
            2:EstoqueMenu,
            3:ProdutoMenu,
            4:None
        }

        #inicia o frame menu principal
        self.trocar_frame(MenuPrincipal(self.root, self))

    def tecla_apertada(self, tecla):
        """Detecta a tecla apertada e chama a função teclas menu do frame atual"""
        if hasattr(self.frame_atual, "teclas_menu"):
            self.frame_atual.teclas_menu(tecla)

    def trocar_frame(self, novo_frame):
        if self.frame_atual:
            self.frame_atual.destroy()

        self.frame_atual = novo_frame
        self.frame_atual.grid(column=0, row=0, sticky="nsew")
    
    def voltar_menu_principal(self):
        self.trocar_frame(MenuPrincipal(self.root, self))

class MenuPrincipal(ctk.CTkFrame):
    """Classe principal que controla toda interface e herda da classe ctk.Frame"""

    def __init__(self, root, main):
        """
        Inicializa o menu principal.

        Args:
            root (Tk): Instância principal do Tkinter.
            main (Main): Controlador principal da aplicação.
        """

        super().__init__(master=root, fg_color="#1e1e1e") #instancia o root usando o init da classe pai
        self.main = main

        #texto
        self.status = StringVar()
        
        #ajustando coluna para centralizar interface
        self.columnconfigure((0,1), weight=1)
        self.rowconfigure((0,1,2), weight=1)

        self.master.bind("<Escape>", lambda e: self.escolher(4))

        #Imagem para usar no label principal
        try:
            img = ctk.CTkImage(
                light_image=Image.open("/home/usuario/Projetos/Adega_do_ze/images/Adega_do_ze.png"),
                size=(400, 400)
            )

            #label menu imagem
            ctk.CTkLabel(
            self, 
            text="",
            image=img
            ).grid(column=0, row=0, columnspan=2, sticky="ew", pady=20)

        except (FileNotFoundError, UnidentifiedImageError, OSError) as e:
            print(f"Erro ao carregar logo: {e}")

            #label menu texto
            ctk.CTkLabel(
            self, 
            text="Adega do zé",
            text_color="white",
            fg_color="#1e1e1e",
            font=("arial", 32, "bold")
            ).grid(column=0, row=0, columnspan=2, sticky="ew", pady=20)

        #label status
        ctk.CTkLabel(
            self,
            textvariable=self.status,
            font=("Arial", 24, "bold"),
            text_color="red"
            ).grid(column=0, row=5, columnspan=2, sticky="ew", padx=20, pady=20)
     
        #botao caixa
        ctk.CTkButton(
            self, 
            text="Abrir caixa",
            text_color="black", 
            corner_radius=40,
            border_color="black",
            hover_color="white",
            border_width=5,
            width=600,  
            height=300,
            font=("Arial", 30, "bold"),
            fg_color="orange",
            command=lambda: self.escolher(1)
            ).grid(column=0, row=1, padx=20, pady=20)

        #botao estoque
        ctk.CTkButton(self, 
            text="Estoque",
            text_color="black", 
            corner_radius=40,
            border_color="black",
            hover_color="white",
            border_width=5,
            width=600,  
            height=300,
            fg_color="orange",
            font=("Arial", 30, "bold"),
            command=lambda: self.escolher(2)
            ).grid(column=0, row=2, padx=20, pady=20)

        #botao cadastro
        ctk.CTkButton(self, 
            text="Cadastrar / Editar produto", 
            text_color="black", 
            corner_radius=40,
            border_color="black",
            hover_color="white",
            border_width=5,
            width=600,  
            height=300,
            fg_color="orange",
            font=("Arial", 30, "bold"),
            command=lambda: self.escolher(3)
            ).grid(column=1, row=1, padx=20, pady=20)


        #botao sair
        ctk.CTkButton(self, 
            text="Sair", 
            text_color="black", 
            corner_radius=40,
            border_color="black",
            hover_color="red",
            border_width=5,
            width=600,  
            height=300,
            fg_color="orange",
            font=("Arial", 30, "bold"),
            command=lambda: self.escolher(4)
            ).grid(column=1, row=2, padx=20, pady=20)

    def escolher(self, opcao):
        """Recebe a opção escolhida,
         Converte a opção em int, busca a tela correspondente no mapa
         Chama o metodo da classe main para trocar de interface, enviando o root e a classe main"""
        try:
            opcao = int(opcao)

        except ValueError:
            self.status.set("Digite apenas numeros inteiros")
            return

        escolhido = self.main.mapa.get(opcao)

        if escolhido is None:
            self.status.set("Finalizando programa...")
            self.master.after(2000, self.master.quit)
            return
            
        self.main.trocar_frame(escolhido(self.master, self.main))

    def teclas_menu(self, tecla):
        if tecla.char in ["1", "2", "3", "4"]:
            self.escolher(int(tecla.char))

root = Tk()
root.title("Adega do zé")



root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


m = Main(root) #Instanciando a main

root.mainloop() #Loop de eventos do tkinter

