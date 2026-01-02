from tkinter import ttk
from tkinter import *

class CaixaMenu(ttk.Frame):

    def __init__(self, root, referencia_main):
        super().__init__(root, padding=10)
        self.referencia_main = referencia_main
        
        #textos
        self.status = StringVar()

        #entradas
        self.codigo = StringVar()
        self.valor_pago = StringVar()

        #frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.frame_conteudo = ttk.Frame(self)
        self.frame_conteudo.grid(row=0, column=0, sticky="nsew")
        self.frame_conteudo.columnconfigure(0,weight=1)
        self.pode_usar_atalho = False
        self.mapa_telas = {1: self.tela_codigo,
                               2: self.tela_finalizar_compra,
                               3: self.voltar}
        self.menu()

    def menu(self):
        self.limpar_tela()
        self.pode_usar_atalho = True

        ttk.Label(self.frame_conteudo, text="""
        Menu do caixa
        """, font=("Arial",16)).grid(column=0, row=0, pady=20)

        ttk.Button(self.frame_conteudo, 
                   text="Ler código", 
                   width=50, 
                   padding=30, 
                   command=lambda: self.escolha(1)
                   ).grid(column=0, row=1, pady=10)
        
        ttk.Button(self.frame_conteudo, 
                   text="Finalizar compra", 
                   width=50, 
                   padding=30, 
                   command=lambda: self.escolha(2)
                   ).grid(column=0, row=2, pady=10)
        
        ttk.Button(self.frame_conteudo, 
                   text="Sair", 
                   width=50, 
                   padding=30, 
                   command=lambda: self.escolha(3)
                   ).grid(column=0, row=3, pady=10)
                                         
        ttk.Label(self.frame_conteudo, textvariable=self.status).grid(column=0, row=4, pady=10)

        
    def escolha(self, escolha):
        try:
            escolha = int(escolha)

        except ValueError:
            self.status.set("Digite apenas numeros inteiros")
            return
            
        escolhido = self.mapa_telas.get(escolha, "Opção inválida")
        self.pode_usar_atalho = False
           
        escolhido()


    def tela_codigo(self):
        self.limpar_tela() 

        entry_codigo = ttk.Entry(self.frame_conteudo, 
                  width=30, 
                  textvariable=self.codigo
                  )
        entry_codigo.grid(row=1, column=0, pady=5)
        entry_codigo.focus_set()
        entry_codigo.bind("<Return>", lambda e: self.enviar_codigo())
        entry_codigo.bind("<Escape>", lambda e: self.menu())

        ttk.Label(self.frame_conteudo, 
                  text="Digite o código do produto", 
                  font=20
                  ).grid(column=0, row=0, pady=5)

        ttk.Label(self.frame_conteudo, 
                  textvariable=self.status
                  ).grid(column=0, row=4, pady=5)

        ttk.Button(self.frame_conteudo, 
                   text="Enviar", 
                   width=50, 
                   padding=30, 
                   command=self.enviar_codigo
                   ).grid(column=0, row=2, pady=5)

        ttk.Button(self.frame_conteudo, 
                   text="Voltar", 
                   width=50, 
                   padding=30, 
                   command=self.menu
                   ).grid(column=0, row=3, pady=5)

    def tela_finalizar_compra(self):
        self.limpar_tela()

        entry_valor_pago = ttk.Entry(self.frame_conteudo, 
                  width=30, 
                  textvariable=self.valor_pago
                  )
        entry_valor_pago.grid(column=0, row=1, pady=5)
        entry_valor_pago.focus_set()
        entry_valor_pago.bind("<Return>", lambda e: self.finalizar_compra())
        entry_valor_pago.bind("<Escape>", lambda e: self.menu())

        ttk.Label(self.frame_conteudo, 
                  text="Digite o valor", 
                  font=20
                  ).grid(column=0, row=0, pady=5)

        ttk.Label(self.frame_conteudo, 
                  foreground="red", 
                  textvariable=self.status
                  ).grid(column=0, row=4, pady=5)

        ttk.Button(self.frame_conteudo, 
                   text="Finalizar", 
                   width=50, 
                   padding=30, 
                   command=self.finalizar_compra
                   ).grid(column=0, row=2, pady=5)

        ttk.Button(self.frame_conteudo, 
                   text="Voltar", 
                   width=50, 
                   padding=30, 
                   command=self.menu
                   ).grid(column=0, row=3, pady=5)


    def voltar(self):
        resultado = self.referencia_main.caixa.validar_compra_existente()

        if resultado["sucesso"]:
            self.status.set(resultado["mensagem"])
            return
                
        self.referencia_main.voltar_menu_principal()

    def enviar_codigo(self):
        try:
            code = int(self.codigo.get())
        except ValueError:
            self.status.set("Digite apenas numeros")
            return
        
        if not self.referencia_main.caixa.validar_codigo(code):
            self.status.set("Produto não encontrado")
            return
        
        self.status.set("Produto registrado")

    def finalizar_compra(self):

        valor_pago = self.valor_pago.get()

        resultado = self.referencia_main.caixa.finalizar_compra(valor_pago)

        if not resultado["sucesso"]:
            self.status.set(f"{resultado['mensagem']}")
            return
        
        self.status.set(f"Total: {resultado['total']:.2f}, Troco: {resultado['troco']:.2f}")

    def limpar_tela(self):
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

        campos = [self.status,
            self.codigo,
            self.valor_pago
            ]

        for var in campos:
            var.set("")

     
    def teclas_menu(self, tecla):
        if tecla.char in ["1", "2", "3"] and self.pode_usar_atalho:
            self.escolha(int(tecla.char))