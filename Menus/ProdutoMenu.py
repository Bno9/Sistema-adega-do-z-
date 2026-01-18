from tkinter import ttk
from tkinter import *

import customtkinter as ctk

class ProdutoMenu(ctk.CTkFrame):

        def __init__(self, root, referencia_main):
            super().__init__(master=root, fg_color="#1e1e1e")
            self.referencia_main = referencia_main
            self.controller = ProdutoController(self, self.referencia_main.estoque)

            #entradas
            self.entries = []

            #atributos
            self.produto = None
            self.atributo = None
            self.pode_usar_atalho = False

            #frame
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)

            self.frame_conteudo = ctk.CTkFrame(self, fg_color="#1e1e1e")
            self.frame_conteudo.grid(row=0, column=0, sticky="nsew")
            self.frame_conteudo.columnconfigure(0, weight=1)
            self.frame_conteudo.rowconfigure(0, weight=1)

            self.menu()

        #telas

        def menu(self):
            self.limpar_tela()
            self.pode_usar_atalho = True
            self.codigo_entry = StringVar()
            self.status_menu = StringVar()

            menu_tela = ctk.CTkFrame(self.frame_conteudo, fg_color="#1e1e1e")
            menu_tela.grid(row=0, column=0, sticky="nsew")
            menu_tela.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
            menu_tela.columnconfigure(0, weight=1)

            botoes = ctk.CTkFrame(menu_tela, fg_color="#1e1e1e")
            botoes.grid(column=0, row=5)
            botoes.columnconfigure((0,1,2), weight=1)

            buttons = [("""Cadastrar
Produto""", "green", lambda:self.tela_formulario(self.codigo_entry.get(), "cadastro")),
                       ("Editar produto", "white", lambda:self.tela_formulario(self.codigo_entry.get(), "edicao")),
                       ("Excluir produto", "red", lambda:self.controller.deletar(self.codigo_entry.get()))]
            
            #label principal
            ctk.CTkLabel(menu_tela, 
                      text="""Menu de cadastro de produtos""", 
                      text_color="white",
                      fg_color="#1e1e1e",
                      font=("arial", 32, "bold")
                      ).grid(column=0, row=0, pady=20)
            
            #label codigo
            ctk.CTkLabel(menu_tela, 
                      text="""Digite o código do produto e escolha uma opção""", 
                      text_color="white",
                      fg_color="#1e1e1e",
                      font=("arial", 22, "bold")
                      ).grid(column=0, row=2, sticky="s")
            
            #label status
            ctk.CTkLabel(menu_tela, 
                      textvariable=self.status_menu,
                      text_color="red",
                      fg_color="#1e1e1e",
                      font=("arial", 22, "bold")
                      ).grid(column=0, row=4, sticky="n")
            
            #entry do codigo
            ctk.CTkEntry(menu_tela,
                         width=300,
                         height=50,
                         font=("arial", 26, "bold"),
                         textvariable=self.codigo_entry).grid(row=3, column=0)
            
            #botoes de escolha
            for i, (texto, cor, comando) in enumerate(buttons):
                ctk.CTkButton(botoes, 
                        text=texto, 
                        text_color="black", 
                        corner_radius=40,
                        border_color="black",
                        hover_color=cor,
                        border_width=5,
                        width=300,  
                        height=200,
                        font=("Arial", 30, "bold"),
                        fg_color="orange",
                        command=comando
                        ).grid(column=i, row=0, pady=20)

            #botao voltar
            ctk.CTkButton(menu_tela, 
                        text="Voltar", 
                        text_color="black", 
                        corner_radius=40,
                        border_color="black",
                        hover_color="red",
                        border_width=5,
                        width=300,  
                        height=200,
                        font=("Arial", 30, "bold"),
                        fg_color="orange",
                        command=self.voltar
                        ).grid(column=0, row=7)
                
            self.master.bind("<Escape>", lambda e: self.voltar())

        def tela_formulario(self, codigo, modo="cadastro"):
            resultado = self.controller.conferir_codigo(codigo, modo)
            if resultado.get("Status", "Erro") == "Erro":
                self.status_menu.set(resultado.get("Mensagem", "Erro de processamento"))
                return

            self.codigo = ctk.StringVar()
            self.nome = ctk.StringVar()
            self.preco_custo = ctk.StringVar()
            self.preco_venda = ctk.StringVar()
            self.quantidade = ctk.StringVar()

            self.status_formulario = ctk.StringVar()

            self.tipo = "unidade"
            self.qtd_fardo = ctk.StringVar()
            self.referencia_codigo_fardo = ctk.StringVar()

            #frame para tela de cadastro
            cadastro_tela = ctk.CTkFrame(self.frame_conteudo, fg_color="#1e1e1e")
            cadastro_tela.grid(row=0, column=0, sticky="nsew")
            cadastro_tela.columnconfigure(0, weight=1)
            cadastro_tela.rowconfigure((0,1,2), weight=1)

            header = ctk.CTkFrame(cadastro_tela, fg_color="#1e1e1e")
            header.grid(row=0, column=0, sticky="nsew")
            header.columnconfigure(0, weight=1)
            header.rowconfigure(0, weight=1)

            form_frame = ctk.CTkFrame(cadastro_tela, fg_color="#1e1e1e")
            form_frame.grid(row=1, column=0, sticky="nsew")
            form_frame.columnconfigure((0,1), weight=1)
            form_frame.rowconfigure((0,1,2,3,4,5,6), weight=1)

            botao_frame = ctk.CTkFrame(cadastro_tela, fg_color="#1e1e1e")
            botao_frame.grid(row=2, column=0, sticky="nsew")
            botao_frame.columnconfigure((0,1,2,3), weight=1)
            botao_frame.rowconfigure(0, weight=1)

            self.campos = [("Código", self.codigo),
                ("Nome", self.nome),
                ("Preço custo", self.preco_custo),
                ("Preço venda", self.preco_venda),
                ("Quantidade", self.quantidade)]
            
            if modo == "cadastro":
                del self.campos[0]

            self.entries.clear()

            #label principal
            ctk.CTkLabel(header, 
                        text="Digite as informações do produto", 
                        text_color="white",
                        fg_color="#1e1e1e",
                        font=("arial", 24, "bold")
                      ).grid(column=0, row=0)
            

            #label status
            ctk.CTkLabel(header, 
                      textvariable=self.status_formulario, 
                      text_color="red",
                        fg_color="#1e1e1e",
                        font=("arial", 32, "bold")
                      ).grid(column=0, row=1, pady=10)

            #labels/entrys
            for i, (texto, variavel) in enumerate(self.campos, start=1):
                ctk.CTkLabel(form_frame, 
                            text=texto, 
                            text_color="white",
                            fg_color="#1e1e1e",
                            font=("arial", 32, "bold")
                          ).grid(column=1, row=i, pady=5, padx=10, sticky="w")


                entry = ctk.CTkEntry(form_frame, 
                                  textvariable=variavel, 
                                  width=300,
                                  font=("Arial", 20, "bold"))
                
                entry.grid(row=i, 
                           column=0, 
                           pady=5, 
                           padx=10,
                           sticky="e"
                           )
                    
                self.entries.append(entry)

            #checkbox tipo
            combobox_tipo = ctk.CTkComboBox(form_frame,
                                            values=["unidade", "fardo"],
                                            width=310,
                                            height=50,
                                            font=("arial", 32, "bold"),
                                            command=self.controller.mudar_conteudo
                                            )
            combobox_tipo.grid(row=0, column=0, sticky="e")

            #label vazio pra alinhar a combobox
            ctk.CTkLabel(form_frame,
                         text="").grid(row=0, column=1, sticky="w")

            #label dependendo do tipo
            self.label_tipo = ctk.CTkLabel(form_frame, 
                            text="Referencia produto (opcional)", 
                            text_color="white",
                            fg_color="#1e1e1e",
                            font=("arial", 32, "bold")
                          )
            self.label_tipo.grid(column=1, row=6, pady=5, padx=10, sticky="w")

            #entrada dependendo do tipo
            self.entry_tipo = ctk.CTkEntry(form_frame, 
                                  textvariable=self.referencia_codigo_fardo, 
                                  width=300,
                                  font=("Arial", 20, "bold"))
            self.entry_tipo.grid(row=6, column=0, pady=5, padx=10, sticky="e")
            self.entries.append(self.entry_tipo)

            #teclas para mudar campo
            for i, entry in enumerate(self.entries):
                entry.bind("<Return>", lambda e, idx=i: self.proximo_campo(idx)) #enter
                entry.bind("<Down>", lambda e, idx=i: self.proximo_campo(idx)) #seta pra baixo
                entry.bind("<Up>", lambda e, idx=i: self.campo_anterior(idx)) #seta pra cima
                entry.bind("<Escape>", lambda e: self.menu())

            if modo == "cadastro":
                #botao cadastrar
                ctk.CTkButton(botao_frame,
                        text="Cadastrar", 
                            text_color="black", 
                            corner_radius=40,
                            border_color="black",
                            hover_color="green",
                            border_width=5,
                            width=300,  
                            height=200,
                            font=("Arial", 30, "bold"),
                            fg_color="orange",
                        command=lambda: self.controller.criar(self.campos)
                        ).grid(column=1, row=0)
                
            elif modo == "edicao":
                #botao editar
                ctk.CTkButton(botao_frame,
                        text="Editar", 
                            text_color="black", 
                            corner_radius=40,
                            border_color="black",
                            hover_color="green",
                            border_width=5,
                            width=300,  
                            height=200,
                            font=("Arial", 30, "bold"),
                            fg_color="orange",
                        command=lambda: self.controller.editar(self.campos)
                        ).grid(column=1, row=0)
            
            #botao voltar
            ctk.CTkButton(botao_frame,  
                       text="Voltar", 
                        text_color="black", 
                        corner_radius=40,
                        border_color="black",
                        hover_color="red",
                        border_width=5,
                        width=300,  
                        height=200,
                        font=("Arial", 30, "bold"),
                        fg_color="orange",
                       command=self.menu
                       ).grid(column=2, row=0)

            self.entries[0].focus_set()

















            
        def voltar(self):
            self.referencia_main.voltar_menu_principal()

        def limpar_tela(self):
            for widget in self.frame_conteudo.winfo_children():
                widget.destroy()

        def proximo_campo(self, indice):
                """Muda o foco do entry pro proximo"""
                if indice + 1 < len(self.entries):
                    self.entries[indice + 1].focus_set()
                else:
                    self.controller.criar()
                    self.entries[0].focus_set()

        def campo_anterior(self, indice):
            "Muda o foco do entry pro anterior"
            if indice - 1 >= 0:
                self.entries[indice - 1].focus_set()

        def teclas_menu(self, tecla):
            if tecla.char.lower() in ["f1", "f2", "f3"] and self.pode_usar_atalho: #arrumar aqui ainda
                self.escolha_tela(tecla.char)

