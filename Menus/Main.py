import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tkinter import ttk, messagebox
from tkinter import *
import customtkinter as ctk
from PIL import Image, UnidentifiedImageError
import logging
import json
from datetime import datetime, timedelta, date

import sqlite3

from Utils.Caixa import Caixa
from Utils.Estoque import Estoque
from Utils.Despesa import Despesas
from Utils.Recibo import Recibo, ImpressoraBase, ImpressoraTxt, ImpressoraWindows
from Utils.Produto import Produto
from Utils.Usuarios import Usuario

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
        self.pode_usar_atalho = True
        self.configs = self.carregar_config()
        self.configs_window = None
        self.estoque = Estoque(self.con)
        self.caixa = Caixa(self.estoque, self.iniciar_impressora, self.con)
        self.despesa = Despesas(self.con)
        self.root.bind_all("<Key>", self.tecla_apertada)
        self.usuario = Usuario(self.con)

        self.usuario_atual = None #Passar sempre o usuario que esta utilizando programa para salvar nos relatorios

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

        #mapa das classes
        self.mapa = {
            1:CaixaMenu,
            2:EstoqueMenu,
            3:ProdutoMenu,
            4:DespesasMenu,
            5:CaixaMenu
        }

        #inicia o frame menu principal
        ModalSenha(self.root, self)

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

    def verificar_senha(self, senha, usuario, modal):
        senha = senha.get()
        resultado = self.usuario.verificar_login(usuario, senha)

        if resultado[0] == True and resultado[2] == "admin":
            modal.destroy()
            self.trocar_frame(MenuPrincipal(self.root, self))
        
        elif resultado[0] == True and resultado[2] == "funcionario":
            modal.destroy()
            self.trocar_frame(CaixaMenu(self.root, self, usuario, on_sair=self.fechar_app))
        
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

    def get_usuarios(self):
        usuarios = self.usuario.listar_usuarios()
        return [nome for nome, _ in usuarios]
    
    def abrir_configs(self):
        if self.configs_window and self.configs_window.winfo_exists():
            self.configs_window.lift()
            self.configs_window.focus_force()
            return

        self.configs_window = Configs(
            self.root,
            self,
            on_close=self._fechar_configs
        )

    def _fechar_configs(self):
        self.configs_window = None

    def voltar_menu_principal(self):
        self.trocar_frame(MenuPrincipal(self.root, self))

    def fechar_app(self):
        with open("configs.json", "w", encoding="utf-8") as f:
            json.dump(self.configs, f, indent=4, ensure_ascii=False)

        self.con.close()
        #self.status.set("Finalizando programa...") #mudar aqui depois (talvez pra uma messagebox do ttk)
        self.root.after(2000, self.root.quit)
        logger.info("Programa finalizado")
        return

class ModalSenha(ctk.CTkToplevel):
    def __init__(self, master, main):
        self.main = main
        super().__init__(master=master, fg_color="#1e1e1e")

        senha = StringVar()
        usuarios = self.main.get_usuarios()
        self.usuario_atual = ctk.StringVar()
        self.usuario_atual.set("Sistema")

        self.title("Login")
        self.geometry("400x400")

        self.transient(master)
        self.update_idletasks()
        self.grab_set()   

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0,1), weight=1)
        header =  ctk.CTkFrame(self, fg_color="#1e1e1e")
        entrys =  ctk.CTkFrame(self, fg_color="#1e1e1e")

        header.grid(row=0, column=0)
        header.rowconfigure(0, weight=1)

        entrys.rowconfigure((0,1), weight=1)
        entrys.columnconfigure(0, weight=1)
        entrys.grid(row=1, column=0, sticky="nsew")

        ctk.CTkLabel(header, 
                    text="Digite a senha",
                    width=300,
                    font=("arial", 32, "bold")
                    ).grid(row=0, column=0)
        
        ctk.CTkComboBox(entrys,
                        values=usuarios,
                        variable=self.usuario_atual,
                        font=("arial", 32, "bold"),
                        command=self.mudar_usuario,
                        width=200
                        ).grid(row=0, column=0)
        
        entry = ctk.CTkEntry(entrys,    
                        textvariable=senha,
                        font=("Arial", 20, "bold"),
                        width=400,
                        height=50)
        entry.grid(row=1, column=0)
        entry.after(1000, entry.focus_set)


        self.protocol("WM_DELETE_WINDOW", self.master.quit) #Fecha o programa caso o modal seja fechado

        entry.bind("<Return>", lambda e: self.main.verificar_senha(senha, self.usuario_atual.get(), self))

    def mudar_usuario(self, usuario):
        self.usuario_atual.set(usuario)

