import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tkinter import ttk
from tkinter import *
import customtkinter as ctk
from PIL import Image, UnidentifiedImageError
import logging

import sqlite3

from Utils.Caixa import Caixa
from Utils.Estoque import Estoque
from Utils.Despesa import Despesas
from Utils.Recibo import Recibo, ImpressoraBase, ImpressoraTxt, ImpressoraWindows
from Utils.Produto import Produto

from Menus.CaixaMenu import CaixaMenu
from Menus.DespesasMenu import DespesasMenu
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
        self.con = sqlite3.connect("adega.db", timeout=10, check_same_thread=False)
        self.impressora = None
        self.frame_atual = None
        self.pode_usar_atalho = False
        self.estoque = Estoque(self.con)
        self.caixa = Caixa(self.estoque, self.iniciar_impressora, self.con)
        self.despesa = Despesas(self.con)
        self.root.bind_all("<Key>", self.tecla_apertada)

        #despesas criadas para teste
        self.despesa.adicionar_despesa("contador", 100)
        self.despesa.adicionar_despesa("aluguel", 1700, "10/12/2026", "Aluguel do imóvel")
        self.despesa.adicionar_despesa("mercadoria", 10000, "15/8/2025")
        self.despesa.adicionar_despesa("mercadoria", 1206, "15/8/2025", "Red label, Black label, Ballena")
        self.despesa.adicionar_despesa("mercadoria", 600, "15/8/2025", "Fardos energetico")
        self.despesa.adicionar_despesa("funcionario", 5000, "5/2/2026", "Salário e décimo terceiro")


        #mapa das classes
        self.mapa = {
            1:CaixaMenu,
            2:EstoqueMenu,
            3:ProdutoMenu,
            4:DespesasMenu,
            5:None,
            6:None
        }

        #inicia o frame menu principal
        self.trocar_frame(MenuPrincipal(self.root, self))

    def iniciar_impressora(self):
        if self.impressora is None:
            try:
                self.impressora = ImpressoraWindows("MP-4200 TH")
            except Exception as e:
                logger.error("Erro ao iniciar impressora | erro=%s", e)
                self.impressora = ImpressoraTxt()
            
            return self.impressora


    def tecla_apertada(self, tecla):
        """Detecta a tecla apertada e chama a função teclas menu do frame atual"""
        if hasattr(self.frame_atual, "teclas_menu"):
            self.frame_atual.teclas_menu(tecla)

    def trocar_frame(self, novo_frame):
        if self.frame_atual:
            self.frame_atual.destroy()

        logger.debug("Frame trocado | frame_atual=%s", novo_frame)
        self.frame_atual = novo_frame
        self.frame_atual.grid(column=0, row=0, sticky="nsew")

    def verificar_senha(self, senha, modal):
        if senha.get() == "123":
            modal.destroy()
            self.pode_usar_atalho = True
    
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

        self.master.bind("<Escape>", lambda e: self.escolher(6))

        #Imagem para usar no label principal
        try:
            img = ctk.CTkImage(
                light_image=Image.open("/home/usuario/Projetos/Adega_do_ze/images/Adega_fundo_cinza.png"),
                size=(400, 400)
            )

            #label menu imagem
            ctk.CTkLabel(
            self, 
            text="",
            image=img,
            fg_color="#1e1e1e"
            ).grid(column=0, row=0, columnspan=2, sticky="ew", pady=20)

        except (FileNotFoundError, UnidentifiedImageError, OSError) as e:
            logger.error("Erro ao carregar logo | erro=%s", e)

            #label menu texto caso imagem nao seja carregada
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
            text="Caixa",
            text_color="black", 
            corner_radius=40,
            border_color="black",
            hover_color="white",
            border_width=5,
            width=500,  
            height=200,
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
            width=500,  
            height=200,
            fg_color="orange",
            font=("Arial", 30, "bold"),
            command=lambda: self.escolher(2)
            ).grid(column=0, row=2, padx=20, pady=20)

        #botao Relatórios
        ctk.CTkButton(self, 
            text="Relatórios (W.I.P)", 
            text_color="black", 
            corner_radius=40,
            border_color="black",
            hover_color="white",
            border_width=5,
            width=500,  
            height=200,
            fg_color="orange",
            font=("Arial", 30, "bold"),
            command=lambda: self.escolher(5)
            ).grid(column=1, row=1, padx=20, pady=20)
        
        #botao despesas
        ctk.CTkButton(self, 
            text="Despesas", 
            text_color="black", 
            corner_radius=40,
            border_color="black",
            hover_color="white",
            border_width=5,
            width=500,  
            height=200,
            fg_color="orange",
            font=("Arial", 30, "bold"),
            command=lambda: self.escolher(4)
            ).grid(column=1, row=2, padx=20, pady=20)
        
        #botao cadastro
        ctk.CTkButton(self, 
            text="Cadastro", 
            text_color="black", 
            corner_radius=40,
            border_color="black",
            hover_color="white",
            border_width=5,
            width=500,  
            height=200,
            fg_color="orange",
            font=("Arial", 30, "bold"),
            command=lambda: self.escolher(3)
            ).grid(column=0, row=3, padx=20, pady=20)

        #botao sair
        ctk.CTkButton(self, 
            text="Sair", 
            text_color="black", 
            corner_radius=40,
            border_color="black",
            hover_color="red",
            border_width=5,
            width=500,  
            height=200,
            fg_color="orange",
            font=("Arial", 30, "bold"),
            command=lambda: self.escolher(6)
            ).grid(column=1, row=3, padx=20, pady=20)
        
        if self.main.pode_usar_atalho == False:
            senha = StringVar()

            tela_senha = ctk.CTkToplevel(self, fg_color="#1e1e1e")

            tela_senha.title("Consultar produto")
            tela_senha.geometry("300x300")

            tela_senha.transient(self)
            tela_senha.update_idletasks()
            tela_senha.grab_set()   

            tela_senha.columnconfigure(0, weight=1)
            tela_senha.rowconfigure((0,1), weight=1)
            header =  ctk.CTkFrame(tela_senha, fg_color="#1e1e1e")
            entrys =  ctk.CTkFrame(tela_senha, fg_color="#1e1e1e")

            header.grid(row=0, column=0)

            entrys.rowconfigure(0, weight=1)
            entrys.columnconfigure(0, weight=1)
            entrys.grid(row=1, column=0)

            ctk.CTkLabel(header, 
                        text="Digite a senha",
                        font=("arial", 32, "bold")
                        ).grid(row=0, column=0, columnspan=2)
            
            entry = ctk.CTkEntry(entrys,
                            textvariable=senha,
                            font=("Arial", 20, "bold"),
                            width=400,
                            height=50)
            entry.grid(row=0, column=0)
            entry.focus_set()


            tela_senha.protocol("WM_DELETE_WINDOW", self.master.quit) #Fecha o programa caso o modal seja fechado

            entry.bind("<Return>", lambda e: self.main.verificar_senha(senha, tela_senha))

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
            #Apagando os testes para nao acumular
            for i in range(10000):
                self.main.despesa.excluir_despesa(i)


            self.main.con.close()
            self.status.set("Finalizando programa...")
            self.master.after(2000, self.master.quit)
            logger.info("Programa finalizado")
            return
            
        self.main.trocar_frame(escolhido(self.master, self.main))

    def teclas_menu(self, tecla):
        if tecla.char in ["1", "2", "3", "4", "5", "6"]and self.main.pode_usar_atalho:
            self.escolher(int(tecla.char))


ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.title("Adega do zé 2.1")
root.configure(bg="#1e1e1e")
root.attributes("-zoomed", True)
#root.protocol("WM_DELETE_WINDOW", lambda: None) #bloqueia o X
#root.state("zoomed") para windows

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

logger = logging.getLogger(__name__)

logging.basicConfig(filename="logs", level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s - %(message)s")


m = Main(root) #Instanciando a main


root.mainloop() #Loop de eventos do customtkinter

