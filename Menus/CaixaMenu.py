from tkinter import ttk
from tkinter import *
import customtkinter as ctk

class CaixaMenu(ctk.CTkFrame):

    def __init__(self, root, referencia_main, usuario, on_sair=None):
        super().__init__(master=root, fg_color="#1e1e1e")
        self.referencia_main = referencia_main
        self.controller = CaixaController(self, self.referencia_main.caixa)
        self.usuario = usuario
        self.on_sair = on_sair if on_sair is not None else self.referencia_main.voltar_menu_principal
        
        #textos
        self.status = StringVar()
        self.total_var = StringVar()
        self.total_itens = StringVar()
        self.compra_pendente = StringVar()
        self.metodo_pagamento = "Dinheiro"

        #entradas
        self.codigo = StringVar()
        self.quantidade = IntVar(value=1)

        #frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.frame_conteudo = ctk.CTkFrame(self, fg_color="#1e1e1e")
        self.frame_conteudo.grid(row=0, column=0, sticky="nsew")
        self.frame_conteudo.columnconfigure(0, weight=1)
        self.frame_conteudo.rowconfigure((0,2), weight=1)
        self.frame_conteudo.rowconfigure(1, weight=4)

        self.header = ctk.CTkFrame(self.frame_conteudo, fg_color="#1e1e1e")
        self.botoes = ctk.CTkFrame(self.frame_conteudo, fg_color="#1e1e1e")
        self.body = ctk.CTkFrame(self.frame_conteudo, fg_color="#1e1e1e")

        self.body.grid(row=1, column=0, sticky="nsew")
        self.header.grid(row=0,column=0, sticky="nsew")
        self.botoes.grid(row=2, column=0, sticky="nsew")

        self.body.columnconfigure(0, weight=1)
        self.body.columnconfigure(1, weight=0)
        self.body.rowconfigure(0, weight=1)
        self.header.columnconfigure((0,1,2), weight=1)
        self.header.rowconfigure((0,1), weight=0)
        self.botoes.columnconfigure((0,1,2), weight=1)
        self.botoes.rowconfigure((0,1), weight=1)

        #entry/label codigo
        self.entry_codigo = ctk.CTkEntry(
            self.header,
            textvariable=self.codigo,
            width=300,
            font=("Arial", 20, "bold")
        )
        self.entry_codigo.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.entry_codigo.focus_set()
        self.entry_codigo.bind("<Return>",
                                lambda e: self.setar_status(resultado=self.controller.enviar_codigo(), 
                                                            label_status=self.label_status, 
                                                           var_status=self.status))
        self.entry_codigo.bind("<Right>", lambda e: self.entry_quantidade.focus())

        #label codigo
        ctk.CTkLabel(
        self.header,
        text="Código do produto",
        text_color="white",
        fg_color="#1e1e1e",
        font=("arial", 24, "bold")
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)

        #label total itens
        ctk.CTkLabel(self.header,
                     textvariable=self.total_itens,
                     text_color="white",
        fg_color="#1e1e1e",
        font=("arial", 48, "bold")
        ).grid(row=1, column=1, sticky="s")
        self.total_itens.set("ITENS: 0")

        #entry/label quantidade
        self.entry_quantidade = ctk.CTkEntry(
            self.header,
            textvariable=self.quantidade,
            width=300,
            font=("Arial", 20, "bold")
        )
        self.entry_quantidade.grid(row=1, column=2, sticky="e", padx=10, pady=10)
        self.entry_quantidade.bind("<Return>",
                                lambda e: self.setar_status(resultado=self.controller.enviar_codigo(), 
                                                            label_status=self.label_status, 
                                                           var_status=self.status))
        self.entry_quantidade.bind("<Left>", lambda e: self.entry_codigo.focus())

        #label quantidade
        ctk.CTkLabel(
        self.header,
        text="Quantidade",
        text_color="white",
        fg_color="#1e1e1e",
        font=("arial", 24, "bold")
        ).grid(row=0, column=2, sticky="e", padx=10, pady=10)

        #label status
        self.label_status = ctk.CTkLabel(
            self.header,
            textvariable=self.status,
            text_color="white",
            fg_color="#1e1e1e",
            font=("arial", 32, "bold")
        )
        self.label_status.grid(row=1, column=1, padx=10)

        #label compra pendente
        compra_pendente = ctk.CTkLabel(
            self.header,
            textvariable=self.compra_pendente,
            text_color="red",
            fg_color="#1e1e1e",
            font=("arial", 32, "bold")
        )
        compra_pendente.grid(row=2, column=1, padx=10, sticky="s")

        #Estilo para tabela
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
        
        #tabela
        self.scroll = ttk.Scrollbar(self.body)
        self.scroll.grid(row=0, column=1, sticky="ns")

        self.tabela = ttk.Treeview(
            self.body,
            columns=("codigo", "nome", "preco", "quantidade"),
            show="headings",
            selectmode="browse",
            style="Custom.Treeview",
            yscrollcommand=self.scroll.set
        )
        self.tabela.grid(row=0, column=0, sticky="nsew", padx=10)
        self.scroll.config(command=self.tabela.yview)

        self.tabela.heading("codigo", text="Código")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("preco", text="Preço")
        self.tabela.heading("quantidade", text="Qtd")
                
        self.tabela.column("codigo", width=80, minwidth=70, stretch=True, anchor="center")
        self.tabela.column("nome", width=160, minwidth=120, stretch=True, anchor="center")
        self.tabela.column("preco", width=140, minwidth=120, stretch=True, anchor="center")
        self.tabela.column("quantidade", width=120, minwidth=100, stretch=True, anchor="center")

        #label total
        ctk.CTkLabel(
            self.botoes,
            textvariable=self.total_var,
            text_color="white",
            fg_color="#1e1e1e",
            font=("Arial", 32, "bold")
        ).grid(row=0, column=1, padx=10)

        #botao finalizar
        ctk.CTkButton(
            self.botoes,
            text="Finalizar Compra",
            text_color="black", 
            corner_radius=20,
            border_color="black",
            border_width=5,
            hover_color="white",
            width=300,  
            height=100,
            font=("Arial", 16, "bold"),
            fg_color="orange",
            command=self.abrir_modal_finalizar
        ).grid(row=0, column=0, padx=10)

        #botao voltar
        ctk.CTkButton(
            self.botoes,
            text="Sair",
           text_color="black", 
            corner_radius=20,
            border_color="black",
            border_width=5,
            hover_color="white",
            width=300,  
            height=100,
            font=("Arial", 16, "bold"),
            fg_color="orange",
            command=self.voltar
        ).grid(row=0, column=2, padx=10)

        frame_atalho = ctk.CTkFrame(self.botoes, fg_color="#e7dddd", corner_radius=12)
        frame_atalho.grid(row=0, column=3, sticky="se")

        frame_atalho.grid_columnconfigure(0, weight=1)
        frame_atalho.grid_rowconfigure(1, weight=1)

        # título
        label_titulo = ctk.CTkLabel(
            frame_atalho,
            text="Atalhos",
            font=("Arial", 17, "bold"),
            text_color="black",
            anchor="center"
        )
        label_titulo.grid(row=0, column=0, sticky="n", padx=14, pady=(12, 6))

        label_atalhos = ctk.CTkLabel(frame_atalho,
                                        text="""
F1 - Finalizar compra
F5 - Aplicar desconto
F7 - Alternar compra
F10 - Consultar produto
Delete - Excluir
Right - Quantidade
Left - Código
Esc - Voltar""",
                text_color="black",
                font=("Consolas", 15),
                anchor="w")
        label_atalhos.grid(row=1, column=0, sticky="nw", padx=10, pady=(0,12))
        
        #binds
        self.master.bind("<F1>", self.atalho_finalizar)
        self.master.bind("<F2>", lambda e: self.pesquisar_produto())
        self.master.bind("<F5>", self.frame_desconto)
        self.master.bind("<F7>", self.mudar_compra)
        self.master.bind("<F10>", self.consultar_produto)
        self.master.bind("<Escape>", self.voltar)
        self.tabela.bind("<Delete>", lambda e: self.controller.excluir_item())

        #carregar layout
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

        self.valor_pago = StringVar()
        self.valor_pago.trace("w", lambda *args: self.atualizar_troco())
        self.status_modal = StringVar()
        self.troco_modal = StringVar()
        
        self.modal = ctk.CTkToplevel(self.frame_conteudo, fg_color="#1e1e1e")
        self.modal.title("Finalizar compra")
        self.modal.geometry("400x450")
        self.modal.resizable(False, False)

        self.modal.transient(self.frame_conteudo)
        self.modal.focus_force()
        self.modal.update_idletasks() 
        self.modal.grab_set()
        self.modal.rowconfigure((0,1,2), weight=1)
        self.modal.columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self.modal, fg_color="#1e1e1e")
        entry = ctk.CTkFrame(self.modal, fg_color="#1e1e1e")
        self.botoes = ctk.CTkFrame(self.modal, fg_color="#1e1e1e")

        self.botoes.columnconfigure((0,1,2), weight=1)
        header.rowconfigure((0,1,2), weight=1)

        header.grid(column=0, row=0)
        entry.grid(column=0, row=1)
        self.botoes.grid(column=0, row=2)

        self.status_modal.set("")
        self.modal.bind("<Escape>", lambda e: self.fechar_modal(self.modal))

         #label status modal
        label_status_modal = ctk.CTkLabel(
            header,
            textvariable=self.status_modal,
            text_color="red",
            fg_color="#1e1e1e",
            font=("arial", 20, "bold")
        )
        label_status_modal.grid(row=1, column=0, pady=5)

        #label status modal
        self.metodo_pagamento_box = ctk.CTkComboBox(
            header,
            values=["Dinheiro", "Cartão", "Pix"],
            variable=self.metodo_pagamento,
            command=self.alterar_metodo_pagamento,
            text_color="white",
            justify="center",
            width=150,
            fg_color="#1e1e1e",
            font=("arial", 20, "bold")
        )
        self.metodo_pagamento_box.grid(row=0, column=0, pady=5)
        self.metodo_pagamento_box.set("Dinheiro")

        #label valor pago
        self.label_valor_pago = ctk.CTkLabel(
            header,
            text="Valor pago",
            text_color="white",
            fg_color="#1e1e1e",
            font=("Arial", 32, "bold")
        )
        self.label_valor_pago.grid(row=2, column=0, pady=5)

        #entry valor pago
        self.entry_valor_pago = ctk.CTkEntry(
            entry,
            textvariable=self.valor_pago,
            width=300,
            font=("Arial", 20, "bold")
        )
        self.entry_valor_pago.grid(row=0, column=0, pady=5)
        self.entry_valor_pago.after(1000, self.entry_valor_pago.focus_set)
        self.entry_valor_pago.bind("<Return>", lambda e: self.setar_status(
                                                                            resultado=self.finalizar_compra(),
                                                                           label_status=label_status_modal, 
                                                                           var_status=self.status_modal)
                                                                           )
        self.entry_valor_pago.bind("<Escape>", lambda e: self.fechar_modal(self.modal))

        #label troco
        ctk.CTkLabel(
            entry,
            textvariable=self.troco_modal,
            text_color="white",
            fg_color="#1e1e1e",
            font=("Arial", 32, "bold")
        ).grid(row=1, column=0, pady=5)
        self.troco_modal.set("Troco: R$ 0.00")

        #botao finalizar compra
        self.botao_finalizar = ctk.CTkButton(
            self.botoes,
            text="Finalizar",
            text_color="black", 
            corner_radius=20,
            border_color="black",
            border_width=5,
            hover_color="white",
            width=300,  
            height=100,
            font=("Arial", 16, "bold"),
            fg_color="orange",
            command=lambda: self.setar_status(
                                                resultado=self.finalizar_compra(),
                                                label_status=label_status_modal, 
                                               var_status=self.status_modal)
                                            )

        self.botao_finalizar.grid(row=0, column=0, pady=10)

        #botao fechar modal
        self.botao_cancelar = ctk.CTkButton(
            self.botoes,
            text="Cancelar",
            text_color="black", 
            corner_radius=20,
            border_color="black",
            border_width=5,
            hover_color="white",
            width=300,  
            height=100,
            font=("Arial", 16, "bold"),
            fg_color="orange",
            command=lambda: self.fechar_modal(self.modal)
        )
        self.botao_cancelar.grid(row=0, column=2)

    def atualizar_troco(self):
        total = self.referencia_main.caixa.total()

        try:
            valor_pago = int(self.valor_pago.get())
        except ValueError:
            return
        
        troco = valor_pago - total
        if troco < 0 or troco > 1000:
            self.troco_modal.set(f"Troco: R$ {0:.2f}")
            return
        
        self.troco_modal.set(f"Troco: R$ {troco:.2f}")

    def alterar_metodo_pagamento(self, metodo):
        self.metodo_pagamento  = metodo

    def finalizar_compra(self):
        """chama o metodo da classe caixa que finaliza a compra"""

        resultado = self.referencia_main.caixa.finalizar_compra(self.valor_pago.get(), self.metodo_pagamento)

        if resultado.sucesso == False:
            return resultado
        
        self.compra_pendente.set("")
        
        #criação botão ok
        self.botao_ok = ctk.CTkButton(
            self.botoes,
            text="OK",
            text_color="black", 
            corner_radius=20,
            border_color="black",
            hover_color="white",
            width=70,  
            height=70,
            font=("Arial", 16, "bold"),
            fg_color="orange",
            command=lambda: self.imprimir_recibo(resultado)
            )
        
        self.botao_ok.grid(column=0, row=0)

        self.master.bind("<Escape>", lambda e: self.fechar_modal(self.modal))
        self.modal.bind("<Return>", lambda e: self.imprimir_recibo(resultado))

        self.valor_pago.set("")

        self.label_valor_pago.destroy()
        self.metodo_pagamento_box.destroy()
        self.entry_valor_pago.destroy()
        self.botao_finalizar.destroy()
        self.botao_cancelar.destroy()

        self.atualizar_tabela()
        self.atualizar_total()
        self.quantidade.set(1)

        return resultado

    def imprimir_recibo(self, resultado): #nao finalizado
        for widget in self.modal.winfo_children():
            widget.destroy()

        self.cpf = ctk.IntVar()

        self.modal.bind("<Return>", lambda e: self.controller.enviar_recibo(resultado.dados["linhas"]))

        self.label_cpf_frame = ctk.CTkFrame(self.modal, fg_color="#1e1e1e")
        self.label_cpf_frame.columnconfigure(0, weight=1)
        self.label_cpf_frame.rowconfigure(0, weight=1)
        self.label_cpf_frame.grid(column=0, row=0, sticky="nsew")

        self.entry_cpf_frame = ctk.CTkFrame(self.modal, fg_color="#1e1e1e")
        self.entry_cpf_frame.columnconfigure(0, weight=1)
        self.entry_cpf_frame.rowconfigure(0, weight=1)
        self.entry_cpf_frame.grid(column=0, row=1, sticky="nsew")

        self.botao_cpf_frame = ctk.CTkFrame(self.modal, fg_color="#1e1e1e")
        self.botao_cpf_frame.columnconfigure(0, weight=1)
        self.botao_cpf_frame.rowconfigure((0,1), weight=1)
        self.botao_cpf_frame.grid(column=0, row=2, sticky="nsew")

        self.label_cpf = ctk.CTkLabel(
            self.label_cpf_frame,
            text="Digite o cpf",
            text_color="white",
            fg_color="#1e1e1e",
            font=("arial", 24, "bold")
            ).grid(column=0, row=0, sticky="nsew")

        self.entry_cpf = ctk.CTkEntry(self.entry_cpf_frame, 
                                      width=300, 
                                      textvariable=self.cpf,
                                      font=("Arial", 20, "bold"))
        self.entry_cpf.grid(column=0, row=0, sticky="ew")
        self.entry_cpf.focus_set()

        self.botao_enviar = ctk.CTkButton(self.botao_cpf_frame,
            text="Enviar",
            text_color="black", 
            corner_radius=20,
            border_color="black",
            border_width=5,
            hover_color="white",
            width=200,  
            height=50,
            font=("Arial", 16, "bold"),
            fg_color="orange",
            command=lambda: self.controller.enviar_recibo(resultado.dados["linhas"]))
        self.botao_enviar.grid(column=0, row=0, pady=20)

        self.botao_cancelar = ctk.CTkButton(self.botao_cpf_frame,
            text="Cancelar",
            text_color="black", 
            corner_radius=20,
            border_color="black",
            border_width=5,
            hover_color="white",
            width=200,  
            height=50,
            font=("Arial", 16, "bold"),
            fg_color="orange",
            command=lambda: self.fechar_modal(self.modal))
        self.botao_cancelar.grid(column=0, row=1, pady=20)

    def fechar_modal(self, modal):
        modal.grab_release()
        modal.destroy()

        self.limpar_campos()
        self.entry_codigo.focus_set()
        self.master.bind("<Escape>", self.voltar)
        self.master.unbind("<Return>")
        

        modal.grab_release()
        modal.destroy()

    def atualizar_total(self):
        total = self.referencia_main.caixa.total()
        self.total_var.set(f"Total: R$ {total:.2f}")

    def atualizar_tabela(self):
        total = 0
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for produto, quantidade in self.referencia_main.caixa.itens_no_carrinho:
            total += quantidade
            self.tabela.insert(
                "",
                "end",
                values=(
                    produto.codigo,
                    produto.nome,
                    f"R$ {produto.preco_venda:.2f}",
                    quantidade
                ))
        
        self.total_itens.set(f"ITENS: {total}")
            
    def frame_desconto(self, event=None):
        desconto = StringVar()
        desconto.trace("w", lambda *args: self.setar_status(
                        resultado=self.controller.dar_desconto(
                        desconto.get()),
                        label_status=self.label_status, 
                        var_status=self.status)
                        )

        #texto desconto
        label_desconto = ctk.CTkLabel(
            self.botoes,
            text="Desconto",
            text_color="green",
            fg_color="#1e1e1e",
            width=100,
            font=("Arial", 32, "bold")
        )
        label_desconto.grid(row=2, column=1, padx=10)

        #entrada de desconto
        entry_desconto = ctk.CTkEntry(
            self.botoes,
            textvariable=desconto,
            text_color="white",
            fg_color="#1e1e1e",
            width=100,
            font=("Arial", 32, "bold")
        )
        entry_desconto.grid(row=1, column=1, padx=10)
        entry_desconto.focus_set()


        self.master.unbind("<Escape>")
        entry_desconto.bind("<Return>", lambda e:  self.entry_codigo.focus_set())
        entry_desconto.bind("<Escape>", lambda e: self.destruir_desconto(label_desconto, entry_desconto))

    def destruir_desconto(self, label, entry):
        label.destroy()
        entry.destroy()
        self.entry_codigo.focus_set()
        self.master.bind("<Escape>", self.voltar)

    def pesquisar_produto(self):
        self.filtro_nome = StringVar()
        self.filtro_nome.trace("w", self.filtrar)
        self.coluna_filtro = "nome"

        modal = ctk.CTkToplevel(self.frame_conteudo, fg_color="#1e1e1e")

        modal.bind("<Escape>", lambda e: self.fechar_modal(modal))
        modal.bind("<Return>", lambda e: self.controller.adicionar_ao_carrinho())

        modal.title("Pesquisar produto")
        modal.geometry("900x900")

        modal.transient(self.frame_conteudo)
        modal.update_idletasks()
        modal.grab_set()   

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#1e1e1e",
            foreground="white",
            rowheight=30,
            fieldbackground="#1e1e1e"
        )
        style.configure(
            "Treeview.Heading",
            background="#2b2b2b",
            foreground="white",
            font=("Arial", 12, "bold")
        )
        style.map("Treeview", background=[("selected", "#2a7fff")])

        self.tabela_estoque = ttk.Treeview(
            modal,
            columns=("codigo", "nome", "preço", "qtd"),
            show="headings"
        )

        self.tabela_estoque.heading("codigo", text="Código")
        self.tabela_estoque.heading("nome", text="Nome")
        self.tabela_estoque.heading("preço", text="Preço")
        self.tabela_estoque.heading("qtd", text="Qtd")

        self.tabela_estoque.column("codigo", width=200, anchor="center")
        self.tabela_estoque.column("nome", width=220, anchor="w")
        self.tabela_estoque.column("preço", width=120, anchor="center")
        self.tabela_estoque.column("qtd", width=60, anchor="center")

        self.tabela_estoque.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(
            modal,
            orient="vertical",
            command=self.tabela_estoque.yview
        )
        self.tabela_estoque.configure(yscrollcommand=scroll.set)

        scroll.grid(row=0, column=1, sticky="ns")
        modal.rowconfigure(0, weight=1)
        modal.rowconfigure(1, weight=0)
        modal.columnconfigure(0, weight=1)

        frame_filtro = ctk.CTkFrame(modal, fg_color="#1e1e1e")
        frame_filtro.grid(row=1, column=0, sticky="nsew")
        frame_filtro.rowconfigure(0, weight=1)
        frame_filtro.columnconfigure((0,1), weight=1)

        label_nome = ctk.CTkLabel(
            frame_filtro,
            text="Digite o nome",
            text_color="white",
            fg_color="#1e1e1e",
            width=100,
            font=("Arial", 32, "bold")
        )
        label_nome.grid(row=1, column=0, sticky="e")
        entry_nome = ctk.CTkEntry(frame_filtro,
                         textvariable=self.filtro_nome,
                         font=("Arial", 20, "bold"),
                         width=200,
                         height=50)
        entry_nome.grid(row=1, column=1, sticky="w")
        entry_nome.focus_set()

        self.carregar_tabela_pesquisa()

    def carregar_tabela_pesquisa(self, estoque=None):

        for item in self.tabela_estoque.get_children():
            self.tabela_estoque.delete(item)

        if estoque is None:
            estoque = self.referencia_main.estoque.get_banco()

        for produto in estoque:
            _, codigo, nome, tipo, preco_custo, preco_venda, quantidade, _, _ = produto

            self.tabela_estoque.insert(
                "",
                "end",
                values=(
                    codigo,
                    nome,
                    preco_venda,
                    quantidade
                )
            )

    def filtrar(self, *args):
        digitado = self.filtro_nome.get()
        filtro = self.referencia_main.estoque.filtrar_produto(self.coluna_filtro, digitado)
        self.carregar_tabela_pesquisa(filtro)

    def atalho_finalizar(self, event=None):
        resultado = self.controller.enviar_codigo()
        self.setar_status(resultado, label_status=self.label_status, var_status=self.status)
        self.abrir_modal_finalizar()
        
    def consultar_produto(self, event=None):
        codigo_consulta = StringVar()

        consulta = ctk.CTkToplevel(self.frame_conteudo, fg_color="#1e1e1e")

        consulta.bind("<Escape>", lambda e: self.fechar_modal(consulta))

        consulta.title("Consultar produto")
        consulta.geometry("700x700")

        consulta.transient(self.frame_conteudo)
        consulta.update_idletasks()
        consulta.grab_set()   

        consulta.columnconfigure(0, weight=1)
        consulta.rowconfigure((0,1,2), weight=1)
        header =  ctk.CTkFrame(consulta, fg_color="#1e1e1e")
        entrys =  ctk.CTkFrame(consulta, fg_color="#1e1e1e")
        informacoes = ctk.CTkFrame(consulta, fg_color="#1e1e1e")

        header.grid(row=0, column=0)

        entrys.rowconfigure(0, weight=1)
        entrys.columnconfigure(0, weight=1)
        entrys.grid(row=1, column=0)

        informacoes.rowconfigure((0,1), weight=1)
        informacoes.columnconfigure((0,1,2), weight=1)
        informacoes.grid(row=2, column=0, sticky="nsew")   

        ctk.CTkLabel(header, 
                     text="Digite o código do produto",
                     font=("arial", 32, "bold")
                     ).grid(row=0, column=0, columnspan=2)
        
        entry = ctk.CTkEntry(entrys,
                         textvariable=codigo_consulta,
                         font=("Arial", 20, "bold"),
                         width=400,
                         height=50)
        entry.grid(row=0, column=0)
        entry.focus_set()

        #label produto
        ctk.CTkLabel(informacoes,
                     text="Produto",
                     font=("arial", 32, "bold")
                     ).grid(row=0, column=0)
        
        #label valor
        ctk.CTkLabel(informacoes,
                     text="Valor",
                     font=("arial", 32, "bold")
                     ).grid(row=0, column=1)
        
        #label quantidade
        ctk.CTkLabel(informacoes,
                     text="Quantidade",
                     font=("arial", 32, "bold")
                     ).grid(row=0, column=2)

        #label info nome
        nome = ctk.CTkLabel(informacoes,
                    text="",
                    font=("arial", 32, "bold")
                    )
        nome.grid(row=1, column=0,  padx=10, pady=20)

        #label info preço
        preco = ctk.CTkLabel(informacoes,
                    text="",
                    font=("arial", 32, "bold")
                    )
        preco.grid(row=1, column=1,  padx=10, pady=20)

        #label info quantidade
        quantidade = ctk.CTkLabel(informacoes,
                    text="",
                    font=("arial", 32, "bold")
                    )
        quantidade.grid(row=1, column=2,  padx=10, pady=20)

        entry.bind("<Return>", lambda e: self.controller.consultar_produto(codigo_consulta.get(), nome, quantidade, preco))

    def mudar_compra(self, event=None):
        if self.controller.alternar_compra():
            self.atualizar_tabela()
            self.atualizar_total()

    def setar_status(self, resultado, label_status=None, var_status=None):
        if resultado is None:
            return
        
        if label_status:
            label_status.configure(text_color=resultado.cor)
       
        if var_status:
            var_status.set(resultado.mensagem)
            self.after(resultado.tempo, lambda: var_status.set(""))

    def voltar(self, event=None):
        resultado = self.referencia_main.caixa.validar_compra_existente()

        if resultado.sucesso == False:
            self.status.set(resultado.mensagem)
            return
            
        self.master.unbind("<Escape>")

        if self.on_sair == self.referencia_main.fechar_app:
            self.status.set("Fechando aplicativo")

        self.on_sair()

    def limpar_campos(self):
        campos = [
            self.codigo
            ]

        for var in campos:
            var.set("")

