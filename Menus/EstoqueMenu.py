from tkinter import ttk
from tkinter import *

class EstoqueMenu(ttk.Frame):

    def __init__(self, root, referencia_main):
        super().__init__(root, padding=10)
        self.referencia_main = referencia_main

        self.frame_conteudo = ttk.Frame(self)
        self.frame_conteudo.grid(row=0, column=0, sticky="nsew")

        self.ordem = {"nome": False,
        "codigo": False}

        ttk.Button(self, text="Voltar", command=self.referencia_main.voltar_menu_principal).grid(row=1, column=0, sticky=W)

        self.scroll = ttk.Scrollbar(self.frame_conteudo)
        self.scroll.grid(row=0, column=1, sticky="ns")

        self.tabela = ttk.Treeview(
            self.frame_conteudo,
            columns=("codigo", "nome", "preco", "quantidade", "margem lucro"),
            show="headings",
            yscrollcommand=self.scroll.set
        )

        self.tabela.grid(row=0, column=0, sticky="nsew")

        self.scroll.config(command=self.tabela.yview)

        self.tabela.heading("codigo", text="Código", command=lambda: self.ordenar_estoque("codigo"))
        self.tabela.heading("nome", text="Nome", command=lambda: self.ordenar_estoque("nome"))
        self.tabela.heading("preco", text="Preço")
        self.tabela.heading("quantidade", text="Quantidade")
        self.tabela.heading("margem lucro", text="Margem lucro")

        self.tabela.column("codigo", width=80)
        self.tabela.column("nome", width=150)
        self.tabela.column("preco", width=100)
        self.tabela.column("quantidade", width=100)
        self.tabela.column("margem lucro", width=70)

        self.carregar_estoque()

    def carregar_estoque(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        estoque = self.referencia_main.estoque.itens

        if not estoque:
            return

        for produto in estoque.values():
            self.tabela.insert(
                "",
                "end",
                values=(
                    produto.codigo,
                    produto.nome,
                    f"{produto.preco_venda:.2f}",
                    produto.quantidade,
                    f"{((produto.preco_venda - produto.preco_custo) / produto.preco_venda) * 100:.2f}%"
                )
            )

    def ordenar_estoque(self, coluna):

        reverso = self.ordem.get(coluna, False)

        dados = [(self.tabela.set(item, coluna), item)
        for item in self.tabela.get_children()]
        
        try:
            dados.sort(key=lambda x: float(x[0]), reverse=reverso)
        except ValueError:
            dados.sort(key=lambda x: x[0], reverse=reverso)

        for indice, (_, item_id) in enumerate(dados):
            self.tabela.move(item_id, '', indice)   

        self.ordem[coluna] = not reverso