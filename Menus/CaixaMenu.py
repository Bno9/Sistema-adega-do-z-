from tkinter import ttk
from tkinter import *

class CaixaMenu(ttk.Frame):

    def __init__(self, root, referencia_main):
        super().__init__(root, padding=10)
        self.referencia_main = referencia_main
        
        #textos
        self.error = StringVar()

        #entradas
        self.codigo = StringVar()
        self.valor_pago = StringVar()

        #frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.frame_conteudo = ttk.Frame(self)
        self.frame_conteudo.grid(row=0, column=0, sticky="nsew")
        self.frame_conteudo.columnconfigure(0,weight=1)
        self.menu()

    def menu(self):
        self.limpar_tela()

        ttk.Label(self.frame_conteudo, text="""
        Menu do caixa
        """, font=("Arial",16)).grid(column=0, row=0, pady=20)

        ttk.Button(self.frame_conteudo, text="Ler código", width=50, padding=30, command=lambda: self.escolha(1)).grid(column=0, row=1, pady=10)
        ttk.Button(self.frame_conteudo, text="Finalizar compra", width=50, padding=30, command=lambda: self.escolha(2)).grid(column=0, row=2, pady=10)
        ttk.Button(self.frame_conteudo, text="Sair", width=50, padding=30, command=lambda: self.escolha(3)).grid(column=0, row=3, pady=10)
                                         
        ttk.Label(self.frame_conteudo, textvariable=self.error).grid(column=0, row=4, pady=10)

        
    def escolha(self, opcao):
        try:
            opcao = int(opcao)

        except ValueError:
            self.error.set("Digite apenas numeros inteiros")
            return

            
        if opcao == 1:
            self.limpar_tela()

            ttk.Entry(self.frame_conteudo, width=30, textvariable=self.codigo).grid(row=1, column=0, pady=5)

            ttk.Label(self.frame_conteudo, text="Digite o código do produto", font=20).grid(column=0, row=0, pady=5)

            ttk.Label(self.frame_conteudo, textvariable=self.error).grid(column=0, row=4, pady=5)

            ttk.Button(self.frame_conteudo, text="Enviar", width=50, padding=30, command=self.enviar_codigo).grid(column=0, row=2, pady=5)

            ttk.Button(self.frame_conteudo, text="Voltar", width=50, padding=30, command=self.menu).grid(column=0, row=3, pady=5)

        elif opcao == 2:
            self.limpar_tela()

            ttk.Entry(self.frame_conteudo, width=30, textvariable=self.valor_pago).grid(row=1, column=0, pady=5)

            ttk.Label(self.frame_conteudo, text="Digite o valor", font=20).grid(row=0, column=0, pady=5)

            ttk.Label(self.frame_conteudo, foreground="red", textvariable=self.error).grid(column=0, row=4, pady=5)

            ttk.Button(self.frame_conteudo, text="Finalizar", width=50, padding=30, command=self.finalizar_compra).grid(column=0, row=2, pady=5)

            ttk.Button(self.frame_conteudo, text="Voltar", width=50, padding=30, command=self.menu).grid(column=0, row=3, pady=5)

        elif opcao == 3:
            resultado = self.referencia_main.caixa.validar_compra_existente()

            if not resultado["sucesso"]:
                self.error.set(resultado["mensagem"])
                return
                
            self.referencia_main.voltar_menu_principal()

        else:
            self.error.set("Opção inválida")

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

    def limpar_tela(self):
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

        campos = [self.error,
            self.codigo,
            self.valor_pago
            ]

        for var in campos:
            var.set("")

     
#Falta terminar de arrumar a interface aqui e depois fazer umas mudanças

#Tirar esses botoes de ler código ou não sei oq

#Todo o caixa vai funcionar por tecla

#Esc vai sair e voltar pro menu principal

#Enter com código vai enviar o código direto e mostrar o item na tela junto do total

#Enter sem o código vai tentar finalizar a compra (e vai precisar de confrmação)