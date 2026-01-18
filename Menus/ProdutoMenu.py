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
            self.status_menu = StringVar()

            self.codigo = ctk.StringVar()
            self.codigo.trace("w", self.controller.buscar_produto)
            self.nome = ctk.StringVar()
            self.preco_custo = ctk.IntVar()
            self.preco_custo.trace("w", self.atualizar_margem)
            self.preco_venda = ctk.IntVar()
            self.preco_venda.trace("w", self.atualizar_margem)
            self.quantidade = ctk.StringVar()

            self.margem = StringVar()
            self.tipo = StringVar()
            self.tipo.trace("w", lambda:self.controller.mudar_conteudo(self.tipo.get()))
            self.qtd_fardo = ctk.StringVar()
            self.referencia_codigo_fardo = ctk.StringVar()


            produto_tela = ctk.CTkFrame(self.frame_conteudo, fg_color="#1e1e1e")
            produto_tela.grid(row=0, column=0, sticky="nsew")
            produto_tela.rowconfigure((0,1,2), weight=1)
            produto_tela.columnconfigure(0, weight=1)

            header = ctk.CTkFrame(produto_tela, fg_color="#1e1e1e")
            header.grid(column=0, row=0, sticky="nsew")
            header.columnconfigure((0,1,2), weight=1)
            header.rowconfigure((0,1), weight=1)

            entrys_frame = ctk.CTkFrame(produto_tela, fg_color="#1e1e1e")
            entrys_frame.grid(column=0, row=1, sticky="nsew")
            entrys_frame.columnconfigure((0,1,2), weight=1)
            entrys_frame.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)


            botoes_frame = ctk.CTkFrame(produto_tela, fg_color="#1e1e1e")
            botoes_frame.grid(column=0, row=2, sticky="nsew")
            botoes_frame.columnconfigure((0,1,2,3,4,5), weight=1)
            botoes_frame.rowconfigure((0,1), weight=1)

            buttons = [("""Salvar""", "green", self.controller.criar),
                       ("Excluir produto", "red", lambda: self.controller.deletar(self.codigo.get())),
                       ("Alterar código", "green", self.controller.editar),
                       ("Voltar", "red", self.voltar)]
            
            self.entrys = [("Código", self.codigo), ("Nome", self.nome), ("Tipo", self.tipo), ("Preço custo", self.preco_custo), ("Preço venda", self.preco_venda), ("Quantidade", self.quantidade), ("Qtd_fardo", self.referencia_codigo_fardo), ("Referencia_id_pai", self.qtd_fardo)]
            
            #label principal
            ctk.CTkLabel(header, 
                      text="""Menu de cadastro de produtos""", 
                      text_color="white",
                      fg_color="#1e1e1e",
                      font=("arial", 32, "bold")
                      ).grid(column=1, row=0)
            
            #label status
            ctk.CTkLabel(header, 
                      textvariable=self.status_menu,
                      text_color="red",
                      fg_color="#1e1e1e",
                      font=("arial", 22, "bold")
                      ).grid(column=1, row=1, sticky="s") 

            entry_codigo = ctk.CTkEntry(entrys_frame,
                        width=350,
                        height=50,
                        font=("arial", 26, "bold"),
                        textvariable=self.codigo)
            entry_codigo.grid(row=1, column=0, sticky="n", padx=20)
            
            label_codigo = ctk.CTkLabel(entrys_frame, 
                    text="Código",
                    text_color="white",
                    fg_color="#1e1e1e",
                    font=("arial", 32, "bold")
                    ).grid(row=0, column=0, sticky="s", padx=20)
            
            entry_nome = ctk.CTkEntry(entrys_frame,
                        width=400,
                        height=50,
                        font=("arial", 26, "bold"),
                        textvariable=self.nome)
            entry_nome.grid(row=1, column=1, sticky="n", padx=20)
            
            label_nome = ctk.CTkLabel(entrys_frame, 
                    text="Nome",
                    text_color="white",
                    fg_color="#1e1e1e",
                    font=("arial", 32, "bold")
                    ).grid(row=0, column=1, sticky="s", padx=20)
            
            #combobox tipo
            combobox_tipo = ctk.CTkComboBox(entrys_frame,
                                            values=["unidade", "fardo"],
                                            variable=self.tipo,
                                            width=310,
                                            height=50,
                                            font=("arial", 32, "bold"),
                                            command=self.controller.mudar_conteudo
                                            )
            combobox_tipo.grid(row=8, column=1)
            self.tipo.set("unidade")

            
            entry_preco_custo = ctk.CTkEntry(entrys_frame,
                        width=100,
                        height=50,
                        font=("arial", 26, "bold"),
                        textvariable=self.preco_custo)
            entry_preco_custo.grid(row=5, column=0, sticky="n", padx=20)
            
            label_preco_custo = ctk.CTkLabel(entrys_frame, 
                    text="Preço Custo",
                    text_color="white",
                    fg_color="#1e1e1e",
                    font=("arial", 32, "bold")
                    ).grid(row=4, column=0, sticky="s", padx=20)
            
            entry_preco_venda = ctk.CTkEntry(entrys_frame,
                        width=100,
                        height=50,
                        font=("arial", 26, "bold"),
                        textvariable=self.preco_venda)
            entry_preco_venda.grid(row=5, column=1, sticky="n", padx=20)
            
            label_preco_venda = ctk.CTkLabel(entrys_frame, 
                    text="Preço venda",
                    text_color="white",
                    fg_color="#1e1e1e",
                    font=("arial", 32, "bold")
                    ).grid(row=4, column=1, sticky="s", padx=20)
            
            #margem
            label_margem = ctk.CTkLabel(entrys_frame, 
                    textvariable=self.margem,
                    text_color="white",
                    fg_color="#1e1e1e",
                    font=("arial", 32, "bold")
                    ).grid(row=5, column=2, sticky="w", padx=20)

            self.margem.set("Margem de lucro: 0%")
            
            entry_quantidade = ctk.CTkEntry(entrys_frame,
                        width=120,
                        height=50,
                        font=("arial", 26, "bold"),
                        textvariable=self.quantidade)
            entry_quantidade.grid(row=1, column=2, sticky="n", padx=20)
            
            label_quantidade = ctk.CTkLabel(entrys_frame, 
                    text="Quantidade",
                    text_color="white",
                    fg_color="#1e1e1e",
                    font=("arial", 32, "bold")
                    ).grid(row=0, column=2, sticky="s", padx=20)
            
            #label dependendo do tipo
            self.label_tipo = ctk.CTkLabel(entrys_frame, 
                            text="Referencia produto", 
                            text_color="white",
                            fg_color="#1e1e1e",
                            font=("arial", 32, "bold")
                          )
            self.label_tipo.grid(row=7, column=0, padx=20, sticky="s")

            #entrada dependendo do tipo
            self.entry_tipo = ctk.CTkEntry(entrys_frame, 
                                  textvariable=self.referencia_codigo_fardo, 
                                  width=300,
                                  height=50,
                                  font=("Arial", 20, "bold"))
            self.entry_tipo.grid(row=8, column=0, padx=20, sticky="n")

            #na ordem que ta na tela
            self.entries.append(entry_codigo)
            self.entries.append(entry_nome)
            self.entries.append(entry_quantidade)
            self.entries.append(entry_preco_custo)
            self.entries.append(entry_preco_venda)
            self.entries.append(self.entry_tipo)
            self.entries.append(combobox_tipo)

            #teclas para mudar campo
            for i, entry in enumerate(self.entries):
                entry.bind("<Return>", lambda e, idx=i: self.proximo_campo(idx)) #enter
                entry.bind("<Down>", lambda e, idx=i: self.proximo_campo(idx)) #seta pra baixo
                entry.bind("<Up>", lambda e, idx=i: self.campo_anterior(idx)) #seta pra cima
                entry.bind("<Escape>", lambda e: self.voltar())
        
            #botoes de escolha
            for i, (texto, cor, comando) in enumerate(buttons, start=1):
                ctk.CTkButton(botoes_frame, 
                        text=texto, 
                        text_color="black", 
                        corner_radius=40,
                        border_color="black",
                        hover_color=cor,
                        border_width=5,
                        width=200,  
                        height=100,
                        font=("Arial", 30, "bold"),
                        fg_color="orange",
                        command=comando
                        ).grid(column=i, row=0, padx=20)
                
            self.master.bind("<Escape>", lambda e: self.voltar())
            self.entries[0].focus_set()

        def atualizar_margem(self, *args):
            try:
                preco_venda = float(self.preco_venda.get())
                preco_custo = float(self.preco_custo.get())
            
            except:
                raise ValueError
            
            try:
                margem = (preco_venda - preco_custo) / preco_venda * 100
            except:
                raise ZeroDivisionError

            if margem < 0:
                self.margem.set("")
                return

            self.margem.set(f"Margem de lucro: {margem:.2f}%")
            
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

    
    def criar(self):
        """Recebe as entradas e envia para a classe estoque criar e salvar o produto"""
        try:
            codigo = int(self.tela.codigo.get())
            nome = self.tela.nome.get()
            preco_custo = float(self.tela.preco_custo.get())
            preco_venda = float(self.tela.preco_venda.get())
            quantidade = int(self.tela.quantidade.get())
            tipo = self.tela.tipo.get()
                
            ref_str = self.tela.referencia_codigo_fardo.get().strip()
            referencia_produto = int(ref_str) if ref_str else None

            qtd_str = self.tela.qtd_fardo.get().strip()
            qtd_fardo = int(qtd_str) if qtd_str else None

        except ValueError:
            self.tela.status_menu.set("Digite apenas numeros")
            return
        
        resultado = self.ref_estoque.criar_produto(codigo,nome,tipo,preco_custo,preco_venda,quantidade, referencia_produto, qtd_fardo)

        if resultado.get("Status", "Erro") == "Erro":
            self.editar(codigo,nome,preco_custo,preco_venda,quantidade,tipo,referencia_produto,qtd_fardo)
            return
    
        self.tela.status_menu.set(resultado.get("Mensagem", "Erro"))

        self.limpar_variaveis()

    def editar(self):
        codigo = self.tela.codigo.get()
        atributos = []
        for i, (texto, var) in enumerate(self.tela.entrys):
                atributos.append(self.tela.entrys.get([i+1]))
                print(atributos)
                                                                        
        self.tela.status_menu.set(self.ref_estoque.atualizar_produto(codigo, atributos))

    def deletar(self, codigo):
        try:
            codigo = int(codigo)
            self.tela.status_menu.set(self.ref_estoque.remover_produto(codigo))
        except ValueError:
            self.tela.status_menu.set("Digite apenas numeros")
            return

        for i, tupla in enumerate(self.tela.entrys):
                if i == 0:
                    continue
                tupla[1].set("")
        
    def mudar_conteudo(self, valor):
        self.tela.tipo = valor
        if self.tela.tipo == "fardo":
            self.tela.label_tipo.configure(text="Quantidade no fardo")
            self.tela.entry_tipo.configure(textvariable=self.tela.qtd_fardo)
            
        else:
            self.tela.label_tipo.configure(text="Referencia produto")
            self.tela.entry_tipo.configure(textvariable=self.tela.referencia_codigo_fardo)
    
    def buscar_produto(self, *args):
        codigo = self.tela.codigo.get()
        try:
            codigo = int(codigo)
        except:
            raise ValueError
        
        produto = self.ref_estoque.get_produto(codigo)

        if produto:
            print(produto)
            for i, (texto, var) in enumerate(self.tela.entrys):
                var.set(produto[i+1])
                print(produto[i+1])
            self.mudar_conteudo(produto[3])

        else:
            for i, tupla in enumerate(self.tela.entrys):
                if i == 0:
                    continue
                tupla[1].set("")
    
    def limpar_variaveis(self):
        for i, tupla in enumerate(self.tela.entrys):
                if i == 0:
                    continue
                tupla[1].set("")