class ProdutoController:
    def __init__(self, tela, ref_estoque):
        self.tela = tela
        self.ref_estoque = ref_estoque

    
    def criar(self, campos):
        """Recebe as entradas e envia para a classe estoque criar e salvar o produto"""
        try:
            codigo = int(self.tela.codigo_cadastro.get())
            nome = self.tela.nome_cadastro.get()
            preco_custo = float(self.tela.preco_custo_cadastro.get())
            preco_venda = float(self.tela.preco_venda_cadastro.get())
            quantidade = int(self.tela.quantidade_cadastro.get())
            tipo = self.tela.tipo
                
            ref_str = self.tela.referencia_codigo_fardo.get().strip()
            referencia_produto = int(ref_str) if ref_str else None

            qtd_str = self.tela.qtd_fardo.get().strip()
            qtd_fardo = int(qtd_str) if qtd_str else None

        except ValueError:
            self.tela.status_cadastro.set("Digite apenas numeros")
            return
        
        resultado = self.ref_estoque.criar_produto(codigo,nome,tipo,preco_custo,preco_venda,quantidade, referencia_produto, qtd_fardo)
    
        self.tela.status_cadastro.set(resultado)

        for _, var in campos:
            var.set("")

    def editar(self):
        valor = self.tela.novo_valor.get()
                                                                        
        self.tela.status_edit.set(self.ref_estoque.atualizar_produto(self.tela.produto[1], self.tela.atributo, valor))

    def deletar(self, codigo):
        try:
            codigo = int(codigo)
            self.tela.status_menu.set(self.ref_estoque.remover_produto(codigo))
        except ValueError:
            self.tela.status_menu.set("Digite apenas numeros")
            return
        
    def mudar_conteudo(self, valor):
        self.tela.tipo = valor
        if self.tela.tipo == "fardo":
            self.tela.label_tipo.configure(text="Quantidade no fardo")
            self.tela.entry_tipo.configure(textvariable=self.tela.qtd_fardo)
            
        else:
            self.tela.label_tipo.configure(text="Referencia produto (opcional)")
            self.tela.entry_tipo.configure(textvariable=self.tela.referencia_codigo_fardo)
    
    def conferir_codigo(self, codigo, modo):
        if codigo == "":
            return {"Status": "Erro",
                    "Mensagem": "Digite um código"}
        
        try:
            codigo = int(codigo)
        except ValueError:
            return {"Status": "Erro",
                    "Mensagem": "Código precisa ser numero"}

        ja_existe = self.ref_estoque.conferir_se_existe_no_estoque(codigo)

        if ja_existe and modo == "cadastro":
            return {"Status": "Erro",
                    "Mensagem": "Não é possivel cadastrar esse código, pois já existe um produto com o mesmo código"}
        
        if modo == "edicao":
            return {"Status": "Erro",
        "Mensagem": "Não é possivel editar, pois não existe um produto com esse código"}

        return {"Status": "Sucesso"}