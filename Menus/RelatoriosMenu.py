import customtkinter as ctk
from tkinter import ttk
from datetime import date


class RelatoriosMenu(ctk.CTkFrame):
    def __init__(self, master, main):
        super().__init__(master=master, fg_color="#1e1e1e")
        self.main = main

        self.controller = RelatorioController(self, self.main.relatorios)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        style = ttk.Style()
        style.theme_use("clam")

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
        self.filtro_data = ctk.StringVar()
        self.forma_pgt = ctk.StringVar()
        self.forma_pgt.set("Tudo")
        self.usuario = ctk.StringVar()
        self.usuario.set(self.main.usuario_atual)
        usuarios = self.main.get_usuarios()
        forma_pgt = ["Tudo", "Dinheiro", "Cartão", "Pix", "Sangria"]

        self.master.bind("<Return>", lambda e: self.carregar_produto_selecionado())

        hoje = date.today().strftime("%d/%m/%Y")
        self.filtro_data.set(hoje)

        self.tab_caixa.columnconfigure((0,1), weight=1)
        self.tab_caixa.rowconfigure(0, weight=1)

        frame_filtros = ctk.CTkFrame(self.tab_caixa)
        frame_filtros.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        frame_filtros.rowconfigure((0,1,2,3), weight=1)
        frame_filtros.columnconfigure((0,1), weight=1)


        self.frame_tabela = ctk.CTkFrame(self.tab_caixa)
        self.frame_tabela.rowconfigure(1, weight=1)
        self.frame_tabela.rowconfigure((0, 2), weight=0)
        self.frame_tabela.columnconfigure(0, weight=1)
        self.frame_tabela.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.carregar_header()
        self.controller.filtrar_relatorio_caixa(data=self.filtro_data.get()) #carrega o caixa com o filtro do dia atual
        self.carregar_bottom()

        botao_filtrar = ctk.CTkButton(frame_filtros,
            text="Filtrar", 
            text_color="black", 
            corner_radius=40,
            border_color="black",
            hover_color="white",
            border_width=5,
            width=150,  
            height=100,
            fg_color="orange",
            font=("Arial", 30, "bold"),
            command=lambda: self.controller.filtrar_relatorio_caixa(usuario=self.usuario.get(), data=self.filtro_data.get(), forma_pgt=self.forma_pgt.get())
            )
        botao_filtrar.grid(row=4, column=0, sticky="nsew")

        botao_voltar = ctk.CTkButton(frame_filtros,
            text="Sair", 
            text_color="black", 
            corner_radius=40,
            border_color="black",
            hover_color="red",
            border_width=5,
            width=150,  
            height=100,
            fg_color="orange",
            font=("Arial", 30, "bold"),
            command=self.main.voltar_menu_principal
            )
        botao_voltar.grid(row=4, column=1, sticky="nsew")

        label_filtros = ctk.CTkLabel(frame_filtros,
                    text="Filtros",
                    font=("arial", 60, "bold")
                    )
        label_filtros.grid(row=0, column=0, columnspan=2, sticky="n")

        label_data = ctk.CTkLabel(frame_filtros,
                    text="Digite a data",
                    font=("arial", 40, "bold")
                    )
        label_data.grid(row=0, column=0, sticky="s")

        entry_data = ctk.CTkEntry(frame_filtros, width=300, height=50, textvariable=self.filtro_data, font=("arial",32))
        entry_data.grid(row=1, column=0, sticky="n")

        label_usuario = ctk.CTkLabel(frame_filtros,
                    text="Escolha um usuario",
                    font=("arial", 40, "bold")
                    )
        label_usuario.grid(row=0, column=1, sticky="s")
        combobox_usuario = ctk.CTkComboBox(frame_filtros, height=50, width=300, fg_color="#1e1e1e", font=("arial", 32, "bold"), variable=self.usuario, values=usuarios, command=self.mudar_usuario)
        combobox_usuario.grid(row=1, column=1, sticky="n")

        label_pgt = ctk.CTkLabel(frame_filtros,
                    text="Pagamento",
                    font=("arial", 40, "bold")
                    )
        label_pgt.grid(row=2, column=0, sticky="s")
        combobox_pgt = ctk.CTkComboBox(frame_filtros, height=50, width=300, fg_color="#1e1e1e", font=("arial", 32, "bold"), variable=self.forma_pgt, values=forma_pgt, command=self.mudar_forma_pgt)
        combobox_pgt.grid(row=3, column=0, sticky="n")


    def carregar_relatorio_caixa(self, vendas=None):
        colunas = ("caixa_id", "data/hora", "funcionario", "pagamento", "total")

        self.tabela = ttk.Treeview(
            self.frame_tabela,
            columns=colunas,
            show="headings"
        )

        self.tabela.heading("caixa_id", text="ID")
        self.tabela.heading("data/hora", text="Data/Hora")
        self.tabela.heading("funcionario", text="Funcionário")
        self.tabela.heading("pagamento", text="Pagamento")
        self.tabela.heading("total", text="Total")

        self.tabela.column("caixa_id", anchor="center", width=60)
        self.tabela.column("data/hora", anchor="center", width=200)
        self.tabela.column("funcionario", anchor="center", width=180)
        self.tabela.column("pagamento", anchor="center", width=120)
        self.tabela.column("total", anchor="e", width=100)

        self.tabela.grid(row=1, column=0, sticky="nsew")

        for widget in self.tabela.get_children():
            widget.destroy()

        if vendas is None:
            vendas = self.main.relatorios.mostrar_vendas()

        for venda in vendas:
            self.tabela.insert(
                "",
                "end",
                iid=venda[0],
                values=(
                    venda[1],
                    str(venda[2]) + " / " + str(venda[3]),
                    venda[4],
                    venda[5],
                    f"R$ {venda[6]:.2f}"
                )
            )

    def carregar_header(self):
        self.dados = self.main.caixa.retornar_dados_caixa(self.filtro_data.get(), self.usuario.get())
        if self.dados is None:
            return
        
        frame_header = ctk.CTkFrame(self.frame_tabela, fg_color="#1e1e1e")
        frame_header.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        frame_header.rowconfigure((0,1), weight=1)
        frame_header.columnconfigure((0,1,2), weight=1)

        caixa_id_label = ctk.CTkLabel(frame_header, fg_color="#1e1e1e", font=("arial", 20), text=f"CAIXA ID: {self.dados[0]}")
        caixa_id_label.grid(row=0, column=0, sticky="nsew")

        data = self.dados[1]
        data_label = ctk.CTkLabel(frame_header, fg_color="#1e1e1e", font=("arial", 20), text=f"Data: {data}")
        data_label.grid(row=0, column=1, sticky="nsew")

        hora_label = ctk.CTkLabel(frame_header, fg_color="#1e1e1e", font=("arial", 20), text=f"Hora: {self.dados[2]}")
        hora_label.grid(row=0, column=2, sticky="nsew")

        funcionario_label = ctk.CTkLabel(frame_header, fg_color="#1e1e1e", font=("arial", 20), text=f"Funcionario: {self.dados[4]}")
        funcionario_label.grid(row=1, column=1, sticky="nsew")

        abertura_caixa_label = ctk.CTkLabel(frame_header, fg_color="#1e1e1e", font=("arial", 20), text=f"Abertura de caixa: R${self.dados[5]:.2f}")
        abertura_caixa_label.grid(row=1, column=2, sticky="nsew")

    def carregar_bottom(self):
        frame_bottom = ctk.CTkFrame(self.frame_tabela)
        frame_bottom.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        frame_bottom.columnconfigure((0, 1), weight=1)

        abertura_caixa = self.main.caixa.retornar_dados_caixa(self.filtro_data.get(), self.usuario.get())[5]

        self.total_vendas = ctk.StringVar()
        self.total_vendas.set(f"R$ {self.main.relatorios.total_vendas(self.usuario.get(), self.filtro_data.get()):.2f}")

        self.total_descontos = ctk.StringVar()
        self.total_descontos.set(f"R$ {self.main.relatorios.total_descontos(self.usuario.get(), self.filtro_data.get()):.2f}")

        self.valor_final_caixa = ctk.StringVar()
        self.valor_final_caixa.set(f"R$ {self.main.relatorios.total_vendas(self.usuario.get(), self.filtro_data.get()) + abertura_caixa - self.main.relatorios.total_descontos(self.usuario.get(), self.filtro_data.get()):.2f}")

        # Linha 0 (total vendas)
        ctk.CTkLabel(frame_bottom, text="Total vendas:").grid(
            row=0, column=0, sticky="w", padx=10, pady=5
        )
        self.lbl_total_vendas = ctk.CTkLabel(frame_bottom, textvariable=self.total_vendas)
        self.lbl_total_vendas.grid(
            row=0, column=1, sticky="e", padx=10, pady=5
        )

        # Linha 1 (sangrias)
        ctk.CTkLabel(frame_bottom, text="Total sangrias:").grid(
            row=1, column=0, sticky="w", padx=10, pady=5
        )
        self.lbl_total_sangrias = ctk.CTkLabel(frame_bottom, text="R$ 0,00")
        self.lbl_total_sangrias.grid(
            row=1, column=1, sticky="e", padx=10, pady=5
        )

        # Linha 2 (descontos)
        ctk.CTkLabel(frame_bottom, text="Total descontos:").grid(
            row=2, column=0, sticky="w", padx=10, pady=5
        )
        self.lbl_total_descontos = ctk.CTkLabel(frame_bottom, textvariable=self.total_descontos)
        self.lbl_total_descontos.grid(
            row=2, column=1, sticky="e", padx=10, pady=5
        )

        # Linha 3 (valor final)
        ctk.CTkLabel(
            frame_bottom,
            text="Valor esperado em caixa:",
            font=("Arial", 14, "bold")
        ).grid(
            row=3, column=0, sticky="w", padx=10, pady=(10, 5)
        )

        self.lbl_valor_esperado = ctk.CTkLabel(
            frame_bottom,
            textvariable=self.valor_final_caixa, #falta descontar sangria e adicionar abertura de caixa na soma
            font=("Arial", 14, "bold")
        )
        self.lbl_valor_esperado.grid(
            row=3, column=1, sticky="e", padx=10, pady=(10, 5)
        )

    def carregar_produto_selecionado(self):
        id_movimentacao = self.tabela.selection()
        if not id_movimentacao:
            return
    
        CarregarProdutos(self.master, self.main.relatorios, id_movimentacao)

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

    def mudar_usuario(self, usuario):
        self.usuario.set(usuario)

    def mudar_forma_pgt(self, forma):
        self.forma_pgt.set(forma)

