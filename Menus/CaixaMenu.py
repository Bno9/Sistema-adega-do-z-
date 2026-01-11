from tkinter import ttk
from tkinter import *
import customtkinter as ctk

class CaixaMenu(ctk.CTkFrame):

    def __init__(self, root, referencia_main):
        super().__init__(master=root, fg_color="#1e1e1e")
        self.referencia_main = referencia_main
        self.controller = CaixaController(self, self.referencia_main.caixa)
        
        #textos
        self.status = StringVar()
        self.total_var = StringVar()

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
        self.entry_codigo.bind("<Return>", self.controller.enviar_codigo)
        self.entry_codigo.bind("<Right>", lambda e: self.entry_quantidade.focus())

        ctk.CTkLabel(
        self.header,
        text="Código do produto",
        text_color="white",
        fg_color="#1e1e1e",
        font=("arial", 24, "bold")
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)

        #entry/label quantidade
        self.entry_quantidade = ctk.CTkEntry(
            self.header,
            textvariable=self.quantidade,
            width=300,
            font=("Arial", 20, "bold")
        )
        self.entry_quantidade.grid(row=1, column=2, sticky="e", padx=10, pady=10)
        self.entry_quantidade.bind("<Return>", self.controller.enviar_codigo)
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
        ctk.CTkLabel(
            self.header,
            textvariable=self.status,
            text_color="white",
            fg_color="#1e1e1e",
            font=("arial", 32, "bold")
        ).grid(row=1, column=1, padx=10)

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
        
        #binds
        self.master.bind("<F10>", self.consultar_produto)
        self.master.bind("<Escape>", self.voltar)
        self.tabela.bind("<Delete>", lambda e: self.excluir_item())

        #carregar layout
        self.atualizar_tabela()
        self.atualizar_total()

    
    #Telas
    
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
        self.status_modal = StringVar()
        self.troco_modal = StringVar()
        
        self.modal = ctk.CTkToplevel(self.frame_conteudo, fg_color="#1e1e1e")
        self.modal.title("Finalizar compra")
        self.modal.geometry("300x330")
        self.modal.resizable(False, False)

        self.modal.transient(self.frame_conteudo)
        self.modal.focus_force()
        self.modal.update_idletasks() 
        self.modal.grab_set()
        self.modal.rowconfigure((0,1,2), weight=1)
        self.modal.columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self.modal, fg_color="#1e1e1e")
        entry = ctk.CTkFrame(self.modal, fg_color="#1e1e1e")
        botoes = ctk.CTkFrame(self.modal, fg_color="#1e1e1e")

        botoes.columnconfigure((0,1,2), weight=1)
        header.rowconfigure((0,1), weight=1)

        header.grid(column=0, row=0)
        entry.grid(column=0, row=1)
        botoes.grid(column=0, row=2)


        self.status_modal.set("")
        self.modal.bind("<Escape>", lambda e: self.fechar_modal(self.modal))
        
        #criação botão ok
        self.botao_ok = ctk.CTkButton(
            botoes,
            text="OK",
            text_color="black", 
            corner_radius=20,
            border_color="black",
            hover_color="white",
            width=70,  
            height=70,
            font=("Arial", 16, "bold"),
            fg_color="orange",
            command=self.pedir_cpf
            )

        #label status modal
        ctk.CTkLabel(
            header,
            textvariable=self.status_modal,
            text_color="red",
            fg_color="#1e1e1e",
            font=("arial", 20, "bold")
        ).grid(row=0, column=0, pady=5)

        #label valor pago
        ctk.CTkLabel(
            header,
            text="Valor pago",
            textvariable=self.troco_modal,
            text_color="white",
            fg_color="#1e1e1e",
            font=("Arial", 32, "bold")
        ).grid(row=1, column=0, pady=5)
        self.troco_modal.set("Valor pago")

        #entry valor pago
        self.entry_valor_pago = ctk.CTkEntry(
            entry,
            textvariable=self.valor_pago,
            width=300,
            font=("Arial", 20, "bold")
        )
        self.entry_valor_pago.grid(row=0, column=0, pady=5)
        self.entry_valor_pago.focus_set()
        self.entry_valor_pago.bind("<Return>", lambda e: self.finalizar_compra())
        self.entry_valor_pago.bind("<Escape>", lambda e: self.fechar_modal(self.modal))


        #botao finalizar compra
        self.botao_finalizar = ctk.CTkButton(
            botoes,
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
            command=self.finalizar_compra
        )
        self.botao_finalizar.grid(row=0, column=0, pady=10)

        #botao fechar modal
        self.botao_cancelar = ctk.CTkButton(
            botoes,
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

    def finalizar_compra(self):
        """chama o metodo da classe caixa que finaliza a compra"""

        self.resultado = self.referencia_main.caixa.finalizar_compra(self.valor_pago.get())

        if not self.resultado["sucesso"]:
            self.status_modal.set(self.resultado["mensagem"])
            return

        self.troco_modal.set(
            f"""Valor pago
R${int(self.valor_pago.get()):.2f}


Troco: R$ {self.resultado['troco']:.2f}""")
        
        self.botao_ok.grid(column=0, row=0)

        self.master.bind("<Escape>", lambda e: self.fechar_modal(self.modal))
        self.modal.bind("<Return>", lambda e: self.pedir_cpf())

        self.valor_pago.set("")

        self.entry_valor_pago.destroy()
        self.botao_finalizar.destroy()
        self.botao_cancelar.destroy()

        self.atualizar_tabela()
        self.atualizar_total()
        self.quantidade.set(1)

    def pedir_cpf(self):
        self.botao_ok.destroy()
        self.cpf = ctk.IntVar()

        self.modal.bind("<Return>", lambda e: self.controller.enviar_recibo(self.resultado["linhas"]))

        self.recibo_frame = ctk.CTkFrame(self.modal, fg_color="#1e1e1e")
        self.recibo_frame.grid(column=0, row=0, sticky="nsew")
        self.recibo_frame.rowconfigure((0,1,2,3), weight=1)
        self.recibo_frame.columnconfigure(0, weight=1)

        self.label_cpf = ctk.CTkLabel(
            self.recibo_frame,
            text="Digite o cpf",
            text_color="white",
            fg_color="#1e1e1e",
            font=("arial", 24, "bold")
            ).grid(column=0, row=0, sticky="ew")

        self.entry_cpf = ctk.CTkEntry(self.recibo_frame, 
                                      width=300, 
                                      textvariable=self.cpf,
                                      font=("Arial", 20, "bold"))
        self.entry_cpf.grid(column=0, row=1, sticky="ew")
        self.entry_cpf.focus_set()

        self.botao_enviar = ctk.CTkButton(self.recibo_frame,
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
            command=lambda: self.controller.enviar_recibo(self.resultado["linhas"]))
        self.botao_enviar.grid(column=0, row=2, pady=20)

        self.botao_cancelar = ctk.CTkButton(self.recibo_frame,
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
        self.botao_cancelar.grid(column=0, row=3, pady=20)

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
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for produto, quantidade in self.referencia_main.caixa.itens_no_carrinho:
            self.tabela.insert(
                "",
                "end",
                values=(
                    produto.codigo,
                    produto.nome,
                    f"R$ {produto.preco_venda:.2f}",
                    quantidade
                ))
            
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

        ctk.CTkLabel(informacoes,
                     text="Produto",
                     font=("arial", 32, "bold")
                     ).grid(row=0, column=0)
        
        ctk.CTkLabel(informacoes,
                     text="Valor",
                     font=("arial", 32, "bold")
                     ).grid(row=0, column=1)
        
        ctk.CTkLabel(informacoes,
                     text="Quantidade",
                     font=("arial", 32, "bold")
                     ).grid(row=0, column=2)

        nome = ctk.CTkLabel(informacoes,
                    text="",
                    font=("arial", 32, "bold")
                    )
        nome.grid(row=1, column=0,  padx=10, pady=20)

        preco = ctk.CTkLabel(informacoes,
                    text="",
                    font=("arial", 32, "bold")
                    )
        preco.grid(row=1, column=1,  padx=10, pady=20)

        quantidade = ctk.CTkLabel(informacoes,
                    text="",
                    font=("arial", 32, "bold")
                    )
        quantidade.grid(row=1, column=2,  padx=10, pady=20)

        entry.bind("<Return>", lambda e: self.controller.consultar_produto(codigo_consulta.get(), nome, quantidade, preco))



    def voltar(self, event=None):
        resultado = self.referencia_main.caixa.validar_compra_existente()

        if resultado["sucesso"]:
            self.status.set(resultado["mensagem"])
            return
            
        self.master.unbind("<Escape>")
        self.referencia_main.voltar_menu_principal()

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

        try:
            code = int(self.tela.codigo.get())

        except ValueError:
            self.tela.status.set("")
            return
        
        quantidade = self.tela.quantidade.get()
        
        if not self.ref_caixa.validar_codigo(code, quantidade):
            self.tela.status.set("Produto não encontrado")
            return
        
        self.tela.codigo.set("")
        self.tela.status.set("")
        self.tela.atualizar_tabela()
        self.tela.atualizar_total()

    def enviar_recibo(self, linhas):
        cpf = self.tela.cpf.get()
        self.ref_caixa.imprimir_recibo(linhas, cpf)
        self.tela.fechar_modal(self.tela.modal)

    def consultar_produto(self, codigo, label_nome, label_quantidade, label_preco):
        try:
            codigo = int(codigo)
        except ValueError:
            raise "Erro na conversão"
        
        produto = self.tela.referencia_main.estoque.get_produto(codigo)

        _, _, nome, preco, _, quantidade = produto

        label_nome.configure(text=nome)
        label_preco.configure(text=f"R$ {preco:.2f}")
        label_quantidade.configure(text=quantidade)