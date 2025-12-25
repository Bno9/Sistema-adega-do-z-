from tkinter import ttk
from tkinter import *

class ProdutoMenu(ttk.Frame):

        def __init__(self, root, referencia_main):
            super().__init__(root, padding=10)
            self.referencia_main = referencia_main

            #textos
            self.error = StringVar()

            #entradas
            self.opcao = StringVar()
            self.codigo = StringVar()
            self.nome = StringVar()
            self.preco_custo = StringVar()
            self.preco_venda = StringVar()
            self.quantidade = StringVar()
            self.novo_valor = StringVar()

            #atributos
            self.produto = None
            self.atributo = None

            #frame
            self.frame_conteudo = ttk.Frame(self)
            self.frame_conteudo.grid(row=2, column=0, columnspan=2, sticky="nsew")
            self.menu()

        def menu(self):
            self.limpar_tela()
            
            ttk.Label(self.frame_conteudo, text="""
            Menu de cadastro de produtos
            
            1- Cadastrar produto
            2- Editar produto
            3- Sair
            """).grid(column=0, row=1, sticky="nsew")

            ttk.Entry(self.frame_conteudo, width=10, textvariable=self.opcao).grid(column=0, row=2, sticky=(W,E))

            ttk.Label(self.frame_conteudo, textvariable=self.error).grid(column=2, row=2, sticky=(W, E))

            ttk.Button(self.frame_conteudo, text="Enviar", command=self.escolha).grid(column=3, row=2, sticky=(W,E))

        def escolha(self):

            try:
                escolha = int(self.opcao.get())
            except ValueError:
                self.error.set("Digite apenas numeros")
                return

            self.limpar_tela()

            if escolha == 1:
                from Utils.Produto import Produto


                campos = [("Código", self.codigo),
                    ("Nome", self.nome),
                    ("Preço custo", self.preco_custo),
                    ("Preço venda", self.preco_venda),
                    ("Quantidade", self.quantidade)]

                ttk.Label(self.frame_conteudo, text="Digite as informações do produto").grid(column=0, row=1, sticky=(W,E))

                ttk.Label(self.frame_conteudo, textvariable=self.error).grid(column=3, row=5, sticky=(W,E))

                for i, (texto, variavel) in enumerate(campos, start=2):
                    ttk.Label(self.frame_conteudo, width=10, text=texto).grid(column=1, row=i, sticky=(W,E))
                    ttk.Entry(self.frame_conteudo, width=10, textvariable=variavel).grid(column=0, row=i, sticky=(W,E))


                ttk.Button(self.frame_conteudo, width=10, text="Cadastrar", command=self.criar).grid(column=4, row= 3, sticky=(W,E))
                ttk.Button(self.frame_conteudo, width=10, text="Voltar", command=self.menu).grid(column=4, row= 4, sticky=(W,E))

            elif escolha == 2:

                ttk.Label(self.frame_conteudo, width=10, text="Digite o código do produto").grid(column=0, row=0, sticky=(W,E))
                ttk.Entry(self.frame_conteudo, width=10, textvariable=self.codigo).grid(column=0, row=1, sticky=(W,E))

                ttk.Label(self.frame_conteudo, width=10, textvariable=self.error).grid(row=2, column=2, sticky=(W,E))

                ttk.Button(self.frame_conteudo, width=10, text="Editar Produto", command=self.editar).grid(column=4, row= 3, sticky=(W,E))

            elif escolha == 3:
                self.referencia_main.voltar_menu_principal()

            else:
                self.error.set("Escolha uma das opções disponiveis")
        
        def criar(self):
                try:
                    codigo = int(self.codigo.get())
                    nome = self.nome.get()
                    preco_custo = float(self.preco_custo.get())
                    preco_venda = float(self.preco_venda.get())
                    quantidade = int(self.quantidade.get())
                
                except ValueError:
                    self.error.set("Digite apenas numeros")
                    return
        
                resultado = self.referencia_main.estoque.criar_produto(codigo,nome,preco_custo,preco_venda,quantidade)

                self.error.set(resultado["sucesso"])

        def editar(self):
            try:
                codigo_produto = int(self.codigo.get())
            except ValueError:
                self.error.set("Digite apenas numeros")

            if not self.referencia_main.estoque.conferir_se_existe(codigo_produto):
                self.error.set("Produto não encontrado")
                return

            self.produto = self.referencia_main.estoque.itens[codigo_produto]
 
            self.limpar_tela()

            ttk.Label(self.frame_conteudo, text="""Escolha o que deseja alterar
                    1- Código
                    2- Nome
                    3- Preço custo
                    4- Preço venda
                    5- Quantidade
                    """).grid(column=0, row=0, sticky="nsew")

            ttk.Entry(self.frame_conteudo, width=10, textvariable=self.opcao).grid(row=3, column=0, sticky=(W,E))
            ttk.Button(self.frame_conteudo, text="Confirmar", command=self.processar_escolha).grid(column=0, row=2)
         
        def processar_escolha(self):
            mapa = {
                "1": "codigo",
                "2": "nome",
                "3": "preco_custo",
                "4": "preco_venda",
                "5": "quantidade"
            }

            escolha = self.opcao.get()

            if escolha not in mapa:
                self.error.set("Escolha inválida")
                return

            self.atributo = mapa[escolha]

            self.limpar_tela()

            ttk.Label(self.frame_conteudo, text="Digite o novo valor").grid(column=0, row=0)
            ttk.Entry(self.frame_conteudo, textvariable=self.novo_valor).grid(column=0, row=1)
            ttk.Button(self.frame_conteudo, text="Salvar", command=self.salvar_alteracao).grid(column=0, row=2)



        def salvar_alteracao(self):
            valor = self.novo_valor.get()

            try:
                if self.atributo in ["codigo", "quantidade"]:
                    valor = int(valor)
                elif self.atributo in ["preco_custo", "preco_venda"]:
                    valor = float(valor)
            except ValueError:
                self.error.set("Valor inválido")
                return

            setattr(self.produto, self.atributo, valor)
            self.error.set("Produto alterado com sucesso!")

            self.menu()

        def limpar_tela(self):
            for widget in self.frame_conteudo.winfo_children():
                widget.destroy()

            campos = [self.error,
            self.opcao,
            self.codigo,
            self.nome,
            self.preco_custo,
            self.preco_venda,
            self.quantidade,
            self.novo_valor
            ]

            for var in campos:
                var.set("")

        
#Falta arrumar o visual da interface. Atualmente ela apenas é funcional