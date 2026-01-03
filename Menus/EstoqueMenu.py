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

        self.master.bind_all("<Escape>", self.voltar)

        #Estilo para tabela
        style = ttk.Style()

        style.configure(
            "Custom.Treeview",
            background="#1e1e1e",      
            foreground="white",        
            fieldbackground="#1e1e1e",
            rowheight=30,
            font=("Arial", 16, "bold")
        )

        style.map(
            "Custom.Treeview",
            background=[("selected", "#ff9800")],
            foreground=[("selected", "black")]
        )
                
        style.configure(
            "Custom.Treeview.Heading",
            background="#333333",
            foreground="white",
            font=("Arial", 14, "bold")
        )

        #scroll
        self.scroll = ttk.Scrollbar(self.frame_conteudo)
        self.scroll.grid(row=0, column=1, sticky="ns")

        #tabela
        self.tabela = ttk.Treeview(
            self.frame_conteudo,
            columns=("codigo", "nome", "preco", "preco_venda", "quantidade", "margem lucro"),
            show="headings",
            style="Custom.Treeview",
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

        ctk.CTkButton(self, 
                    text="Voltar", 
                    text_color="black", 
                    corner_radius=20,
                    border_color="black",
                    hover_color="white",
                    width=300,  
                    height=100,
                    font=("Arial", 16, "bold"),
                    fg_color="orange",
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
                    f"R$: {produto.preco_custo:.2f}",
                    f"R$: {produto.preco_venda:.2f}",
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
        self.master.unbind_all("<Escape>")
        self.referencia_main.voltar_menu_principal()