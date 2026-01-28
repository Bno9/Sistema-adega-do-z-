import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tkinter import ttk, messagebox
from tkinter import *
import customtkinter as ctk
from PIL import Image, UnidentifiedImageError
import logging
import json
import os
from datetime import datetime, timedelta, date

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
        self.impressora =  None
        self.frame_atual = None
        self.pode_usar_atalho = False
        self.configs = self.carregar_config()
        self.estoque = Estoque(self.con)
        self.caixa = Caixa(self.estoque, self.iniciar_impressora, self.con)
        self.despesa = Despesas(self.con)
        self.root.bind_all("<Key>", self.tecla_apertada)

        ultimo = self.configs.get("ultimo_dia_backup")
        if ultimo:
            self.ultimo_dia_backup = datetime.fromisoformat(ultimo).date()
        else:
            self.ultimo_dia_backup = None

        hoje = date.today()

        if self.ultimo_dia_backup is None or self.ultimo_dia_backup < hoje:
            self.fazer_backup()
            self.configs["ultimo_dia_backup"] = hoje.isoformat()

            with open("configs.json", "w", encoding="utf-8") as f:
                json.dump(self.configs, f, indent=4, ensure_ascii=False)

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
            5:None
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

    def carregar_config(self):
        try:
            with open("configs.json", "r", encoding="utf-8") as arquivo:
                config = json.load(arquivo)
                return config
        except FileNotFoundError:
                logger.warning("configs.json não encontrado, usando configurações padrão")
                return {}

        except json.JSONDecodeError:
            logger.error("configs.json está vazio ou inválido, recriando arquivo")
            return {}

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
        
    def fazer_backup(self):
        try:
            os.makedirs("backup", exist_ok=True)

            agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nome_backup = f"backup/adega_{agora}.db"

            destino = sqlite3.connect(nome_backup)
            with destino:
                self.con.backup(destino)

            destino.close()

            hoje = date.today()
            self.configs["ultimo_dia_backup"] = hoje.isoformat()

            with open("configs.json", "w", encoding="utf-8") as f:
                json.dump(self.configs, f, indent=4, ensure_ascii=False)

            self.limpar_backups_antigos()

            logger.info("Backup realizado com sucesso | arquivo=%s", nome_backup)
            return True

        except Exception as e:
            logger.error("Erro ao realizar backup | erro=%s", e)
            return False
        
    def limpar_backups_antigos(self):
        dias = self.configs.get("Dias_backup", 7)
        limite = datetime.now() - timedelta(days=dias)
        maximo_backups = 20

        if not os.path.exists("backup"):
            return

        backups = []

        for nome in os.listdir("backup"):
            if nome.endswith(".db"):
                caminho = os.path.join("backup", nome)
                data = datetime.fromtimestamp(os.path.getmtime(caminho))
                backups.append((nome, caminho, data))

        for nome, caminho, data in backups:
            if data < limite:
                os.remove(caminho)
                logger.info("Backup antigo removido | arquivo=%s", nome)

        backups = [(n, c, d) for n, c, d in backups if os.path.exists(c)]

        backups.sort(key=lambda x: x[2])

        while len(backups) > maximo_backups:
            nome, caminho, _ = backups.pop(0)
            os.remove(caminho)
            logger.info("Backup removido por excesso | arquivo=%s", nome)

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
        self.submenu_aberto = None
        
        root.protocol("WM_DELETE_WINDOW", lambda: self.escolher(5)) #bloqueia o X

        #texto
        self.status = StringVar()
        
        #ajustando coluna para centralizar interface
        self.columnconfigure((0,1), weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure((1,2,3,4), weight=1)

        self.master.bind("<Escape>", lambda e: self.escolher(6))

        #frame pra menubar
        header_menubar = ctk.CTkFrame(self, fg_color="#313030")
        header_menubar.grid(row=0, column=0, sticky="w")
        header_menubar.columnconfigure((0,1,2), weight=1)

        #botao configurações
        ctk.CTkButton(header_menubar, 
                    text="Configurações",
                    text_color="white", 
                    hover_color="gray",
                    width=50,  
                    height=30,
                    font=("arial", 22, "bold"),
                    fg_color="#313030",
                    command=lambda: Configs(root, self.main, self.main.configs)
                    ).grid(column=0, row=0, padx=50, pady=20, sticky="ns")
        
        #botao admin
        ctk.CTkButton(header_menubar, 
                    text="Admin",
                    text_color="white", 
                    hover_color="gray",
                    width=50,  
                    height=30,
                    font=("arial", 22, "bold"),
                    fg_color="#313030",
                    command=lambda: self.abrir_submenu(self.submenu_admin)
                    ).grid(column=1, row=0, padx=50, pady=20, sticky="ns")
        
        #submenu
        self.submenu_admin = ctk.CTkFrame(
            header_menubar,
            fg_color="#313030",
            corner_radius=10
        )

        #começa escondido
        self.submenu_admin.grid(column=1, row=1, pady=(0, 10))
        self.submenu_admin.grid_remove()

        #submenu botao cadastrar usuario
        ctk.CTkButton(
            self.submenu_admin,
            text="Cadastrar usuário",
            fg_color="#313030",
            hover_color="gray",
            font=("Arial", 16),
            width=180
        ).pack(padx=10, pady=5)

        #submenu botao alterar senha
        ctk.CTkButton(
            self.submenu_admin,
            text="Alterar senha",
            fg_color="#313030",
            hover_color="gray",
            font=("Arial", 16),
            width=180
        ).pack(padx=10, pady=5)
        
        #botao ajuda
        ctk.CTkButton(header_menubar, 
                    text="Ajuda",
                    text_color="white", 
                    hover_color="gray",
                    width=50,  
                    height=30,
                    font=("arial", 22, "bold"),
                    fg_color="#313030",
                    command=lambda: self.abrir_submenu(self.submenu_ajuda)
                    ).grid(column=2, row=0, padx=50, pady=20, sticky="ns")
        
        self.submenu_ajuda = ctk.CTkFrame(
            header_menubar,
            fg_color="#313030",
            corner_radius=10
        )

        #começa escondido
        self.submenu_ajuda.grid(column=2, row=1, pady=(0, 10))
        self.submenu_ajuda.grid_remove()

        #submenu botao 
        ctk.CTkButton(
            self.submenu_ajuda,
            text="Abrir manual",
            fg_color="#313030",
            hover_color="gray",
            font=("Arial", 16),
            width=180
        ).pack(padx=10, pady=5)

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
            ).grid(column=0, row=1, columnspan=2, sticky="new", pady=20)

        except (FileNotFoundError, UnidentifiedImageError, OSError) as e:
            logger.error("Erro ao carregar logo | erro=%s", e)

            #label menu texto caso imagem nao seja carregada
            ctk.CTkLabel(
            self, 
            text="Adega do zé",
            text_color="white",
            fg_color="#1e1e1e",
            font=("arial", 32, "bold")
            ).grid(column=0, row=1, columnspan=2, sticky="ew", pady=20)

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
            ).grid(column=0, row=2, padx=20, pady=20)

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
            ).grid(column=0, row=3, padx=20, pady=20)

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
            ).grid(column=1, row=2, padx=20, pady=20)
        
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
            ).grid(column=1, row=3, padx=20, pady=20)
        
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
            ).grid(column=0, row=4, padx=20, pady=20)

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
            ).grid(column=1, row=4, padx=20, pady=20)
        
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

        estoque_baixo = self.main.estoque.estoque_baixo(self.main.configs.get("Quantidade_aviso", 4))
        
        if estoque_baixo:
            PopupBaixoEstoque(self, estoque_baixo, self.main.configs)
            logger.info("Produtos com estoque baixo produtos=%s", estoque_baixo)

    def abrir_submenu(self, menu):
        self.main.pode_usar_atalho = False
        if self.submenu_aberto is None:
            menu.grid()
            self.submenu_aberto = menu
            return
        
        if self.submenu_aberto == menu:
            menu.grid_remove()
            self.submenu_aberto = None
            pode_usar_atalho = True
            return
        
        self.submenu_aberto.grid_remove()
        menu.grid()
        self.submenu_aberto = menu

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

            with open("configs.json", "w", encoding="utf-8") as f:
                json.dump(self.main.configs, f, indent=4, ensure_ascii=False)

            self.main.con.close()
            self.status.set("Finalizando programa...")
            self.master.after(2000, self.master.quit)
            logger.info("Programa finalizado")
            return
            
        self.main.trocar_frame(escolhido(self.master, self.main))

    def teclas_menu(self, tecla):
        if tecla.char in ["1", "2", "3", "4", "5"] and self.main.pode_usar_atalho:
            self.escolher(int(tecla.char))

