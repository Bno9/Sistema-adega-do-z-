from tkinter import ttk
from tkinter import *

class EstoqueMenu(ttk.Frame):

    def __init__(self, root, referencia_main):
        super().__init__(root, padding=10)
        self.referencia_main = referencia_main

        #textos
        self.error= StringVar()

        #entradas
        self.opcao = StringVar()
        self.codigo = StringVar()

        #frame
        self.frame_conteudo = ttk.Frame(self)
        self.frame_conteudo.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.menu()

    def menu(self):
        self.limpar_tela()
        
        ttk.Label(self.frame_conteudo, text="""
        Menu do estoque
        
        1- Ver estoque
        2- Remover produto 
        3- Sair
        """).grid(column=0, row=0, sticky=(W,E))

        ttk.Entry(self.frame_conteudo, textvariable=self.opcao).grid(column=0, row=1, sticky=(W,E))

        ttk.Button(self.frame_conteudo, text="Enviar", command=self.escolha).grid(column=1, row=1, sticky=(W,E))

    def escolha(self):
        try:
            escolha = int(self.opcao.get())
        except ValueError:
            self.error.set("Digite apenas numeros")
            return

        self.limpar_tela()

        if escolha == 1:
            ttk.Label(self.frame_conteudo, textvariable=self.error).grid(column=0, row=0, sticky=(W,E))
            
            self.referencia_main.estoque.listar_itens()

            ttk.Button(self.frame_conteudo, text="Voltar", command=self.menu).grid(row=1, column=1, sticky=(W,E))

        elif escolha == 2:
            ttk.Label(self.frame_conteudo, text="Digite o código do produto que deseja remover").grid(column=0, row=0, sticky=(W,E))

            ttk.Entry(self.frame_conteudo, textvariable=self.codigo).grid(column=0, row=1, sticky=(W,E))
           
            ttk.Button(self.frame_conteudo, text="Enviar", command=self.deletar).grid(column=2, row=2, sticky=(W,E))

            ttk.Button(self.frame_conteudo, text="Voltar", command=self.menu).grid(column=1, row=2, sticky=(W,E))


        elif escolha == 3:
            self.referencia_main.voltar_menu_principal()

        else:
            self.error.set("Escolha uma das opções disponiveis")

    def deletar(self):
        try:
            codigo = int(self.codigo.get())
            self.error.set(self.referencia_main.estoque.remover_produto(codigo))
        except ValueError:
            self.error.set("Digite apenas numeros")
            return

    def limpar_tela(self):
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

        campos = [self.error,
            self.opcao
            ]

        for var in campos:
            var.set("")