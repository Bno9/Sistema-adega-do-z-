from tkinter import ttk
from tkinter import *

class ProdutoMenu(ttk.Frame):

        def __init__(self, root, referencia_main):
            super().__init__(root, padding=10)
            self.referencia_main = referencia_main

            #textos
            self.error = StringVar()

            #entradas
            self.codigo = StringVar()
            self.nome = StringVar()
            self.preco_custo = StringVar()
            self.preco_venda = StringVar()
            self.quantidade = StringVar()
            self.novo_valor = StringVar()

            self.entries = []

            #atributos
            self.produto = None
            self.atributo = None

            #frame
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)

            self.frame_conteudo = ttk.Frame(self)
            self.frame_conteudo.grid(row=0, column=0, sticky="nsew")
            self.frame_conteudo.columnconfigure(0, weight=1)

            self.menu()

        def menu(self):
            self.limpar_tela()
            
            ttk.Label(self.frame_conteudo, text="""
            Menu de cadastro de produtos
                """, font=("Arial", 16),  anchor="center", padding=20).grid(column=0, row=0, pady=20)
            
            ttk.Label(self.frame_conteudo, textvariable=self.error).grid(column=0, row=6, pady=20)

            ttk.Button(self.frame_conteudo, text="Cadastrar produto", width=50, padding=30, command=lambda: self.escolha(1)).grid(column=0, row=2, pady=20)

            ttk.Button(self.frame_conteudo, text="Editar produto", width=50, padding=30, command=lambda: self.escolha(2)).grid(column=0, row=3, pady=20)

            ttk.Button(self.frame_conteudo, text="Excluir produto", width=50, padding=30, command=lambda: self.escolha(3)).grid(column=0, row=4, pady=20)

            ttk.Button(self.frame_conteudo, text="Voltar", width=50, padding=30, command=lambda: self.escolha(4)).grid(column=0, row=5, pady=20)


        def escolha(self, escolha):

            try:
                escolha = int(escolha)
            except ValueError:
                self.error.set("Digite apenas numeros")
                return

            self.limpar_tela()

            if escolha == 1:
                from Utils.Produto import Produto

                form_frame = ttk.Frame(self.frame_conteudo)
                form_frame.grid(row=0, column=0, sticky="n", pady=30)

                form_frame.columnconfigure(0, weight=1)
                form_frame.columnconfigure(1, weight=2)
                for i in range(15):
                    form_frame.rowconfigure(i, weight=1)


                campos = [("Código", self.codigo),
                    ("Nome", self.nome),
                    ("Preço custo", self.preco_custo),
                    ("Preço venda", self.preco_venda),
                    ("Quantidade", self.quantidade)]

                self.entries.clear()

                ttk.Label(form_frame, text="Digite as informações do produto", font=12, anchor="center").grid(column=0, row=0, columnspan=2, pady=20)

                
                for i, (texto, variavel) in enumerate(campos, start=2):
                    ttk.Label(form_frame, width=10, text=texto, anchor="e", font=12).grid(column=0, row=i, sticky="e", pady=5, padx=10)

                    entry = ttk.Entry(form_frame, textvariable=variavel, width=30)
                    entry.grid(row=i, column=1, pady=5, padx=10, sticky="w")
                    self.entries.append(entry)

                #Teclas para mudar campo
                for i, entry in enumerate(self.entries):
                    entry.bind("<Return>", lambda e, idx=i: self.proximo_campo(idx)) #enter
                    entry.bind("<Down>", lambda e, idx=i: self.proximo_campo(idx)) #seta pra baixo
                    entry.bind("<Up>", lambda e, idx=i: self.campo_anterior(idx)) #seta pra cima

                ttk.Label(form_frame, textvariable=self.error, foreground="red").grid(column=0, row=len(campos)+5, columnspan=2, pady=10)

                ttk.Button(form_frame, width=30, padding=20, text="Cadastrar", command=self.criar).grid(column=0, row= len(campos)+2, columnspan=2, pady=10)
                ttk.Button(form_frame, width=30, padding=20, text="Voltar", command=self.menu).grid(column=0, row= len(campos)+3, columnspan=2)

                self.entries[0].focus_set()


            elif escolha == 2:

                ttk.Label(self.frame_conteudo, text="Digite o código do produto", font=16).grid(column=0, row=0, pady=20)
                ttk.Entry(self.frame_conteudo, width=30, textvariable=self.codigo).grid(column=0, row=1, pady=20)

                ttk.Label(self.frame_conteudo, width=30, textvariable=self.error).grid(row=2, column=0, pady=20)

                ttk.Button(self.frame_conteudo, width=50, padding=30, text="Editar Produto", command=self.editar).grid(column=0, row= 3, pady=20)

                ttk.Button(self.frame_conteudo, width=50, padding=30, text="Voltar", command=self.menu).grid(column=0, row= 4, pady=20)

            elif escolha == 3:
                ttk.Label(self.frame_conteudo, text="Digite o código do produto que deseja remover").grid(column=0, row=0, pady=20)

                ttk.Entry(self.frame_conteudo, width=30, textvariable=self.codigo).grid(column=0, row=1, pady=20)
            
                ttk.Button(self.frame_conteudo, text="Enviar", width=50, padding=30, command=self.deletar).grid(column=0, row=2, pady=20)

                ttk.Button(self.frame_conteudo, text="Voltar", width=50, padding=30, command=self.menu).grid(column=0, row=2, pady=20)

            elif escolha == 4:
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

                self.frame_conteudo.after(2000, self.limpar_campos)

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

            mapa = [
                (1, "codigo"),
                (2, "nome"),
                (3, "preco_custo"),
                (4, "preco_venda"),
                (5, "quantidade")
            ]

            ttk.Label(self.frame_conteudo, text="""Escolha o que deseja alterar
                    
                    """).grid(column=0, row=0, sticky="nsew")
            
            for i, (opcao, texto) in enumerate(mapa, start=2):
                ttk.Button(self.frame_conteudo, text=texto, command=lambda: self.processar_escolha(opcao)).grid(column=0, row=i)
         
        def processar_escolha(self, opcao):
            mapa = {
                1: "codigo",
                2: "nome",
                3: "preco_custo",
                4: "preco_venda",
                5: "quantidade"
            }

            escolha = opcao

            if escolha not in mapa:
                self.error.set("Escolha inválida")
                return

            self.atributo = mapa[escolha]

            self.limpar_tela()
            self.limpar_campos()

            ttk.Label(self.frame_conteudo, text="Digite o novo valor").grid(column=0, row=0)
            ttk.Entry(self.frame_conteudo, textvariable=self.novo_valor).grid(column=0, row=1)
            ttk.Button(self.frame_conteudo, text="Salvar", command=self.salvar_alteracao).grid(column=0, row=2)
            ttk.Button(self.frame_conteudo, text="Cancelar", command=self.menu).grid(column=0, row=3)



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
            
            self.limpar_campos() #sempre que eu quiser limpar a tela eu vou querer limpar os campos

        def limpar_campos(self):
            campos = [self.error,
            self.codigo,
            self.nome,
            self.preco_custo,
            self.preco_venda,
            self.quantidade,
            self.novo_valor
            ]

            for var in campos:
                var.set("")

        def proximo_campo(self, indice):
            if indice + 1 < len(self.entries):
                self.entries[indice + 1].focus_set()
            else:
                self.criar()
                self.entries[0].focus_set()

        def campo_anterior(self, indice):
            if indice - 1 >= 0:
                self.entries[indice - 1].focus_set() #aqui posso refatorar depois pra deixar em 1 função só

#aqui falta só arrumar a interface dos ultimos if e metodos