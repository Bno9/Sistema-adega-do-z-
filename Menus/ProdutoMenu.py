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
            self.mapa_telas = {1: self.tela_cadastro,
                               2: self.tela_editar,
                               3: self.tela_excluir,
                               4: self.voltar}
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

            menu_tela = ctk.CTkFrame(self.frame_conteudo, fg_color="#1e1e1e")
            menu_tela.grid(row=0, column=0, sticky="nsew")
            menu_tela.rowconfigure((0,1,2,3,4), weight=1)
            menu_tela.columnconfigure(0, weight=1)

            buttons = [("Cadastrar Produto", 1),
                       ("Editar produto", 2),
                       ("Excluir produto", 3),
                       ("Voltar", 4)]
            
            #label principal
            ctk.CTkLabel(menu_tela, 
                      text="""Menu de cadastro de produtos""", 
                      text_color="white",
                      fg_color="#1e1e1e",
                      font=("arial", 26, "bold")
                      ).grid(column=0, row=0, pady=20)
            
            #botoes de escolha
            for i, (texto, comando) in enumerate(buttons, start=1):
                ctk.CTkButton(menu_tela, 
                        text=texto, 
                        text_color="black", 
                        corner_radius=40,
                        border_color="black",
                        hover_color="white",
                        border_width=5,
                        width=300,  
                        height=200,
                        font=("Arial", 30, "bold"),
                        fg_color="orange",
                        command=lambda c=comando: self.escolha_tela(c)
                        ).grid(column=0, row=i, pady=20)
                
            self.master.bind("<Escape>", lambda e: self.voltar())

        def escolha_tela(self, escolha):
            try:
                escolha = int(escolha)
            except ValueError:
                raise ValueError("Valor recebido inválido")
            
            escolhido = self.mapa_telas.get(escolha, self.referencia_main.voltar_menu_principal)
            self.pode_usar_atalho = False

            self.limpar_tela()
            self.unbind("<Escape>")

            escolhido()

        def tela_cadastro(self):
            self.codigo_cadastro = StringVar()
            self.nome_cadastro = StringVar()
            self.preco_custo_cadastro = StringVar()
            self.preco_venda_cadastro = StringVar()
            self.quantidade_cadastro = StringVar()
            self.status_cadastro = StringVar()

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
            form_frame.rowconfigure((0,1,2,3,4,5), weight=1)

            botao_frame = ctk.CTkFrame(cadastro_tela, fg_color="#1e1e1e")
            botao_frame.grid(row=2, column=0, sticky="nsew")
            botao_frame.columnconfigure((0,1,2,3), weight=1)
            botao_frame.rowconfigure(0, weight=1)


            campos = [("Código", self.codigo_cadastro),
                ("Nome", self.nome_cadastro),
                ("Preço custo", self.preco_custo_cadastro),
                ("Preço venda", self.preco_venda_cadastro),
                ("Quantidade", self.quantidade_cadastro)]

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
                      textvariable=self.status_cadastro, 
                      text_color="red",
                        fg_color="#1e1e1e",
                        font=("arial", 32, "bold")
                      ).grid(column=0, row=1, pady=10)

            #labels/entrys
            for i, (texto, variavel) in enumerate(campos):
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

            #teclas para mudar campo
            for i, entry in enumerate(self.entries):
                entry.bind("<Return>", lambda e, idx=i: self.proximo_campo(idx)) #enter
                entry.bind("<Down>", lambda e, idx=i: self.proximo_campo(idx)) #seta pra baixo
                entry.bind("<Up>", lambda e, idx=i: self.campo_anterior(idx)) #seta pra cima
                entry.bind("<Escape>", lambda e, idx=i: self.menu())

            #botao cadastrar
            ctk.CTkButton(botao_frame,
                       text="Cadastrar", 
                        text_color="black", 
                        corner_radius=40,
                        border_color="black",
                        hover_color="white",
                        border_width=5,
                        width=300,  
                        height=200,
                        font=("Arial", 30, "bold"),
                        fg_color="orange",
                       command=self.controller.criar
                       ).grid(column=1, row=0)
            
            #botao voltar
            ctk.CTkButton(botao_frame,  
                       text="Voltar", 
                        text_color="black", 
                        corner_radius=40,
                        border_color="black",
                        hover_color="white",
                        border_width=5,
                        width=300,  
                        height=200,
                        font=("Arial", 30, "bold"),
                        fg_color="orange",
                       command=self.menu
                       ).grid(column=2, row=0)

            self.entries[0].focus_set()

        def tela_editar(self):
            self.codigo_edit = StringVar()
            self.nome_edit = StringVar()
            self.preco_custo_edit = StringVar()
            self.preco_venda_edit = StringVar()
            self.quantidade_edit = StringVar()
            self.novo_valor = StringVar()
            self.status_edit = StringVar()

            #frame tela editar
            frame = ctk.CTkFrame(self.frame_conteudo, fg_color="#1e1e1e")
            frame.grid(column=0, row=0)
            frame.columnconfigure((0,1), weight=1)
            frame.rowconfigure((0,1,2,3), weight=1)
            
            #label principal
            ctk.CTkLabel(frame,
                    text="Digite o código do produto", 
                     text_color="white",
                    fg_color="#1e1e1e",
                    font=("arial", 30, "bold")
                    ).grid(column=0, row=0, columnspan=2, pady=20)

            #label status
            ctk.CTkLabel(frame, 
                      width=30, 
                      textvariable=self.status_edit,
                      font=("Arial", 24, "bold"),
                      text_color="red"
                      ).grid(row=2, column=0, columnspan=2, pady=20)

            #entry código
            entry_codigo = ctk.CTkEntry(frame, 
                      width=300,
                      font=("Arial", 20, "bold"),
                      textvariable=self.codigo_edit
                      )
            entry_codigo.grid(column=0, row=1, columnspan=2, pady=20)
            entry_codigo.focus_set()
            entry_codigo.bind("<Escape>", lambda e: self.menu())
            entry_codigo.bind("<Return>", lambda e: self.editar())

            #botao editar
            ctk.CTkButton(frame,  
                       text="Editar", 
                        text_color="black", 
                        corner_radius=40,
                        border_color="black",
                        hover_color="white",
                        border_width=5,
                        width=300,  
                        height=200,
                        font=("Arial", 30, "bold"),
                        fg_color="orange",
                       command=self.editar
                       ).grid(column=0, row=3, pady=20)

            #botao voltar
            ctk.CTkButton(frame, 
                       text="Voltar", 
                        text_color="black", 
                        corner_radius=40,
                        border_color="black",
                        hover_color="white",
                        border_width=5,
                        width=300,  
                        height=200,
                        font=("Arial", 30, "bold"),
                        fg_color="orange",
                       command=self.menu
                       ).grid(column=1, row=3, pady=20)
            
        def editar(self):
            """Recebe o valor e altera o atributo do produto"""

            try:
                codigo_produto = int(self.codigo_edit.get())
            except ValueError:
                self.status_edit.set("Digite apenas numeros")

            if not self.referencia_main.estoque.conferir_se_existe_no_estoque(codigo_produto):
                self.status_edit.set("Produto não encontrado")
                return

            self.produto = self.referencia_main.estoque.get_produto(codigo_produto)
 
            self.limpar_tela()

            mapa = [
                (1, "codigo"),
                (2, "nome"),
                (3, "preco_custo"),
                (4, "preco_venda"),
                (5, "quantidade")
            ]

            frame = ctk.CTkFrame(self.frame_conteudo, fg_color="#1e1e1e")
            frame.rowconfigure((0,1,2,3,4,5,6,7), weight=1)
            frame.columnconfigure(0, weight=1)
            frame.grid(row=0, column=0, sticky="nsew")

            #label escolha
            ctk.CTkLabel(frame, 
                         text="""Escolha o que deseja alterar""",
                         text_color="white",
                            fg_color="#1e1e1e",
                            font=("arial", 24, "bold")
            ).grid(column=0, row=0, sticky="ew")
            
            #botões de escolha
            for i, (opcao, texto) in enumerate(mapa, start=2):
                ctk.CTkButton(frame, 
                              text=texto, 
                              text_color="black", 
                                corner_radius=40,
                                border_color="black",
                                hover_color="white",
                                border_width=5,
                                width=600,  
                                height=300,
                                font=("Arial", 30, "bold"),
                                fg_color="orange",
                              command=lambda c=opcao: self.processar_escolha(c, self.novo_valor)
                              ).grid(column=0, row=i, pady=20)
         
            #botao cancelar
            ctk.CTkButton(frame,
                       text="Cancelar",
                       text_color="black", 
                        corner_radius=40,
                        border_color="black",
                        hover_color="white",
                        border_width=5,
                        width=600,  
                        height=300,
                        font=("Arial", 30, "bold"),
                        fg_color="orange",
                       command=self.menu).grid(column=0, row=6, pady=20)        
            
        def processar_escolha(self, escolha, novo_valor):
            mapa = {
                1: "codigo",
                2: "nome",
                3: "preco_custo",
                4: "preco_venda",
                5: "quantidade"
            }

            if escolha not in mapa:
                self.status_edit.set("Escolha inválida")
                return

            self.atributo = mapa[escolha]

            self.limpar_tela()

            frame = ctk.CTkFrame(self.frame_conteudo, fg_color="#1e1e1e")
            frame.rowconfigure((0,1,2,3), weight=1)
            frame.columnconfigure((0,1,2,3), weight=1)
            frame.grid(row=0, column=0, sticky="nsew")

            #label novo valor
            ctk.CTkLabel(frame, 
                      text="Digite o novo valor",
                      text_color="white",
                        fg_color="#1e1e1e",
                        font=("arial", 36, "bold")
                      ).grid(column=1, row=0, columnspan=2)
            
            #label status
            ctk.CTkLabel(frame, 
                      textvariable=self.status_edit,
                      font=("Arial", 24, "bold"),
                        text_color="red"
                      ).grid(column=1, row=3, columnspan=2)
            
            #entry novo valor
            entry_foco = ctk.CTkEntry(frame, 
                      textvariable=novo_valor,
                      width=300,
                        font=("Arial", 20, "bold")
                      )
            entry_foco.grid(column=1, row=1, columnspan=2)
            entry_foco.focus_set()
            entry_foco.bind("<Escape>", lambda e: self.menu())
            entry_foco.bind("<Return>", lambda e: self.controller.salvar_alteracao())
            
            #botao salvar
            ctk.CTkButton(frame,
                    text="Salvar", 
                    command=self.controller.salvar_alteracao,
                    text_color="black", 
                    corner_radius=40,
                    border_color="black",
                    hover_color="white",
                    border_width=5,
                    width=300,  
                    height=200,
                    font=("Arial", 30, "bold"),
                    fg_color="orange",
                    ).grid(column=1, row=2)
            
            #botao cancelar
            ctk.CTkButton(frame, 
                       text="Cancelar", 
                       command=self.menu,
                       text_color="black", 
                        corner_radius=40,
                        border_color="black",
                        hover_color="white",
                        border_width=5,
                        width=300,  
                        height=200,
                        font=("Arial", 30, "bold"),
                        fg_color="orange",
                       ).grid(column=2, row=2)


        def tela_excluir(self):
            self.codigo_excluir = StringVar()
            self.status_excluir = StringVar()

            #frame tela excluir
            frame = ctk.CTkFrame(self.frame_conteudo, fg_color="#1e1e1e")
            frame.grid(column=0, row=0, pady=40)
            frame.columnconfigure((0,1), weight=1)
            frame.rowconfigure((0,1,2,3), weight=1)

            #label principal
            ctk.CTkLabel(frame, 
                      text="Digite o código do produto que deseja remover",
                      text_color="white",
                        fg_color="#1e1e1e",
                        font=("arial", 32, "bold")
                        ).grid(column=0, row=0, columnspan=2, pady=20)
            
            #label status
            ctk.CTkLabel(frame, 
                      textvariable=self.status_excluir,
                      font=("Arial", 24, "bold"),
                      text_color="red"
                      ).grid(column=0, row=3, columnspan=2, pady=20)

            #entry codigo
            entry_codigo = ctk.CTkEntry(frame,  
                      textvariable=self.codigo_excluir,
                      width=300,
                      font=("Arial", 20, "bold")
                      )
            
            entry_codigo.grid(column=0, row=1, columnspan=2, pady=20)
            entry_codigo.focus_set()
            entry_codigo.bind("<Escape>", lambda e: self.menu())
            entry_codigo.bind("<Return>", lambda e: self.controller.deletar())
            
            #botao enviar
            ctk.CTkButton(frame, 
                       text="Enviar", 
                       text_color="black", 
                        corner_radius=40,
                        border_color="black",
                        hover_color="white",
                        border_width=5,
                        width=300,  
                        height=200,
                        font=("Arial", 30, "bold"),
                        fg_color="orange",
                       command=self.controller.deletar
                       ).grid(column=0, row=2, pady=20)

            #botao voltar
            ctk.CTkButton(frame, 
                       text="Voltar", 
                      text_color="black", 
                        corner_radius=40,
                        border_color="black",
                        hover_color="white",
                        border_width=5,
                        width=300,  
                        height=200,
                        font=("Arial", 30, "bold"),
                        fg_color="orange",
                       command=self.menu
                       ).grid(column=1, row=2, pady=20)

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
                    self.criar()
                    self.entries[0].focus_set()

        def campo_anterior(self, indice):
            "Muda o foco do entry pro anterior"
            if indice - 1 >= 0:
                self.entries[indice - 1].focus_set()


        def teclas_menu(self, tecla):
            if tecla.char in ["1", "2", "3", "4"] and self.pode_usar_atalho:
                self.escolha_tela(int(tecla.char))