class CaixaController:
    def __init__(self, tela, ref_caixa):
        self.tela = tela
        self.ref_caixa = ref_caixa
    
    def excluir_item(self):
        """Recebe a linha clicada pelo usuario e exclui do caixa"""

        #seleção de linha
        selecionado = self.tela.tabela.selection()

        if not selecionado:
            return

        item_id = selecionado[0] #id do item
        valores = self.tela.tabela.item(item_id, "values") #valores do item

        self.ref_caixa.excluir_do_carrinho(int(valores[0]))
        self.tela.atualizar_tabela()
        self.tela.atualizar_total()

    def enviar_codigo(self, event=None):
        """Envia o codigo para a classe caixa e valida se existe no estoque"""

        code = self.tela.codigo.get()

        if code == "":
            self.tela.abrir_modal_finalizar()
            return
    
        quantidade = self.tela.quantidade.get()    
        resultado = self.ref_caixa.validar_codigo(code, quantidade)
        
        self.tela.codigo.set("")
        self.tela.quantidade.set(1)
        self.tela.status.set("")
        self.tela.atualizar_tabela()
        self.tela.atualizar_total()

        return resultado

    def enviar_recibo(self, linhas):
        self.tela.metodo_pagamento = "Dinheiro"
        cpf = self.tela.cpf.get()
        if cpf == "n":
            return
        
        self.ref_caixa.imprimir_recibo(linhas, cpf)
        self.tela.fechar_modal(self.tela.modal)

    def consultar_produto(self, codigo, label_nome, label_quantidade, label_preco):     
        produto = self.tela.referencia_main.estoque.get_produto(codigo)

        _, _, nome, _, preco, _, quantidade, _, _ = produto

        label_nome.configure(text=nome)
        label_preco.configure(text=f"R$ {preco:.2f}")
        label_quantidade.configure(text=quantidade)

    def dar_desconto(self, valor):
        total = self.ref_caixa.aplicar_desconto(valor)

        if hasattr(total, "mensagem"):
             self.tela.total_var.set(f"Total: R$ {self.ref_caixa.aplicar_desconto(0):.2f}")
             return total #total aqui é um objeto da classe Resultado
        
        if total:
            self.tela.total_var.set(f"Total: R$ {total:.2f}")

    def alternar_compra(self):
        resultado = self.ref_caixa.alternar_compra()

        if resultado == "Pendente":
            self.tela.compra_pendente.set("Venda pendente no f7")
            return True

        if resultado == "Retomou":
            self.tela.compra_pendente.set("")
            return True
        
        else:
            self.tela.compra_pendente.set("")
            return False
        
    def adicionar_ao_carrinho(self):
        selecionado = self.tela.tabela_estoque.selection()

        if not selecionado:
            return
        
        item_id = selecionado[0] #codigo do item
        valores = self.tela.tabela_estoque.item(item_id, "values")

        produto = self.tela.referencia_main.estoque.get_produto(valores[0])
        self.ref_caixa.validar_codigo(produto[1])
        self.tela.atualizar_tabela()
        self.tela.atualizar_total()
        return
