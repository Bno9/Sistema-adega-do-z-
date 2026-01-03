from tkinter import ttk
from tkinter import *
import customtkinter as ctk

class CaixaMenu(ctk.CTkFrame):

    def __init__(self, root, referencia_main):
        super().__init__(master=root, fg_color="#1e1e1e")
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

        self.frame_conteudo = ctk.CTkFrame(self, fg_color="#1e1e1e")
        self.frame_conteudo.grid(row=0, column=0, sticky="nsew")
        self.frame_conteudo.columnconfigure(0,weight=1)
        self.frame_conteudo.columnconfigure(1, weight=0)
        self.frame_conteudo.columnconfigure(10, weight=0)
        self.frame_conteudo.rowconfigure(2,weight=1)

        #entry/label codigo
        self.entry_codigo = ctk.CTkEntry(
            self.frame_conteudo,
            textvariable=self.codigo,
            width=300,
            font=("Arial", 20, "bold")
        )
        self.entry_codigo.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.entry_codigo.focus_set()
        self.entry_codigo.bind("<Return>", self.enviar_codigo)
        self.entry_codigo.bind("<Right>", lambda e: self.entry_quantidade.focus())

        ctk.CTkLabel(
        self.frame_conteudo,
        text="Código do produto",
        text_color="white",
        fg_color="#1e1e1e",
        font=("arial", 24, "bold")
        ).grid(row=0, column=0, sticky="w", padx=10)

        self.entry_codigo.grid(row=1, column=0, sticky="w", padx=10)

        #entry/label quantidade
        self.entry_quantidade = ctk.CTkEntry(
            self.frame_conteudo,
            textvariable=self.quantidade,
            width=300,
            font=("Arial", 20, "bold")
        )
        self.entry_quantidade.grid(row=0, column=10, sticky="w", padx=10, pady=10)
        self.entry_quantidade.bind("<Return>", self.enviar_codigo)
        self.entry_quantidade.bind("<Left>", lambda e: self.entry_codigo.focus())

        #label quantidade
        ctk.CTkLabel(
        self.frame_conteudo,
        text="Quantidade",
        text_color="white",
        fg_color="#1e1e1e",
        font=("arial", 24, "bold")
        ).grid(row=0, column=10, sticky="w", padx=10)

        self.entry_quantidade.grid(row=1, column=10, sticky="w", padx=10)

        #label status
        ctk.CTkLabel(
            self.frame_conteudo,
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
        self.scroll = ttk.Scrollbar(self.frame_conteudo)
        self.scroll.grid(row=2, column=1, sticky="ns")

        self.tabela = ttk.Treeview(
            self.frame_conteudo,
            columns=("codigo", "nome", "preco", "quantidade"),
            show="headings",
            selectmode="browse",
            style="Custom.Treeview",
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

        #label total
        ctk.CTkLabel(
            self.frame_conteudo,
            textvariable=self.total_var,
            text_color="white",
            fg_color="#1e1e1e",
            font=("Arial", 32, "bold")
        ).grid(row=3, column=0, padx=10, pady=10)

        #botoes finalizar compra
        frame_botoes = ctk.CTkFrame(self.frame_conteudo, fg_color="#1e1e1e")
        frame_botoes.grid(row=4, column=0, pady=10)

        ctk.CTkButton(
            frame_botoes,
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
            frame_botoes,
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
        ).grid(row=0, column=1, padx=10)
        
        #binds
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
        
        self.modal = ctk.CTkToplevel(self.master, fg_color="#1e1e1e")
        self.modal.title("Finalizar compra")
        self.modal.geometry("300x330")
        self.modal.resizable(False, False)

        self.modal.transient(self.master)
        self.modal.grab_set()
        self.modal.focus_force()

        self.status_modal.set("")
        self.master.unbind("<Escape>")
        
        #criação botão ok
        self.botao_ok = ctk.CTkButton(
            self.modal,
            text="OK",
            text_color="black", 
            corner_radius=20,
            border_color="black",
            hover_color="white",
            width=70,  
            height=100,
            font=("Arial", 16, "bold"),
            fg_color="orange",
            command=self.fechar_modal
            )

        #label valor pago
        ctk.CTkLabel(
            self.modal,
            text="Valor pago",
            text_color="white",
            fg_color="#1e1e1e",
            font=("Arial", 20, "bold")
        ).grid(row=0, column=0, pady=5)

        #label status modal
        ctk.CTkLabel(
            self.modal,
            textvariable=self.status_modal,
            text_color="red",
            fg_color="#1e1e1e",
            font=("arial", 20, "bold")
        ).grid(row=4, column=0, pady=5)

        #entry valor pago
        self.entry_valor_pago = ctk.CTkEntry(
            self.modal,
            textvariable=self.valor_pago,
            width=300,
            font=("Arial", 20, "bold")
        )
        self.entry_valor_pago.grid(row=1, column=0, pady=5)
        self.entry_valor_pago.focus_set()
        self.entry_valor_pago.bind("<Return>", lambda e: self.finalizar_compra())
        self.entry_valor_pago.bind("<Escape>", lambda e: self.fechar_modal())


        #botao finalizar compra
        self.botao_finalizar = ctk.CTkButton(
            self.modal,
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
        self.botao_finalizar.grid(row=2, column=0, pady=10)

        #botao fechar modal
        self.botao_cancelar = ctk.CTkButton(
            self.modal,
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
            command=self.fechar_modal
        )
        self.botao_cancelar.grid(row=3, column=0)

    

    #Métodos

    def enviar_codigo(self, event=None):
        """Envia o codigo para a classe caixa e valida se existe no estoque"""

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
        """chama o metodo da classe caixa que finaliza a compra"""
        resultado = self.referencia_main.caixa.finalizar_compra(self.valor_pago.get())

        if not resultado["sucesso"]:
            self.status_modal.set(resultado["mensagem"])
            return

        self.status_modal.set(
            f"""    R${int(self.valor_pago.get()):.2f} 

Troco: R$ {resultado['troco']:.2f}"""
)

        self.botao_ok.grid(row=5, column=0, pady=10)

        self.master.bind("<Return>", lambda e: self.fechar_modal())

        self.entry_valor_pago.destroy()
        self.botao_finalizar.destroy()
        self.botao_cancelar.destroy()

        self.atualizar_tabela()
        self.atualizar_total()
        self.quantidade.set(1)

    def excluir_item(self):
        """Recebe a linha clicada pelo usuario e exclui do caixa"""

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
        
        self.master.unbind("<Escape>")
        self.referencia_main.voltar_menu_principal()

    def fechar_modal(self): #essa função ta dando um erro no ctk que eu não faço ideia do que é, mas pelo menos o programa continua. Vou precisar pesquisar pra arrumar, m
        self.limpar_campos()
        self.entry_codigo.focus_set()
        self.master.bind("<Escape>", self.voltar)
        self.master.unbind("<Return>")
        

        self.modal.grab_release()
        self.modal.destroy()

    def limpar_campos(self):
        campos = [
            self.codigo,
            self.valor_pago
            ]

        for var in campos:
            var.set("")