class ProdutoController:
    def __init__(self, tela, ref_estoque):
        self.tela = tela
        self.ref_estoque = ref_estoque

    
    def criar(self):
        """Recebe as entradas e envia para a classe estoque criar e salvar o produto"""
        try:
            codigo = int(self.tela.codigo_cadastro.get())
            nome = self.tela.nome_cadastro.get()
            preco_custo = float(self.tela.preco_custo_cadastro.get())
            preco_venda = float(self.tela.preco_venda_cadastro.get())
            quantidade = int(self.tela.quantidade_cadastro.get())
                
        except ValueError:
            self.tela.status_cadastro.set("Digite apenas numeros")
            return
        
        resultado = self.ref_estoque.criar_produto(codigo,nome,preco_custo,preco_venda,quantidade)
    
        self.tela.status_cadastro.set(resultado)

    def salvar_alteracao(self):
        valor = self.tela.novo_valor.get()
                                                                           #eu poderia desempacotar o valor pra ficar mais facil, mas preferi deixar o indice mesmo
        self.tela.status_edit.set(self.ref_estoque.atualizar_produto(self.tela.produto[1], self.tela.atributo, valor))
        
    def deletar(self):
        try:
            codigo = int(self.tela.codigo_excluir.get())
            self.tela.status_excluir.set(self.ref_estoque.remover_produto(codigo))
        except ValueError:
            self.tela.status_excluir.set("Digite apenas numeros")
            return