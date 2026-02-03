import customtkinter as ctk


class RelatoriosMenu(ctk.CTkFrame):
    def __init__(self, master, main):
        super().__init__(master=master, fg_color="#1e1e1e")
        self.main = main

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self._criar_header()
        self._criar_tabs()

    def _criar_header(self):
        header = ctk.CTkFrame(self, fg_color="#1e1e1e")
        header.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        header.columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(
            header,
            text="Relatórios",
            font=("Arial", 32, "bold")
        ).grid(row=0, column=0, sticky="w")

    def _criar_tabs(self):
        container = ctk.CTkFrame(self, fg_color="#1e1e1e")
        container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        self.tabs = ctk.CTkTabview(container)
        self.tabs.grid(row=0, column=0, sticky="nsew")

        self.tab_caixa = self.tabs.add("Caixa")
        self.tab_estoque = self.tabs.add("Estoque")
        self.tab_produtos = self.tabs.add("Produtos mais vendidos")

        self._aba_caixa()
        self._aba_estoque()
        self._aba_produtos()

    def _aba_caixa(self):
        self.tab_caixa.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.tab_caixa,
            text="Relatório de movimentação de caixa",
            font=("Arial", 20, "bold")
        ).grid(row=0, column=0)

    def _aba_estoque(self):
        self.tab_estoque.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.tab_estoque,
            text="Relatório de movimentação de estoque",
            font=("Arial", 20, "bold")
        ).grid(row=0, column=0)

    def _aba_produtos(self):
        self.tab_produtos.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.tab_produtos,
            text="Produtos mais vendidos",
            font=("Arial", 20, "bold")
        ).grid(row=0, column=0)
