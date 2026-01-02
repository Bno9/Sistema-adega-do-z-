from tkinter import ttk
from tkinter import *

class CaixaMenu(ttk.Frame):

    def __init__(self, root, referencia_main):
        super().__init__(root, padding=10)
        self.referencia_main = referencia_main
        
        #textos
        self.status = StringVar()
        self.status_modal = StringVar()
        self.total_var = StringVar()

        #entradas
        self.codigo = StringVar()
        self.valor_pago = StringVar()
        self.quantidade = IntVar(value=1)

        #frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.frame_conteudo = ttk.Frame(self)
        self.frame_conteudo.grid(row=0, column=0, sticky="nsew")
        self.frame_conteudo.columnconfigure(0,weight=1)
        self.frame_conteudo.columnconfigure(1, weight=0)
        self.frame_conteudo.columnconfigure(10, weight=0)
        self.frame_conteudo.rowconfigure(2,weight=1)

        #entry/label codigo
        self.entry_codigo = ttk.Entry(
            self.frame_conteudo,
            textvariable=self.codigo,
            width=30
        )
        self.entry_codigo.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.entry_codigo.focus_set()
        self.entry_codigo.bind("<Return>", self.enviar_codigo)
        self.entry_codigo.bind("<Right>", lambda e: self.entry_quantidade.focus())

        ttk.Label(
        self.frame_conteudo,
        text="Código do produto"
        ).grid(row=0, column=0, sticky="w", padx=10)

        self.entry_codigo.grid(row=1, column=0, sticky="w", padx=10)

        #entry/label quantidade
        self.entry_quantidade = ttk.Entry(
            self.frame_conteudo,
            textvariable=self.quantidade,
            width=30
        )
        self.entry_quantidade.grid(row=0, column=10, sticky="w", padx=10, pady=10)
        self.entry_quantidade.bind("<Return>", self.enviar_codigo)
        self.entry_quantidade.bind("<Left>", lambda e: self.entry_codigo.focus())

        ttk.Label(
        self.frame_conteudo,
        text="Quantidade"
        ).grid(row=0, column=10, sticky="w", padx=10)

        self.entry_quantidade.grid(row=1, column=10, sticky="w", padx=10)

        #status
        ttk.Label(
            self.frame_conteudo,
            textvariable=self.status,
            padding=30,
            font=("arial",20)
        ).grid(row=1, column=1, sticky="n", padx=10)
        
        # TABELA
        self.scroll = ttk.Scrollbar(self.frame_conteudo)
        self.scroll.grid(row=2, column=1, sticky="ns")

        self.tabela = ttk.Treeview(
            self.frame_conteudo,
            columns=("codigo", "nome", "preco", "quantidade"),
            show="headings",
            selectmode="browse",
            yscrollcommand=self.scroll.set
        )
        self.tabela.grid(row=2, column=0,columnspan=11, sticky="nsew", padx=10)
        self.scroll.config(command=self.tabela.yview)

        self.tabela.heading("codigo", text="Código")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("preco", text="Preço")
        self.tabela.heading("quantidade", text="Qtd")
                
        self.tabela.column("codigo", width=80, minwidth=70, stretch=True, anchor="center")
        self.tabela.column("nome", width=160, minwidth=120, stretch=True)
        self.tabela.column("preco", width=140, minwidth=120, stretch=True, anchor="e")
        self.tabela.column("quantidade", width=120, minwidth=100, stretch=True, anchor="center")

        # TOTAL
        ttk.Label(
            self.frame_conteudo,
            textvariable=self.total_var,
            font=("Arial", 32, "bold")
        ).grid(row=3, column=0, sticky="e", padx=10, pady=10)

        # BOTÕES
        frame_botoes = ttk.Frame(self.frame_conteudo)
        frame_botoes.grid(row=4, column=0, pady=10)

        ttk.Button(
            frame_botoes,
            text="Finalizar Compra",
            width=30,
            padding=20,
            command=self.abrir_modal_finalizar
        ).grid(row=0, column=0, padx=10)

        ttk.Button(
            frame_botoes,
            text="Sair",
            width=30,
            padding=20,
            command=self.voltar
        ).grid(row=0, column=1, padx=10)
        
        #bind
        self.bind_all("<Escape>", self.voltar)
        self.tabela.bind("<Delete>", lambda e: self.excluir_item())

        self.atualizar_tabela()
        self.atualizar_total()

    def layout_caixa(self):
        for item in self.tabela.get_children(): #retorna o id de cada linha
            self.tabela.delete(item)

        items_no_caixa = self.referencia_main.caixa.itens_no_carrinho

        if not items_no_caixa:
            return

        for produto, quantidade in items_no_caixa: #pega o objeto que foi passado e insere na tela
            self.tabela.insert(
                "",
                "end",
                values=(
                    produto.codigo,
                    produto.nome,
                    f"R$:{produto.preco_venda:.2f}",
                    quantidade
                )
            )

    def abrir_modal_finalizar(self):
        """Tela de finalização da compra
            Exibe valor pago e troco"""
        self.modal = ttk.Frame(self.frame_conteudo, padding=20, relief="raised")
        self.modal.place(relx=0.5, rely=0.5, anchor="center")

        self.status_modal.set("")
        self.unbind_all("<Escape>")
        

        self.botao_ok = ttk.Button(
            self.modal,
            text="OK",
            command=self.fechar_modal
            )

        ttk.Label(
            self.modal,
            text="Valor pago",
            font=("Arial", 20)
        ).grid(row=0, column=0, pady=5)

        ttk.Label(
            self.modal,
            textvariable=self.status_modal,
            padding=30,
            font=("arial",20)
        ).grid(row=4, column=0, pady=5)

        self.entry_valor_pago = ttk.Entry(
            self.modal,
            textvariable=self.valor_pago,
            width=30
        )
        self.entry_valor_pago.grid(row=1, column=0, pady=5)
        self.entry_valor_pago.focus_set()
        self.entry_valor_pago.bind("<Return>", lambda e: self.finalizar_compra())
        self.entry_valor_pago.bind("<Escape>", lambda e: self.fechar_modal())

        self.botao_finalizar = ttk.Button(
            self.modal,
            text="Finalizar",
            command=self.finalizar_compra
        )
        self.botao_finalizar.grid(row=2, column=0, pady=10)

        self.botao_cancelar = ttk.Button(
            self.modal,
            text="Cancelar",
            command=self.fechar_modal
        )
        self.botao_cancelar.grid(row=3, column=0)

    def fechar_modal(self):
        self.limpar_campos()
        self.modal.destroy()
        self.entry_codigo.focus_set()
        self.bind_all("<Escape>", self.voltar)

    def enviar_codigo(self, event=None):
        code = self.codigo.get()

        if code == "":
            self.abrir_modal_finalizar()

        try:
            code = int(self.codigo.get())

        except ValueError:
            self.status.set("")
            return
        
        quantidade = self.quantidade.get()
        
        if not self.referencia_main.caixa.validar_codigo(code, quantidade):
            self.status.set("Produto não encontrado")
            return
        
        self.codigo.set("")
        self.status.set("")
        self.atualizar_tabela()
        self.atualizar_total()

    def finalizar_compra(self):
        resultado = self.referencia_main.caixa.finalizar_compra(self.valor_pago.get())

        if not resultado["sucesso"]:
            self.status_modal.set(resultado["mensagem"])
            return

        self.status_modal.set(
            f"""    R${int(self.valor_pago.get()):.2f} 

Troco: R$ {resultado['troco']:.2f}"""
)

        self.botao_ok.grid(row=5, column=0, pady=10)

        self.entry_valor_pago.destroy()
        self.botao_finalizar.destroy()
        self.botao_cancelar.destroy()

        self.atualizar_tabela()
        self.atualizar_total()
        self.quantidade.set(1)

    def excluir_item(self):
        #seleção de linha
        selecionado = self.tabela.selection()

        if not selecionado:
            return

        item_id = selecionado[0] #id do item
        valores = self.tabela.item(item_id, "values") #valores do item

        self.referencia_main.caixa.excluir_do_carrinho(int(valores[0]))
        self.atualizar_tabela()
        self.atualizar_total()

    def atualizar_total(self):
        total = self.referencia_main.caixa.total()
        self.total_var.set(f"Total: R$ {total:.2f}")

    def atualizar_tabela(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for produto, quantidade in self.referencia_main.caixa.itens_no_carrinho:
            self.tabela.insert(
                "",
                "end",
                values=(
                    produto.codigo,
                    produto.nome,
                    f"{produto.preco_venda:.2f}",
                    quantidade
                )
            )


    def voltar(self, event=None):
        resultado = self.referencia_main.caixa.validar_compra_existente()

        if resultado["sucesso"]:
            self.status.set(resultado["mensagem"])
            return
        
        self.unbind_all("<Escape>")
        self.referencia_main.voltar_menu_principal()


    def limpar_campos(self):
        campos = [
            self.codigo,
            self.valor_pago
            ]

        for var in campos:
            var.set("")