class ModalAlterarSenha(ctk.CTkToplevel):
    def __init__(self, master, main):
        self.main = main
        super().__init__(master=master, fg_color="#1e1e1e")

        senha = StringVar()
        usuarios = self.main.get_usuarios()
        self.usuario_atual = ctk.StringVar()
        self.usuario_atual.set("Sistema")

        self.title("Alterar senha")
        self.geometry("400x400")

        self.transient(master)
        self.update_idletasks()
        self.grab_set()   

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0,1), weight=1)
        header =  ctk.CTkFrame(self, fg_color="#1e1e1e")
        entrys =  ctk.CTkFrame(self, fg_color="#1e1e1e")

        header.grid(row=0, column=0)
        header.rowconfigure(0, weight=1)

        entrys.rowconfigure((0,1), weight=1)
        entrys.columnconfigure(0, weight=1)
        entrys.grid(row=1, column=0, sticky="nsew")

        ctk.CTkLabel(header, 
                    text="Escolha um usuario e digite a nova senha",
                    width=300,
                    wraplength=300,
                    font=("arial", 32, "bold")
                    ).grid(row=0, column=0)
        
        ctk.CTkComboBox(entrys,
                        values=usuarios,
                        variable=self.usuario_atual,
                        font=("arial", 32, "bold"),
                        command=self.mudar_usuario,
                        width=200
                        ).grid(row=0, column=0)
        
        entry = ctk.CTkEntry(entrys,    
                        textvariable=senha,
                        font=("Arial", 20, "bold"),
                        width=400,
                        height=50)
        entry.grid(row=1, column=0)
        entry.after(1000, entry.focus_set)

        entry.bind("<Escape>", lambda e: self.destroy())
        entry.bind("<Return>", lambda e: self.alterar(self.usuario_atual.get(), senha.get()))
        
    def mudar_usuario(self, usuario):
        self.usuario_atual.set(usuario)

    def alterar(self, usuario, senha):
        resultado = self.main.usuario.alterar_senha(usuario, senha)

        if resultado.sucesso:
            messagebox.showinfo("Sucesso", resultado.mensagem)
            self.destroy()
            return

        messagebox.showerror("Erro", resultado.mensagem)
        return

class ModalCadastrarUsuario(ctk.CTkToplevel):
    def __init__(self, master, main):
        self.main = main
        super().__init__(master=master, fg_color="#1e1e1e")

        senha = StringVar()
        usuario = StringVar()
        self.cargo_atual = StringVar()
        self.cargo_atual.set("funcionario")
        cargos = ["funcionario", "admin"]

        self.title("Cadastrar usuario")
        self.geometry("500x500")

        self.transient(master)
        self.update_idletasks()
        self.grab_set()   

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0,1), weight=1)
        header =  ctk.CTkFrame(self, fg_color="#1e1e1e")
        entrys =  ctk.CTkFrame(self, fg_color="#1e1e1e")

        header.grid(row=0, column=0)
        header.rowconfigure(0, weight=1)

        entrys.rowconfigure((0,1,2,3,4), weight=1)
        entrys.columnconfigure(0, weight=1)
        entrys.grid(row=1, column=0, sticky="nsew")

        ctk.CTkLabel(header, 
                    text="Digite o nome e a senha do usuario",
                    width=300,
                    wraplength=300,
                    font=("arial", 32, "bold")
                    ).grid(row=0, column=0)

        ctk.CTkComboBox(entrys,
                values=cargos,
                variable=self.cargo_atual,
                font=("arial", 32, "bold"),
                command=self.mudar_cargo,
                width=300
                ).grid(row=0, column=0)

        ctk.CTkLabel(entrys, 
                    text="Nome",
                    width=300,
                    wraplength=300,
                    font=("arial", 32, "bold")
                    ).grid(row=1, column=0, sticky="s")
                
        entry_nome = ctk.CTkEntry(entrys,    
                        textvariable=usuario,
                        font=("Arial", 20, "bold"),
                        width=400,
                        height=50)
        entry_nome.grid(row=2, column=0, sticky="n")

        ctk.CTkLabel(entrys, 
                    text="Senha",
                    width=300,
                    wraplength=300,
                    font=("arial", 32, "bold")
                    ).grid(row=3, column=0, sticky="s")
        
        entry_senha = ctk.CTkEntry(entrys,    
                        textvariable=senha,
                        font=("Arial", 20, "bold"),
                        width=400,
                        height=50)
        entry_senha.grid(row=4, column=0)

        self.after(1000, entry_nome.focus_set)
        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Return>", lambda e: self.cadastrar(usuario.get(), senha.get(), self.cargo_atual.get()))
    
    def mudar_cargo(self, valor):
        self.cargo_atual.set(valor)

    def cadastrar(self, usuario, senha, cargo):
        resultado = self.main.usuario.cadastrar_usuario(usuario, senha, cargo)

        if resultado.sucesso:
            messagebox.showinfo("Sucesso", resultado.mensagem)
            self.destroy()
            return

        messagebox.showerror("Erro", resultado.mensagem)
        return