import customtkinter as ctk

class PopupBaixoEstoque(ctk.CTkToplevel):
    #fiz essa classe pra nao deixar tao poluido e ilegivel  o código (inclusive acho que vou fazer nas outras telas tambem com as coisas repetidas)
    def __init__(self, master, produtos, configs):
        super().__init__(master)

        # Config básica
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configs = configs #aqui vai ser um dicionario com informações por exemplo "quantidade": 1, "tempo para fechar popup": "10000" (vou salvar num banco de dados isso e o usuario vai poder configurar na menubar)

        largura = 320
        altura = 180
        margem = 80

        self.update_idletasks()

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        x = screen_w - largura - margem
        y = screen_h - altura - margem

        self.geometry(f"{largura}x{altura}+{x}+{y}")

        frame = ctk.CTkFrame(self, corner_radius=12)
        frame.pack(fill="both", expand=True, padx=8, pady=8)


        for i, produto in enumerate(produtos):
            nome = produto[2]
            quantidade = produto[6]
            
            ctk.CTkLabel(
                frame,
                text=f"Produto {nome} com estoque baixo | Quantidade: {quantidade}",
                text_color="red",
                justify="left",
                wraplength=280
            ).pack(padx=10)


            if i >= 2:
                ctk.CTkLabel(
                    frame,
                    text="E mais...",
                    justify="left",
                    wraplength=280
                ).pack(padx=10)
                self.after(self.configs.get("Tempo_popup", 4000), self.destroy)
                return

        self.after(self.configs.get("Tempo_popup", 4000), self.destroy)

