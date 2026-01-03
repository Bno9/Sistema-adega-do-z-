from tkinter import ttk
from tkinter import *

class ProdutoMenu(ttk.Frame):

        def __init__(self, root, referencia_main):
            super().__init__(root, padding=10)
            self.referencia_main = referencia_main

            #textos
            self.status = StringVar()

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
            self.mapa_telas = {1: self.tela_cadastro,
                               2: self.tela_editar,
                               3: self.tela_excluir,
                               4: self.voltar}
            self.pode_usar_atalho = False

            #frame
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)

            self.frame_conteudo = ttk.Frame(self)
            self.frame_conteudo.grid(row=0, column=0, sticky="nsew")
            self.frame_conteudo.columnconfigure(0, weight=1)

            self.menu()

        #telas

        def menu(self):
            self.limpar_tela()
            self.pode_usar_atalho = True

            buttons = [("Cadastrar produto", 1),
                       ("Editar produto", 2),
                       ("Excluir produto", 3),
                       ("Voltar", 4)]
            
            #label principal
            ttk.Label(self.frame_conteudo, 
                      text="""
                      Menu de cadastro de produtos
                      """, 
                      font=("Arial", 16),  
                      anchor="center", 
                      padding=20
                      ).grid(column=0, row=0, pady=20)
            
            #label status
            ttk.Label(self.frame_conteudo, 
                      textvariable=self.status,
                      foreground="red"
                      ).grid(column=0, row=6, pady=20)
            
            #botoes de escolha
            for i, (texto, comando) in enumerate(buttons, start=2):
                ttk.Button(self.frame_conteudo, 
                        text=texto, 
                        width=50, 
                        padding=30, 
                        command=lambda c=comando: self.escolha_tela(c)
                        ).grid(column=0, row=i, pady=20)
                
            self.bind_all("<Escape>", lambda e: self.voltar())

        def escolha_tela(self, escolha):
            try:
                escolha = int(escolha)
            except ValueError:
                self.status.set("Digite apenas numeros")
                return
            
            escolhido = self.mapa_telas.get(escolha, "Escolha uma das opções disponiveis")
            self.pode_usar_atalho = False

            self.limpar_tela()

            escolhido()

        def tela_cadastro(self):
            self.unbind_all("<Escape>")

            #frame para tela de cadastro
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

            #label principal
            ttk.Label(form_frame, 
                      text="Digite as informações do produto", 
                      font=12, 
                      anchor="center"
                      ).grid(column=0, row=0, columnspan=2, pady=20)

            
            #labels/entrys
            for i, (texto, variavel) in enumerate(campos, start=2):
                ttk.Label(form_frame, 
                          width=10, 
                          text=texto, 
                          anchor="e", 
                          font=12
                          ).grid(column=0, row=i, sticky="e", pady=5, padx=10)


                entry = ttk.Entry(form_frame, 
                                  textvariable=variavel, 
                                  width=30)
                
                entry.grid(row=i, 
                           column=1, 
                           pady=5, 
                           padx=10, 
                           sticky="w")
                    
                self.entries.append(entry)

            #teclas para mudar campo
            for i, entry in enumerate(self.entries):
                entry.bind("<Return>", lambda e, idx=i: self.proximo_campo(idx)) #enter
                entry.bind("<Down>", lambda e, idx=i: self.proximo_campo(idx)) #seta pra baixo
                entry.bind("<Up>", lambda e, idx=i: self.campo_anterior(idx)) #seta pra cima
                entry.bind("<Escape>", lambda e, idx=i: self.menu())

            #label status
            ttk.Label(form_frame, 
                      textvariable=self.status, 
                      foreground="red"
                      ).grid(column=0, row=len(campos)+5, columnspan=2, pady=10)

            #botao cadastrar
            ttk.Button(form_frame, 
                       width=30, 
                       padding=20, 
                       text="Cadastrar", 
                       command=self.criar
                       ).grid(column=0, row= len(campos)+2, columnspan=2, pady=10)
            
            #botao voltar
            ttk.Button(form_frame, 
                       width=30, 
                       padding=20, 
                       text="Voltar", 
                       command=self.menu
                       ).grid(column=0, row= len(campos)+3, columnspan=2)

            self.entries[0].focus_set()

        def tela_editar(self):
            self.unbind_all("<Escape>")

            #frame tela editar
            frame = ttk.Frame(self.frame_conteudo)
            frame.grid(column=0, row=0, pady=40)
            
            #label principal
            ttk.Label(frame,
                    text="Digite o código do produto", 
                    font=16
                    ).grid(column=0, row=0, pady=20)

            #label status
            ttk.Label(frame, 
                      width=30, 
                      textvariable=self.status,
                      foreground="red"
                      ).grid(row=2, column=0, pady=20)

            #entry código
            entry_codigo = ttk.Entry(frame, 
                      width=30, 
                      textvariable=self.codigo
                      )
            entry_codigo.grid(column=0, row=1, pady=20)
            entry_codigo.focus_set()
            entry_codigo.bind("<Escape>", lambda e: self.menu())
            entry_codigo.bind("<Return>", lambda e: self.editar())

            #botao editar
            ttk.Button(frame, 
                       width=50, 
                       padding=30, 
                       text="Editar Produto", 
                       command=self.editar
                       ).grid(column=0, row= 3, pady=20)

            #botao voltar
            ttk.Button(frame, 
                       width=50, 
                       padding=30, 
                       text="Voltar", 
                       command=self.menu
                       ).grid(column=0, row= 4, pady=20)


        def tela_excluir(self):
            self.unbind_all("<Escape>")

            #frame tela excluir
            frame = ttk.Frame(self.frame_conteudo)
            frame.grid(column=0, row=0, pady=40)

            #label principal
            ttk.Label(frame, 
                      text="Digite o código do produto que deseja remover"
                      ).grid(column=0, row=0, pady=20)
            
            #label status
            ttk.Label(frame, 
                      textvariable=self.status
                      ).grid(column=0, row=4, pady=20)

            #entry codigo
            entry_codigo = ttk.Entry(frame, 
                      width=30, 
                      textvariable=self.codigo
                      )
            
            entry_codigo.grid(column=0, row=1, pady=20)
            entry_codigo.focus_set()
            entry_codigo.bind("<Escape>", lambda e: self.menu())
            entry_codigo.bind("<Return>", lambda e: self.deletar())
            
            #botao enviar
            ttk.Button(frame, 
                       text="Enviar", 
                       width=50, 
                       padding=30, 
                       command=self.deletar
                       ).grid(column=0, row=2, pady=20)

            #botao voltar
            ttk.Button(frame, 
                       text="Voltar", 
                       width=50, 
                       padding=30, 
                       command=self.menu
                       ).grid(column=0, row=3, pady=20)

        def voltar(self):
            self.referencia_main.voltar_menu_principal()


        #métodos
 
        def criar(self):
                """Recebe as entradas e envia para a classe estoque criar e salvar o produto"""
                self.unbind_all("<Escape>")
                try:
                    codigo = int(self.codigo.get())
                    nome = self.nome.get()
                    preco_custo = float(self.preco_custo.get())
                    preco_venda = float(self.preco_venda.get())
                    quantidade = int(self.quantidade.get())
                
                except ValueError:
                    self.status.set("Digite apenas numeros")
                    return
        
                resultado = self.referencia_main.estoque.criar_produto(codigo,nome,preco_custo,preco_venda,quantidade)

                self.status.set(resultado)

                self.frame_conteudo.after(2000, self.limpar_campos)

        def editar(self):
            """Recebe o valor e altera o atributo do produto"""
            self.unbind_all("<Escape>")
            try:
                codigo_produto = int(self.codigo.get())
            except ValueError:
                self.status.set("Digite apenas numeros")

            if not self.referencia_main.estoque.conferir_se_existe_no_estoque(codigo_produto):
                self.status.set("Produto não encontrado")
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

            #label escolha
            ttk.Label(self.frame_conteudo, text="""Escolha o que deseja alterar""").grid(column=0, row=0, sticky="ew")
            
            #botões de escolha
            for i, (opcao, texto) in enumerate(mapa, start=2):
                ttk.Button(self.frame_conteudo, text=texto, width=30, padding=30, command=lambda: self.processar_escolha(opcao)).grid(column=0, row=i, pady=20)
         
            #botao cancelar
            ttk.Button(self.frame_conteudo,
                       text="Cancelar",
                       width=30,
                       padding=30,
                       command=self.menu).grid(column=0, row=len(mapa)+1, pady=20)

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
                self.status.set("Escolha inválida")
                return

            self.atributo = mapa[escolha]

            self.limpar_tela()
            self.limpar_campos()

            #label novo valor
            ttk.Label(self.frame_conteudo, 
                      text="Digite o novo valor"
                      ).grid(column=0, row=0, pady=20)
            
            #label status
            ttk.Label(self.frame_conteudo, 
                      textvariable=self.status
                      ).grid(column=0, row=4, pady=20)
            
            #entry novo valor
            entry_foco = ttk.Entry(self.frame_conteudo, 
                      textvariable=self.novo_valor
                      )
            entry_foco.grid(column=0, row=1, pady=20)
            entry_foco.focus_set()
            entry_foco.bind("<Escape>", lambda e: self.menu())
            entry_foco.bind("<Return>", lambda e: self.salvar_alteracao())
            
            #botao salvar
            ttk.Button(self.frame_conteudo,
                    text="Salvar", 
                    command=self.salvar_alteracao,
                    width=30,
                    padding=30
                    ).grid(column=0, row=2, pady=20)
            
            #botao cancelar
            ttk.Button(self.frame_conteudo, 
                       text="Cancelar", 
                       command=self.menu,
                       width=30,
                       padding=30
                       ).grid(column=0, row=3, pady=20)



        def salvar_alteracao(self):
            valor = self.novo_valor.get()

            try:
                if self.atributo in ["codigo", "quantidade"]:
                    valor = int(valor)
                elif self.atributo in ["preco_custo", "preco_venda"]:
                    valor = float(valor)
            except ValueError:
                self.status.set("Valor inválido") #isso aparece sempre que tento editar o nome
                return

            setattr(self.produto, self.atributo, valor)
            self.status.set("Produto alterado com sucesso!") #nao ta alterando codigo nem nome

        def deletar(self):
            try:
                codigo = int(self.codigo.get())
                self.status.set(self.referencia_main.estoque.remover_produto(codigo))
            except ValueError:
                self.status.set("Digite apenas numeros")
                return
            

        
        #métodos tela e campo

        def limpar_tela(self):
            for widget in self.frame_conteudo.winfo_children():
                widget.destroy()
            self.limpar_campos()

        def limpar_campos(self):
            campos = [self.status,
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
                """Muda o foco do entry pro proximo"""
                if indice + 1 < len(self.entries):
                    self.entries[indice + 1].focus_set()
                else:
                    self.criar()
                    self.entries[0].focus_set()

        def campo_anterior(self, indice):
            "Muda o foco do entry pro anterior"
            if indice - 1 >= 0:
                self.entries[indice - 1].focus_set()


        def teclas_menu(self, tecla):
            if tecla.char in ["1", "2", "3", "4"] and self.pode_usar_atalho:
                self.escolha_tela(int(tecla.char))