class ListarUsuarios(ctk.CTkToplevel):
    def __init__(self, master, main):
        self.main = main
        self.usuario_selecionado = None
        self.linhas = {}

        super().__init__(master=master, fg_color="#1e1e1e")

        self.title("Usuários cadastrados")
        self.geometry("300x400")
        self.transient(master)
        self.update_idletasks()
        self.grab_set()

        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Delete>", lambda e: self._excluir_selecionado())

        self.frame = ctk.CTkFrame(self, fg_color="#1e1e1e")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.tabela = ctk.CTkScrollableFrame(self.frame)
        self.tabela.pack(fill="both", expand=True)

        self.btn_excluir = ctk.CTkButton(
            self.frame,
            text="Excluir selecionado",
            fg_color="#b00020",
            hover_color="#8e001a",
            command=self._excluir_selecionado
        )
        self.btn_excluir.pack(pady=10)

        self._criar_tabela()

    def _criar_tabela(self):
        usuarios = self.main.usuario.listar_usuarios()

        headers = ["Usuário", "Cargo"]
        for col, texto in enumerate(headers):
            ctk.CTkLabel(
                self.tabela,
                text=texto,
                font=("Arial", 16, "bold")
            ).grid(row=0, column=col, padx=15, pady=(0, 10))

        for row, (usuario, cargo) in enumerate(usuarios, start=1):
            lbl_usuario = ctk.CTkLabel(
                self.tabela,
                text=usuario,
                font=("Arial", 14)
            )
            lbl_usuario.grid(row=row, column=0, padx=15, pady=5, sticky="w")

            lbl_cargo = ctk.CTkLabel(
                self.tabela,
                text=cargo,
                font=("Arial", 14)
            )
            lbl_cargo.grid(row=row, column=1, padx=15, pady=5, sticky="w")

            for widget in (lbl_usuario, lbl_cargo):
                widget.bind(
                    "<Button-1>",
                    lambda e, u=usuario: self._selecionar_usuario(u)
                )

            self.linhas[usuario] = (lbl_usuario, lbl_cargo)

    def _selecionar_usuario(self, usuario):
        for labels in self.linhas.values():
            for lbl in labels:
                lbl.configure(text_color="white")

        for lbl in self.linhas[usuario]:
            lbl.configure(text_color="#00bcd4")

        self.usuario_selecionado = usuario

    def _excluir_selecionado(self):
        if not self.usuario_selecionado:
            messagebox.showwarning(
                "Aviso",
                "Nenhum usuário selecionado."
            )
            return
        
        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Tem certeza que deseja excluir o usuário '{self.usuario_selecionado}'?"
        )

        if not confirmar:
            return

        resultado = self.main.usuario.excluir_usuario(self.usuario_selecionado)

        if not resultado.sucesso:
            messagebox.showerror("Erro", resultado.mensagem)
            return

        messagebox.showinfo("Sucesso", resultado.mensagem)
        self._atualizar()

    def _atualizar(self):
        for widget in self.tabela.winfo_children():
            widget.destroy()

        self.usuario_selecionado = None
        self.linhas.clear()
        self._criar_tabela()

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

        #texto
        self.status = StringVar()
        
        #ajustando coluna para centralizar interface
        self.columnconfigure((0,1), weight=1)
        self.rowconfigure(2, weight=1)

        self.master.bind("<Escape>", lambda e: self.escolher(6))

        #frame pra menubar
        header_menubar = ctk.CTkFrame(self, fg_color="#313030")
        header_menubar.grid(row=0, column=0, sticky="w")
        header_menubar.columnconfigure((0,1,2), weight=1)

        botoes_frame = ctk.CTkFrame(self, fg_color="#1e1e1e", height=520)
        botoes_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="nsew"
        )
        botoes_frame.columnconfigure((0, 1), weight=1)

        for i in range(3):
            botoes_frame.rowconfigure(i, weight=1)

        botoes_frame.columnconfigure((0,1), weight=1)
        botoes_frame.grid_propagate(False)

        #botao configurações
        ctk.CTkButton(header_menubar, 
                    text="Configurações",
                    text_color="white", 
                    hover_color="gray",
                    width=50,  
                    height=30,
                    font=("arial", 22, "bold"),
                    fg_color="#313030",
                    command=self.main.abrir_configs
                    ).grid(column=0, row=0, padx=50, pady=20, sticky="ns")
        
        #botao admin
        self.botao_admin = ctk.CTkButton(header_menubar, 
                    text="Admin",
                    text_color="white", 
                    hover_color="gray",
                    width=50,  
                    height=30,
                    font=("arial", 22, "bold"),
                    fg_color="#313030",
                    command=lambda: self.abrir_submenu(self.submenu_admin, self.botao_admin)
                    )
        self.botao_admin.grid(column=1, row=0, padx=50, pady=20, sticky="ns")
        
        #submenu
        self.submenu_admin = ctk.CTkFrame(
            self,
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
            width=180,
            command=lambda: ModalCadastrarUsuario(self.master, self.main)
        ).pack(padx=10, pady=5)

        #submenu botao alterar senha
        ctk.CTkButton(
            self.submenu_admin,
            text="Alterar senha",
            fg_color="#313030",
            hover_color="gray",
            font=("Arial", 16),
            width=180,
            command=lambda: ModalAlterarSenha(self.master, self.main)
        ).pack(padx=10, pady=5)

        #submenu botao listar usuarios
        ctk.CTkButton(
            self.submenu_admin,
            text="Ver funcionarios",
            fg_color="#313030",
            hover_color="gray",
            font=("Arial", 16),
            width=180,
            command=lambda: ListarUsuarios(self.master, self.main)
        ).pack(padx=10, pady=5)
        
        #botao ajuda
        self.botao_ajuda = ctk.CTkButton(header_menubar, 
                    text="Ajuda",
                    text_color="white", 
                    hover_color="gray",
                    width=50,  
                    height=30,
                    font=("arial", 22, "bold"),
                    fg_color="#313030",
                    command=lambda: self.abrir_submenu(self.submenu_ajuda, self.botao_ajuda)
                    )
        self.botao_ajuda.grid(column=2, row=0, padx=50, pady=20, sticky="ns")
        
        self.submenu_ajuda = ctk.CTkFrame(
            self,
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

        logo_frame = ctk.CTkFrame(self, fg_color="#1e1e1e", height=420)
        logo_frame.grid(row=1, column=0, columnspan=2, pady=30)
        logo_frame.grid_propagate(False)

        #Imagem para usar no label principal
        try:
            self.logo_img = ctk.CTkImage(
                light_image=Image.open("images/Adega_fundo_cinza.png"),
                size=(300, 300)
            )

            #label menu imagem
            ctk.CTkLabel(
            logo_frame, 
            text="",
            image=self.logo_img,
            fg_color="#1e1e1e"
            ).pack(pady=(10, 20))

        except (FileNotFoundError, UnidentifiedImageError, OSError) as e:
            logger.error("Erro ao carregar logo | erro=%s", e)

            ctk.CTkLabel(
            logo_frame, 
            text="",
            fg_color="#1e1e1e"
            ).pack(pady=(10, 20))

        #label status
        ctk.CTkLabel(
            self,
            textvariable=self.status,
            font=("Arial", 24, "bold"),
            text_color="red"
            ).grid(column=0, row=5, columnspan=2, sticky="ew", padx=20, pady=20)
     
        #botao caixa
        ctk.CTkButton(
            botoes_frame, 
            text="Caixa",
            text_color="black", 
            corner_radius=40,
            border_color="black",
            hover_color="white",
            border_width=5,
            width=350,  
            height=200,
            font=("Arial", 30, "bold"),
            fg_color="orange",
            command=lambda: self.escolher(1)
            ).grid(column=0, row=0, pady=20,  padx=40, sticky="ns")

        #botao estoque
        ctk.CTkButton(
            botoes_frame, 
            text="Estoque",
            text_color="black", 
            corner_radius=40,
            border_color="black",
            hover_color="white",
            border_width=5,
            width=350,  
            height=200,
            fg_color="orange",
            font=("Arial", 30, "bold"),
            command=lambda: self.escolher(2)
            ).grid(column=0, row=1, pady=20, padx=40, sticky="ns")

        #botao Relatórios
        ctk.CTkButton(
            botoes_frame, 
            text="Relatórios (W.I.P)", 
            text_color="black", 
            corner_radius=40,
            border_color="black",
            hover_color="white",
            border_width=5,
            width=350,  
            height=200,
            fg_color="orange",
            font=("Arial", 30, "bold"),
            command=lambda: self.escolher(5)
            ).grid(column=1, row=0, pady=20,  padx=40, sticky="ns")
        
        #botao despesas
        ctk.CTkButton(
            botoes_frame, 
            text="Despesas", 
            text_color="black", 
            corner_radius=40,
            border_color="black",
            hover_color="white",
            border_width=5,
            width=350,  
            height=200,
            fg_color="orange",
            font=("Arial", 30, "bold"),
            command=lambda: self.escolher(4)
            ).grid(column=1, row=1, pady=20, sticky="ns", padx=40)
        
        #botao cadastro
        ctk.CTkButton(
            botoes_frame, 
            text="Cadastro", 
            text_color="black", 
            corner_radius=40,
            border_color="black",
            hover_color="white",
            border_width=5,
            width=350,  
            height=200,
            fg_color="orange",
            font=("Arial", 30, "bold"),
            command=lambda: self.escolher(3)
            ).grid(column=0, row=2, pady=20, sticky="ns", padx=40)

        #botao sair
        ctk.CTkButton(
            botoes_frame, 
            text="Sair", 
            text_color="black", 
            corner_radius=40,
            border_color="black",
            hover_color="red",
            border_width=5,
            width=350,  
            height=200,
            fg_color="orange",
            font=("Arial", 30, "bold"),
            command=lambda: self.escolher(6)
            ).grid(column=1, row=2, pady=20, sticky="ns", padx=40)

        estoque_baixo = self.main.estoque.estoque_baixo(self.main.configs.get("Quantidade_aviso", 4))
        
        if estoque_baixo:
            PopupBaixoEstoque(self, estoque_baixo, self.main.configs)
            logger.info("Produtos com estoque baixo produtos=%s", estoque_baixo)

    def abrir_submenu(self, submenu, botao):
        self.main.pode_usar_atalho = False

        # se não tem nenhum submenu aberto
        if self.submenu_aberto is None:
            self._posicionar_submenu(submenu, botao)
            self.submenu_aberto = submenu
            return

        # se clicou no mesmo submenu → fecha
        if self.submenu_aberto == submenu:
            submenu.place_forget()
            self.submenu_aberto = None
            self.main.pode_usar_atalho = True
            return

        # se clicou em outro submenu → troca
        self.submenu_aberto.place_forget()
        self._posicionar_submenu(submenu, botao)
        self.submenu_aberto = submenu

    def _posicionar_submenu(self, submenu, botao):
        OFFSET_Y = 18 
        OFFSET_X = -50 

        x = (
            botao.winfo_rootx()
            - self.master.winfo_rootx()
            + OFFSET_X
        )

        y = (
            botao.winfo_rooty()
            - self.master.winfo_rooty()
            + botao.winfo_height()
            + OFFSET_Y
        )

        submenu.place(x=x, y=y)

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

        if opcao == 6:
            self.main.fechar_app()
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
                text=f"Produto '{nome}' com estoque baixo | Quantidade: {quantidade}",
                text_color="red",
                justify="left",
                wraplength=400
            ).pack(padx=10)


            if i >= 3:
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
    def __init__(self, master, main, on_close=None):
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
        self.on_close = on_close
        self.config = self.main.configs


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

        if self.on_close:
            self.on_close()

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
#root.state("zoomed") #para windows

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

logger = logging.getLogger(__name__)

logging.basicConfig(filename="logs", level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s - %(message)s")

m = Main(root) #Instanciando a main

root.mainloop() #Loop de eventos do customtkinter