class Configs(ctk.CTkToplevel):
    def __init__(self, master, main, config):
        super().__init__(master)

        self.main = main
        self.attributes("-topmost", True)
        self.title("Configurações")
        self.resizable(False, False)
        self.main.pode_usar_atalho = False

        # variáveis
        self.tempo_popup = StringVar()
        self.quantidade_aviso = StringVar()
        self.dias_backup = StringVar()
        self.config = config


        self.protocol("WM_DELETE_WINDOW", self.fechar)

        self.tempo_popup.set(self.config.get("Tempo_popup", 4000))
        self.quantidade_aviso.set(self.config.get("Quantidade_aviso", 4))
        self.dias_backup.set(self.config.get("Dias_backup", 7))


        frame = ctk.CTkFrame(self, corner_radius=12)
        frame.grid(row=0, column=0, padx=20, pady=20)

        # título
        ctk.CTkLabel(
            frame,
            text="Configurações",
            font=("Arial", 20, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # TEMPO POPUP
        ctk.CTkLabel(
            frame,
            text="Tempo para popup expirar (ms)",
            anchor="w"
        ).grid(row=1, column=0, columnspan=2, sticky="w")

        ctk.CTkEntry(
            frame,
            textvariable=self.tempo_popup,
            width=250
        ).grid(row=2, column=0, columnspan=2, pady=(0, 15))

        # QUANTIDADE AVISO 
        ctk.CTkLabel(
            frame,
            text="Quantidade para aviso de estoque",
            anchor="w"
        ).grid(row=3, column=0, columnspan=2, sticky="w")

        ctk.CTkEntry(
            frame,
            textvariable=self.quantidade_aviso,
            width=250
        ).grid(row=4, column=0, columnspan=2, pady=(0, 25))

        # DIAS BACKUP
        ctk.CTkLabel(
            frame,
            text="Manter backups por quantos dias?",
            anchor="w"
        ).grid(row=5, column=0, columnspan=2, sticky="w")

        ctk.CTkEntry(
            frame,
            textvariable=self.dias_backup,
            width=250
        ).grid(row=6, column=0, columnspan=2, pady=(0, 20))

        # FAZER BACKUP
        ctk.CTkLabel(
            frame,
            text="Backup",
            font=("Arial", 16, "bold")
        ).grid(row=7, column=0, columnspan=2, pady=(10, 5))

        ctk.CTkButton(
            frame,
            text="Fazer backup agora",
            width=260,
            fg_color="#1f6aa5",
            hover_color="#144870",
            command=self.fazer_backup
        ).grid(row=8, column=0, columnspan=2, pady=(0, 25))

        # ---------- BOTÕES ----------
        ctk.CTkButton(
            frame,
            text="Salvar",
            width=120,
            command=self.salvar
        ).grid(row=9, column=0, padx=10)

        ctk.CTkButton(
            frame,
            text="Cancelar",
            width=120,
            fg_color="gray",
            hover_color="#555555",
            command=self.fechar
        ).grid(row=9, column=1, padx=10)

        # ---------- CENTRALIZAR ----------
        self.update_idletasks()

        largura = frame.winfo_width() + 40
        altura = frame.winfo_height() + 40

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        x = (screen_w // 2) - (largura // 2)
        y = (screen_h // 2) - (altura // 2)

        self.geometry(f"{largura}x{altura}+{x}+{y}")

    def salvar(self):
        try:
            Tempo_popup = int(self.tempo_popup.get())
            Quantidade_aviso = int(self.quantidade_aviso.get())
            Dias_backup = int(self.dias_backup.get())
        except ValueError:
            messagebox.showinfo(
                title="Erro",
                message="Digite apenas números!",
                parent=self
            )
            return

        self.config = {
            "Tempo_popup": Tempo_popup,
            "Quantidade_aviso": Quantidade_aviso,
            "Dias_backup": Dias_backup
        }

        self.main.configs.update(self.config)

        with open("configs.json", "w", encoding="utf-8") as arquivo:
            json.dump(self.main.configs, arquivo, indent=4, ensure_ascii=False)

        self.main.pode_usar_atalho = True
        self.destroy()

    def fechar(self):
        self.main.pode_usar_atalho = True
        self.destroy()

    def fazer_backup(self):
        sucesso = self.main.fazer_backup()

        if sucesso:
            messagebox.showinfo(
                    title="Backup",
                    message="Backup realizado com sucesso!",
                    parent=self
            )
        else:
            messagebox.showerror(
                                title="Erro",
                                message="Falha ao realizar backup.",
                                parent=self
                            )

ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.title("Adega do zé 2.1")
root.configure(bg="#1e1e1e")
root.attributes("-zoomed", True)
#root.state("zoomed") para windows

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

logger = logging.getLogger(__name__)

logging.basicConfig(filename="logs", level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s - %(message)s")

m = Main(root) #Instanciando a main

root.mainloop() #Loop de eventos do customtkinter