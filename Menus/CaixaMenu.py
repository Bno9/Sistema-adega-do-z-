from tkinter import ttk
from tkinter import *

class CaixaMenu(ttk.Frame):

    def __init__(self, root, referencia_main):
        super().__init__(root, padding=10)
        self.referencia_main = referencia_main
        
        self.opcao = StringVar()
        self.codigo = StringVar()
        self.error = StringVar()
        self.valor_pago = StringVar()

        self.frame_conteudo = ttk.Frame(self)
        self.frame_conteudo.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.menu()

    def menu(self):
        self.limpar_tela()

        ttk.Label(self.frame_conteudo, text="""
        Menu do caixa
        
        1- Ler código
        2- Finalizar compra
        3- Sair
        """).grid(column=1, row=1, sticky="nsew")

        ttk.Entry(self.frame_conteudo, width=10, textvariable=self.opcao).grid(row=0, column=1, sticky=(W, E))

        ttk.Button(self.frame_conteudo, text="Enviar", command=self.escolha).grid(column=0, row=0, sticky=(W,E))
                                       
        ttk.Label(self.frame_conteudo, textvariable=self.error).grid(column=1, row=2, sticky=(W, E))

        
    def escolha(self):
        try:
            opcao = int(self.opcao.get())

        except ValueError:
            self.error.set("Digite apenas numeros inteiros")
            return

            
        if opcao == 1:
            self.limpar_tela()

            ttk.Entry(self.frame_conteudo, width=10, textvariable=self.codigo).grid(row=0, column=1, sticky=(W,E))

            ttk.Label(self.frame_conteudo, text="Digite o código do produto").grid(row=0, column=2, sticky=(W,E))

            ttk.Label(self.frame_conteudo, textvariable=self.error).grid(column=1, row=2, sticky=(W, E))

            ttk.Button(self.frame_conteudo, text="Enviar", command=self.enviar_codigo).grid(column=1, row=1, sticky=(W,E))

            ttk.Button(self.frame_conteudo, text="Voltar", command=self.menu).grid(column=2, row=1, sticky=(W,E))

        elif opcao == 2:
            self.limpar_tela()

            ttk.Entry(self.frame_conteudo, width=10, textvariable=self.valor_pago).grid(row=0, column=1, sticky=(W,E))

            ttk.Label(self.frame_conteudo, width=10, text="Digite o valor").grid(row=0, column=2, sticky=(W,E))

            ttk.Label(self.frame_conteudo, textvariable=self.error).grid(column=1, row=2, sticky=(W, E))

            ttk.Button(self.frame_conteudo, text="Finalizar", command=self.finalizar_compra).grid(column=1, row=1, sticky=(W,E))

            ttk.Button(self.frame_conteudo, text="Voltar", command=self.menu).grid(column=2, row=1, sticky=(W,E))

        elif opcao == 3:
            resultado = self.referencia_main.caixa.validar_compra_existente()

            if not resultado["sucesso"]:
                self.error.set(resultado["mensagem"])
                return
                
            self.referencia_main.voltar_menu_principal()

        else:
            self.error.set("Opção inválida")

    
    def limpar_tela(self):
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

    def enviar_codigo(self):
        try:
            code = int(self.codigo.get())
        except ValueError:
            self.error.set("Digite apenas numeros")
            return
        
        if not self.referencia_main.caixa.validar_codigo(code):
            self.error.set("Produto não encontrado")
            return
        
        self.error.set("Produto registrado") #nao é um erro mas nao criei algo pra exibir sucesos

    def finalizar_compra(self):

        valor_pago = self.valor_pago.get()

        resultado = self.referencia_main.caixa.finalizar_compra(valor_pago)

        if not resultado["sucesso"]:
            self.error.set(f"{resultado['mensagem']}")
            return
        
        self.error.set(f"Total: {resultado['total']:.2f}, Troco: {resultado['troco']:.2f}")