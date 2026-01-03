from tkinter import ttk
from tkinter import *
import customtkinter as ctk

class EstoqueMenu(ctk.CTkFrame):

    def __init__(self, root, referencia_main):
        super().__init__(master=root, fg_color="#1e1e1e")
        self.referencia_main = referencia_main

        #frame
        self.frame_conteudo = ttk.Frame(self)
        self.frame_conteudo.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.frame_conteudo.rowconfigure(0, weight=1)
        self.frame_conteudo.columnconfigure(0, weight=1)

        self.ordem = {"nome": False,
        "codigo": False}

        self.bind_all(
            "<Escape>", 
            self.voltar
            )
        
        #scroll
        self.scroll = ttk.Scrollbar(self.frame_conteudo)
        self.scroll.grid(row=0, column=1, sticky="ns")

        #tabela
        self.tabela = ttk.Treeview(
            self.frame_conteudo,
            columns=("codigo", "nome", "preco", "preco_venda", "quantidade", "margem lucro"),
            show="headings",
            yscrollcommand=self.scroll.set
        )

        #inserção da tabela
        self.tabela.grid(row=0, column=0, sticky="nsew")

        #inserção do scroll
        self.scroll.config(command=self.tabela.yview)

        #Cabeçalhos da tabela
        self.tabela.heading("codigo", text="Código", command=lambda: self.ordenar_estoque("codigo"))
        self.tabela.heading("nome", text="Nome", command=lambda: self.ordenar_estoque("nome"))
        self.tabela.heading("preco", text="Preço")
        self.tabela.heading("preco_venda", text="Preço de venda")
        self.tabela.heading("quantidade", text="Quantidade")
        self.tabela.heading("margem lucro", text="Margem lucro")

        #Coluna da tabela
        self.tabela.column("codigo", width=80)
        self.tabela.column("nome", width=150)
        self.tabela.column("preco", width=100)
        self.tabela.column("preco_venda", width=100)
        self.tabela.column("quantidade", width=100)
        self.tabela.column("margem lucro", width=70)

        self.carregar_estoque()

        ttk.Button(self, 
                   text="Voltar", 
                   width=30, 
                   padding=30, 
                   command=self.referencia_main.voltar_menu_principal
                   ).grid(row=1, column=0, sticky=W)

    def carregar_estoque(self):
        for item in self.tabela.get_children(): #retorna o id de cada linha
            self.tabela.delete(item)

        estoque = self.referencia_main.estoque.itens

        if not estoque:
            return

        for produto in estoque.values(): #pega o objeto no estoque e insere na tabela
            self.tabela.insert(
                "",
                "end",
                values=(
                    produto.codigo,
                    produto.nome,
                    f"{produto.preco_custo:.2f}",
                    f"{produto.preco_venda:.2f}",
                    produto.quantidade,
                    f"{((produto.preco_venda - produto.preco_custo) / produto.preco_venda) * 100:.2f}%"
                )
            )

    def ordenar_estoque(self, coluna):
        reverso = self.ordem.get(coluna, False)

        dados = [(self.tabela.set(id_linha, coluna), id_linha)
        for id_linha in self.tabela.get_children()]
        
        try:
            dados.sort(key=lambda x: float(x[0]), reverse=reverso)
        except ValueError:
            dados.sort(key=lambda x: x[0], reverse=reverso)

        for indice, (_, item_id) in enumerate(dados):
            self.tabela.move(item_id, '', indice)   

        self.ordem[coluna] = not reverso


    def voltar(self, event):
        self.unbind_all("<Escape>")
        self.referencia_main.voltar_menu_principal()