class CarregarProdutos(ctk.CTkToplevel):
    def __init__(self, master, relatorios, id_mov):
        super().__init__(master=master, fg_color="#1e1e1e")
        self.relatorios = relatorios
        self.id_mov = id_mov
        self.produtos = self.relatorios.retornar_produtos(self.id_mov)

        self.title("Movimentação de produtos")
        self.geometry("800x500")
        self.resizable(False, False)

        self.transient(master)
        self.grab_set()

        self._criar_widgets()

    def _criar_widgets(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        frame.grid_columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        colunas = ("codigo", "nome", "quantidade", "valor_unitario", "subtotal")

        self.tabela = ttk.Treeview(
            frame,
            columns=colunas,
            show="headings"
        )

        self.tabela.heading("codigo", text="Código")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("quantidade", text="Quantidade")
        self.tabela.heading("valor_unitario", text="Valor_Unit")
        self.tabela.heading("subtotal", text="Subtotal")

        self.tabela.column("codigo", anchor="center", width=60)
        self.tabela.column("nome", anchor="center", width=200)
        self.tabela.column("quantidade", anchor="center", width=180)
        self.tabela.column("valor_unitario", anchor="center", width=120)
        self.tabela.column("subtotal", anchor="e", width=100)

        self.tabela.grid(row=0, column=0, sticky="nsew")

        for widget in self.tabela.get_children():
            widget.destroy()

        for produto in self.produtos:
            self.tabela.insert(
                "",
                "end",
                values=(
                    produto[0],
                    produto[1],
                    produto[2],
                    f"R$ {produto[3]:.2f}",
                    f"R$ {produto[4]:.2f}"
                )
            )

        btn_cancelar = ctk.CTkButton(
            frame,
            text="Fechar",
            fg_color="red",
            height=70,
            command=self.destroy
        )
        btn_cancelar.grid(row=1, column=0, sticky="ew", pady=10)


class RelatorioController:
    def __init__(self, tela, relatorios):
        self.tela = tela
        self.relatorios = relatorios

    def filtrar_relatorio_caixa(self, **dados):
        if dados:
            resultado = self.relatorios.filtrar_vendas(dados.get("usuario"), dados.get("data"), dados.get("forma_pgt"))
            self.tela.carregar_relatorio_caixa(resultado)
            self.tela.carregar_header()
            self.tela.carregar_bottom()