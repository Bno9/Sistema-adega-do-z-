from tkinter import ttk
from tkinter import *

import customtkinter as ctk

class ProdutoMenu(ctk.CTkFrame):

        def __init__(self, root, referencia_main):
            super().__init__(master=root, fg_color="#1e1e1e")
            self.referencia_main = referencia_main

            #textos
            self.status = StringVar()

            #entradas
            self.codigo = StringVar()
            self.nome = StringVar()
            self.preco_custo = StringVar()
            self.preco_venda = StringVar()
            self.quantidade = StringVar()
            self.novo_valor = StringVar()
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
            self.frame_conteudo.rowconfigure((0,1,2,3,4,5,6), weight=1)

            self.menu()

        #telas

        def menu(self):
            self.limpar_tela()
            self.pode_usar_atalho = True

            buttons = [("Cadastrar produto", 1),
                       ("Editar produto", 2),
                       ("Excluir produto", 3),
                       ("Voltar", 4)]
            
            #label principal
            ctk.CTkLabel(self.frame_conteudo, 
                      text="""Menu de cadastro de produtos""", 
                      text_color="white",
                      fg_color="#1e1e1e",
                      font=("arial", 26, "bold")
                      ).grid(column=0, row=0, columnspan=2, pady=20)
            
            #label status
            ctk.CTkLabel(self.frame_conteudo, 
                      textvariable=self.status,
                      font=("Arial", 24, "bold"),
                      text_color="red"
                      ).grid(column=0, row=6, pady=20)
            
            #botoes de escolha
            for i, (texto, comando) in enumerate(buttons, start=2):
                ctk.CTkButton(self.frame_conteudo, 
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
                self.status.set("Digite apenas numeros")
                return
            
            escolhido = self.mapa_telas.get(escolha, "Escolha uma das opções disponiveis")
            self.pode_usar_atalho = False

            self.limpar_tela()

            escolhido()

        def tela_cadastro(self):
            self.unbind("<Escape>")

            #frame para tela de cadastro
            form_frame = ctk.CTkFrame(self.frame_conteudo, fg_color="#1e1e1e")
            form_frame.grid(row=0, column=0, sticky="n", pady=30)
            form_frame.columnconfigure(0, weight=1)
            form_frame.columnconfigure(1, weight=2)
            for i in range(15):
                form_frame.rowconfigure(i, weight=1)

            campos = [("Código", self.codigo),
                ("Nome", self.nome),
                ("Preço custo", self.preco_custo),
                ("Preço venda", self.preco_venda),
                ("Quantidade", self.quantidade)]

            self.entries.clear()

            #label principal
            ctk.CTkLabel(form_frame, 
                        text="Digite as informações do produto", 
                        text_color="white",
                        fg_color="#1e1e1e",
                        font=("arial", 24, "bold")
                      ).grid(column=0, row=0, columnspan=2, pady=20)

            
            #labels/entrys
            for i, (texto, variavel) in enumerate(campos, start=2):
                ctk.CTkLabel(form_frame, 
                            text=texto, 
                            text_color="white",
                            fg_color="#1e1e1e",
                            font=("arial", 32, "bold")
                          ).grid(column=0, row=i, pady=5, padx=10)


                entry = ctk.CTkEntry(form_frame, 
                                  textvariable=variavel, 
                                  width=300,
                                  font=("Arial", 20, "bold"))
                
                entry.grid(row=i, 
                           column=1, 
                           pady=5, 
                           padx=10, 
                           sticky="w")
                    
                self.entries.append(entry)

            #teclas para mudar campo
            for i, entry in enumerate(self.entries):
                entry.bind("<Return>", lambda e, idx=i: self.proximo_campo(idx)) #enter
                entry.bind("<Down>", lambda e, idx=i: self.proximo_campo(idx)) #seta pra baixo
                entry.bind("<Up>", lambda e, idx=i: self.campo_anterior(idx)) #seta pra cima
                entry.bind("<Escape>", lambda e, idx=i: self.menu())

            #label status
            ctk.CTkLabel(form_frame, 
                      textvariable=self.status, 
                      text_color="red",
                        fg_color="#1e1e1e",
                        font=("arial", 32, "bold")
                      ).grid(column=0, row=len(campos)+5, columnspan=2, pady=10)

            #botao cadastrar
            ctk.CTkButton(form_frame,
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
                       command=self.criar
                       ).grid(column=0, row= len(campos)+4, padx=10, pady=100)
            
            #botao voltar
            ctk.CTkButton(form_frame,  
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
                       ).grid(column=1, row= len(campos)+4, padx=10, pady=100)

            self.entries[0].focus_set()

        def tela_editar(self):
            self.unbind("<Escape>")

            #frame tela editar
            frame = ctk.CTkFrame(self.frame_conteudo, fg_color="#1e1e1e")
            frame.grid(column=0, row=0, pady=40)
            
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
                      textvariable=self.status,
                      font=("Arial", 24, "bold"),
                      text_color="red"
                      ).grid(row=2, column=0, columnspan=2, pady=20)

            #entry código
            entry_codigo = ctk.CTkEntry(frame, 
                      width=300,
                      font=("Arial", 20, "bold"),
                      textvariable=self.codigo
                      )
            entry_codigo.grid(column=0, row=1, columnspan=2, pady=20)
            entry_codigo.focus_set()
            entry_codigo.bind("<Escape>", lambda e: self.menu())
            entry_codigo.bind("<Return>", lambda e: self.editar())

            #botao editar
            ctk.CTkButton(frame,  
                       text="Editar Produto", 
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
                       ).grid(column=0, row= 3, pady=20)

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
                       ).grid(column=1, row= 3, pady=20)


        def tela_excluir(self):
            self.unbind("<Escape>")

            #frame tela excluir
            frame = ctk.CTkFrame(self.frame_conteudo, fg_color="#1e1e1e")
            frame.grid(column=0, row=0, pady=40)

            #label principal
            ctk.CTkLabel(frame, 
                      text="Digite o código do produto que deseja remover",
                      text_color="white",
                        fg_color="#1e1e1e",
                        font=("arial", 32, "bold")
                        ).grid(column=0, row=0, columnspan=2, pady=20)
            
            #label status
            ctk.CTkLabel(frame, 
                      textvariable=self.status,
                      font=("Arial", 24, "bold"),
                      text_color="red"
                      ).grid(column=0, row=4, columnspan=2, pady=20)

            #entry codigo
            entry_codigo = ctk.CTkEntry(frame,  
                      textvariable=self.codigo,
                      width=300,
                      font=("Arial", 20, "bold")
                      )
            
            entry_codigo.grid(column=0, row=1, columnspan=2, pady=20)
            entry_codigo.focus_set()
            entry_codigo.bind("<Escape>", lambda e: self.menu())
            entry_codigo.bind("<Return>", lambda e: self.deletar())
            
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
                       command=self.deletar
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


        #métodos
 
        def criar(self):
                """Recebe as entradas e envia para a classe estoque criar e salvar o produto"""
                self.unbind("<Escape>")
                try:
                    codigo = int(self.codigo.get())
                    nome = self.nome.get()
                    preco_custo = float(self.preco_custo.get())
                    preco_venda = float(self.preco_venda.get())
                    quantidade = int(self.quantidade.get())
                
                except ValueError:
                    self.status.set("Digite apenas numeros")
                    return
        
                resultado = self.referencia_main.estoque.criar_produto(codigo,nome,preco_custo,preco_venda,quantidade)

                self.status.set(resultado)

                self.frame_conteudo.after(2000, self.limpar_campos)

        def editar(self):
            """Recebe o valor e altera o atributo do produto"""

            self.unbind("<Escape>")

            try:
                codigo_produto = int(self.codigo.get())
            except ValueError:
                self.status.set("Digite apenas numeros")

            if not self.referencia_main.estoque.conferir_se_existe_no_estoque(codigo_produto):
                self.status.set("Produto não encontrado")
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

            #label escolha
            ctk.CTkLabel(self.frame_conteudo, 
                         text="""Escolha o que deseja alterar""",
                         text_color="white",
                            fg_color="#1e1e1e",
                            font=("arial", 24, "bold")
            ).grid(column=0, row=0, sticky="ew")
            
            #botões de escolha
            for i, (opcao, texto) in enumerate(mapa, start=2):
                ctk.CTkButton(self.frame_conteudo, 
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
                              command=lambda c=opcao: self.processar_escolha(c)
                              ).grid(column=0, row=i, pady=20)
         
            #botao cancelar
            ctk.CTkButton(self.frame_conteudo,
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
                       command=self.menu).grid(column=0, row=len(mapa)+1, pady=20)

        def processar_escolha(self, opcao):
            mapa = {
                1: "codigo",
                2: "nome",
                3: "preco_custo",
                4: "preco_venda",
                5: "quantidade"
            }

            escolha = opcao

            if escolha not in mapa:
                self.status.set("Escolha inválida")
                return

            self.atributo = mapa[escolha]

            self.limpar_tela()
            self.limpar_campos()
            

            #label novo valor
            ctk.CTkLabel(self.frame_conteudo, 
                      text="Digite o novo valor",
                      text_color="white",
                        fg_color="#1e1e1e",
                        font=("arial", 26, "bold")
                      ).grid(column=0, row=0, columnspan=2, pady=20)
            
            #label status
            ctk.CTkLabel(self.frame_conteudo, 
                      textvariable=self.status,
                      font=("Arial", 24, "bold"),
                        text_color="red"
                      ).grid(column=0, row=4, columnspan=2, pady=20)
            
            #entry novo valor
            entry_foco = ctk.CTkEntry(self.frame_conteudo, 
                      textvariable=self.novo_valor,
                      width=300,
                        font=("Arial", 20, "bold")
                      )
            entry_foco.grid(column=0, row=1, columnspan=2, pady=20)
            entry_foco.focus_set()
            entry_foco.bind("<Escape>", lambda e: self.menu())
            entry_foco.bind("<Return>", lambda e: self.salvar_alteracao())
            
            #botao salvar
            ctk.CTkButton(self.frame_conteudo,
                    text="Salvar", 
                    command=self.salvar_alteracao,
                    text_color="black", 
                    corner_radius=40,
                    border_color="black",
                    hover_color="white",
                    border_width=5,
                    width=300,  
                    height=200,
                    font=("Arial", 30, "bold"),
                    fg_color="orange",
                    ).grid(column=0, row=2, pady=20)
            
            #botao cancelar
            ctk.CTkButton(self.frame_conteudo, 
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
                       ).grid(column=1, row=2, pady=20)



        def salvar_alteracao(self):
            valor = self.novo_valor.get()
                                                                           #eu poderia desempacotar o valor pra ficar mais facil, mas preferi deixar o indice mesmo
            self.status.set(self.referencia_main.estoque.atualizar_produto(self.produto[1], self.atributo, valor))
        
        def deletar(self):
            try:
                codigo = int(self.codigo.get())
                self.status.set(self.referencia_main.estoque.remover_produto(codigo))
            except ValueError:
                self.status.set("Digite apenas numeros")
                return
            

        
        #métodos tela e campo

        def limpar_tela(self):
            for widget in self.frame_conteudo.winfo_children():
                widget.destroy()
            self.limpar_campos()

        def limpar_campos(self):
            campos = [self.status,
            self.codigo,
            self.nome,
            self.preco_custo,
            self.preco_venda,
            self.quantidade,
            self.novo_valor
            ]

            for var in campos:
                var.set("")

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