from tkinter import ttk
from tkinter import *

import customtkinter as ctk

class ProdutoMenu(ctk.CTkFrame):

        def __init__(self, root, referencia_main, usuario):
            super().__init__(master=root, fg_color="#1e1e1e")
            self.referencia_main = referencia_main
            self.controller = ProdutoController(self, self.referencia_main.estoque)
            self.usuario = usuario

            #entradas
            self.entries = []

            #atributos
            self.produto = None
            self.pode_usar_atalho = False

            #frame
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)

            self.frame_conteudo = ctk.CTkFrame(self, fg_color="#1e1e1e")
            self.frame_conteudo.grid(row=0, column=0, sticky="nsew")
            self.frame_conteudo.columnconfigure(0, weight=1)
            self.frame_conteudo.rowconfigure(0, weight=1)

            self.menu()

        #telas

        def menu(self):
            self.limpar_tela()
            self.status_menu = StringVar()
            self.coluna_filtro = "nome"
            self.filtro = StringVar()
            self.filtro.trace("w", self.filtrar)

            self.codigo = ctk.StringVar()
            self.codigo.trace("w", self.controller.buscar_produto)
            self.nome = ctk.StringVar()
            self.preco_custo = ctk.StringVar()
            self.preco_custo.trace("w", self.atualizar_margem)
            self.preco_venda = ctk.StringVar()
            self.preco_venda.trace("w", self.atualizar_margem)
            self.quantidade = ctk.StringVar()

            self.margem = StringVar()
            self.tipo = StringVar()
            self.qtd_fardo = ctk.StringVar()
            self.referencia_codigo_fardo = ctk.StringVar()


            produto_tela = ctk.CTkFrame(self.frame_conteudo, fg_color="#1e1e1e")
            produto_tela.grid(row=0, column=0, sticky="nsew")
            produto_tela.rowconfigure((0,1,2), weight=1)
            produto_tela.columnconfigure(0, weight=1)

            header = ctk.CTkFrame(produto_tela, fg_color="#1e1e1e")
            header.grid(column=0, row=0, sticky="nsew")
            header.columnconfigure((0,1,2), weight=1)
            header.rowconfigure((0,1), weight=1)

            body = ctk.CTkFrame(produto_tela, fg_color="#1e1e1e")
            body.grid(column=0, row=1, sticky="nsew")
            body.columnconfigure((0,1), weight=1)

            entrys_frame = ctk.CTkFrame(body, fg_color="#1e1e1e")
            entrys_frame.grid(column=0, row=0, sticky="nsew")
            entrys_frame.columnconfigure((0,1,2), weight=1)
            entrys_frame.rowconfigure((0,1,3,4,5,6,7,8), weight=1)
            entrys_frame.rowconfigure(2, weight=0)

            margem_frame = ctk.CTkFrame(entrys_frame, fg_color="#1e1e1e")
            margem_frame.grid(row=5, column=2, sticky="nsew", padx=10)
            margem_frame.columnconfigure(0, weight=1)

            estoque = ctk.CTkFrame(body, fg_color="#1e1e1e")
            estoque.grid(column=1, row=0, sticky="nsew")
            estoque.columnconfigure(0, weight=1)
            estoque.rowconfigure((0,1,2), weight=1)


            botoes_frame = ctk.CTkFrame(produto_tela, fg_color="#1e1e1e")
            botoes_frame.grid(column=0, row=2, sticky="nsew")
            botoes_frame.columnconfigure((0,1,2,3,4), weight=1)
            botoes_frame.rowconfigure((0,1), weight=1)

            buttons = [("""Salvar""", "green", lambda: self.setar_status(resultado=self.controller.criar(), 
                                                                         label_status=self.label_status, 
                                                                         var_status=self.status_menu)),
                       ("Alterar código", "green", self.modal_codigo_novo),
                       ("Excluir produto", "red", self.modal_confirmar_exclusao),
                       ("Voltar", "red", self.voltar)]
            
            self.entrys = [("Código", self.codigo), ("Nome", self.nome), ("Tipo", self.tipo), ("Preço custo", self.preco_custo), ("Preço venda", self.preco_venda), ("Quantidade", self.quantidade), ("Qtd_fardo", self.referencia_codigo_fardo), ("Referencia_id_pai", self.qtd_fardo)]
            
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

            self.tabela = ttk.Treeview(
                estoque,
                columns=("codigo", "nome", "qtd"),
                show="headings"
            )

            self.tabela.heading("codigo", text="Código")
            self.tabela.heading("nome", text="Nome")
            self.tabela.heading("qtd", text="Qtd")

            self.tabela.column("codigo", width=100, anchor="center")
            self.tabela.column("nome", width=220, anchor="center")
            self.tabela.column("qtd", width=60, anchor="center")

            self.tabela.grid(row=0, column=0, sticky="nsew")

            scroll = ttk.Scrollbar(
                estoque,
                orient="vertical",
                command=self.tabela.yview
            )
            self.tabela.configure(yscrollcommand=scroll.set)

            scroll.grid(row=0, column=1, sticky="ns")
            estoque.rowconfigure(0, weight=1)
            estoque.columnconfigure(0, weight=1)

            #label filtro estoque
            ctk.CTkLabel(estoque, 
                        text="Digite o nome do produto", 
                        text_color="white",
                        font=("Arial", 30, "bold"),
                        fg_color="#1e1e1e",
                        anchor="center",
                        wraplength=320
                        ).grid(column=0, row=1, padx=20)
            
            #entry filtro estoque
            ctk.CTkEntry(estoque, 
                        textvariable=self.filtro, 
                        width=200,
                        height=50,
                        font=("Arial", 20, "bold")
                        ).grid(row=2, column=0, padx=20, sticky="n")
                

            #label principal
            ctk.CTkLabel(header, 
                      text="""Menu de cadastro de produtos""", 
                      text_color="white",
                      fg_color="#1e1e1e",
                      font=("arial", 32, "bold")
                      ).grid(column=1, row=0)
            
            #label status
            self.label_status = ctk.CTkLabel(header, 
                      textvariable=self.status_menu,
                      text_color="red",
                      fg_color="#1e1e1e",
                      font=("arial", 28, "bold")
                      )
            self.label_status.grid(column=1, row=1, sticky="s") 

            entry_codigo = ctk.CTkEntry(entrys_frame,
                        width=350,
                        height=50,
                        font=("arial", 26, "bold"),
                        textvariable=self.codigo)
            entry_codigo.grid(row=1, column=0, sticky="n", padx=20)
            
            label_codigo = ctk.CTkLabel(entrys_frame, 
                    text="Código",
                    text_color="white",
                    fg_color="#1e1e1e",
                    font=("arial", 32, "bold")
                    ).grid(row=0, column=0, sticky="s", padx=20)
            
            entry_nome = ctk.CTkEntry(entrys_frame,
                        width=400,
                        height=50,
                        font=("arial", 26, "bold"),
                        textvariable=self.nome)
            entry_nome.grid(row=1, column=1, sticky="n", padx=20)
            
            label_nome = ctk.CTkLabel(entrys_frame, 
                    text="Nome",
                    text_color="white",
                    fg_color="#1e1e1e",
                    font=("arial", 32, "bold")
                    ).grid(row=0, column=1, sticky="s", padx=20)
            
            #combobox tipo
            combobox_tipo = ctk.CTkComboBox(entrys_frame,
                                            values=["unidade", "fardo"],
                                            variable=self.tipo,
                                            state="readonly",
                                            width=310,
                                            height=50,
                                            font=("arial", 32, "bold"),
                                            command=self.controller.mudar_conteudo
                                            )
            combobox_tipo.grid(row=8, column=1)
            self.tipo.set("unidade")

            
            entry_preco_custo = ctk.CTkEntry(entrys_frame,
                        width=100,
                        height=50,
                        font=("arial", 26, "bold"),
                        textvariable=self.preco_custo)
            entry_preco_custo.grid(row=5, column=0, sticky="n", padx=20)
            
            label_preco_custo = ctk.CTkLabel(entrys_frame, 
                    text="Preço Custo",
                    text_color="white",
                    fg_color="#1e1e1e",
                    font=("arial", 32, "bold")
                    ).grid(row=4, column=0, sticky="s", padx=20)
            
            entry_preco_venda = ctk.CTkEntry(entrys_frame,
                        width=100,
                        height=50,
                        font=("arial", 26, "bold"),
                        textvariable=self.preco_venda)
            entry_preco_venda.grid(row=5, column=1, sticky="n", padx=20)
            
            label_preco_venda = ctk.CTkLabel(entrys_frame, 
                    text="Preço venda",
                    text_color="white",
                    fg_color="#1e1e1e",
                    font=("arial", 32, "bold")
                    ).grid(row=4, column=1, sticky="s", padx=20)
            
            #margem
            label_margem = ctk.CTkLabel(margem_frame, 
                    textvariable=self.margem,
                    text_color="white",
                    fg_color="#1e1e1e",
                    font=("arial", 26, "bold"),
                    anchor="center",
                    wraplength=220
                    ).grid(sticky="nsew")

            self.margem.set("Margem de lucro: 0%")
            
            entry_quantidade = ctk.CTkEntry(entrys_frame,
                        width=120,
                        height=50,
                        font=("arial", 26, "bold"),
                        textvariable=self.quantidade)
            entry_quantidade.grid(row=1, column=2, sticky="n", padx=20)
            
            label_quantidade = ctk.CTkLabel(entrys_frame, 
                    text="Quantidade",
                    text_color="white",
                    fg_color="#1e1e1e",
                    font=("arial", 32, "bold")
                    ).grid(row=0, column=2, sticky="s", padx=20)
            
            #label dependendo do tipo
            self.label_tipo = ctk.CTkLabel(entrys_frame, 
                            text="Referencia produto", 
                            text_color="white",
                            fg_color="#1e1e1e",
                            font=("arial", 32, "bold")
                          )
            self.label_tipo.grid(row=7, column=0, padx=20, sticky="s")

            #entrada dependendo do tipo
            self.entry_tipo = ctk.CTkEntry(entrys_frame, 
                                  textvariable=self.referencia_codigo_fardo, 
                                  width=300,
                                  height=50,
                                  font=("Arial", 20, "bold"))
            self.entry_tipo.grid(row=8, column=0, padx=20, sticky="n")

            #na ordem que ta na tela
            self.entries.append(entry_codigo)
            self.entries.append(entry_nome)
            self.entries.append(entry_quantidade)
            self.entries.append(entry_preco_custo)
            self.entries.append(entry_preco_venda)
            self.entries.append(self.entry_tipo)

            #teclas para mudar campo
            for i, entry in enumerate(self.entries):
                entry.bind("<Return>", lambda e, idx=i: self.proximo_campo(idx)) #enter
                entry.bind("<Down>", lambda e, idx=i: self.proximo_campo(idx)) #seta pra baixo
                entry.bind("<Up>", lambda e, idx=i: self.campo_anterior(idx)) #seta pra cima
                entry.bind("<Escape>", lambda e: self.voltar())
        
            #botoes de escolha
            for i, (texto, cor, comando) in enumerate(buttons, start=1):
                ctk.CTkButton(botoes_frame, 
                        text=texto, 
                        text_color="black", 
                        corner_radius=40,
                        border_color="black",
                        hover_color=cor,
                        border_width=5,
                        width=200,  
                        height=100,
                        font=("Arial", 30, "bold"),
                        fg_color="orange",
                        command=comando
                        ).grid(column=i, row=0, padx=20)
                
            #frame atalhos
            frame_atalho = ctk.CTkFrame(botoes_frame, fg_color="#e7dddd", corner_radius=12)
            frame_atalho.grid(row=0, column=5, sticky="new")

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
F1 - Salvar
F2 - Alterar código
F3 - Excluir
Esc - Voltar""",
                    text_color="black",
                    font=("Consolas", 15),
                    anchor="w")
            label_atalhos.grid(row=1, column=0, sticky="nw", padx=10, pady=(0,12))
            
            
            self.master.bind("<F1>", lambda e: self.setar_status(resultado=self.controller.criar(), 
                                                                 label_status=self.label_status, 
                                                                 var_status=self.status_menu))
            self.master.bind("<F2>", lambda e: self.modal_codigo_novo())
            self.master.bind("<F3>", lambda e: self.modal_confirmar_exclusao())
            self.master.bind("<Escape>", lambda e: self.voltar())
            self.master.bind("<Return>", lambda e: self.controller.produto_selecionado())
            self.entries[0].focus_set()

            self.carregar_estoque()

        def modal_confirmar_exclusao(self):
            codigo = self.referencia_main.estoque.conferir_se_existe_no_estoque(self.codigo.get())

            if codigo:
                modal = ctk.CTkToplevel(self.frame_conteudo, fg_color="#1e1e1e")

                modal.title("Excluir")
                modal.geometry("400x300")
                modal.transient(self.frame_conteudo)
                modal.update_idletasks()
                modal.grab_set()

                label = ctk.CTkLabel(modal, text="Deseja realmente excluir?", font=("Arial", 20, "bold"))
                label.pack(padx=20, pady=20)

                botao_sim = ctk.CTkButton(modal,
                            text="Sim", 
                            text_color="black", 
                            corner_radius=40,
                            border_color="black",
                            hover_color="green",
                            border_width=5,
                            width=150,  
                            height=100,
                            font=("Arial", 30, "bold"),
                            fg_color="orange",
                            command=lambda: self.setar_status(resultado=self.controller.deletar(self.codigo.get(), modal), 
                                                            label_status=self.label_status,
                                                            var_status=self.status_menu))
                botao_sim.pack(side="left", padx=28)

                botao_nao = ctk.CTkButton(modal,
                            text="Não", 
                            text_color="black", 
                            corner_radius=40,
                            border_color="black",
                            hover_color="red",
                            border_width=5,
                            width=150,  
                            height=100,
                            font=("Arial", 30, "bold"),
                            fg_color="orange",
                            command=lambda: modal.destroy()
                            )
                botao_nao.pack(side="left", padx=28)

                modal.bind("<Return>", lambda e: self.setar_status(resultado=self.controller.deletar(self.codigo.get(), modal), 
                                                                   label_status=self.label_status,
                                                                   var_status=self.status_menu))
                modal.bind("<Escape>", lambda e: modal.destroy())


        def modal_codigo_novo(self):
            codigo_atual = self.codigo.get()

            produto = self.referencia_main.estoque.get_produto(codigo_atual)

            if produto:
                codigo_novo = ctk.StringVar()
                modal = ctk.CTkToplevel(self.frame_conteudo, fg_color="#1e1e1e")
                modal_status = StringVar()

                label_modal_status = ctk.CTkLabel(modal, 
                      textvariable=modal_status,
                      fg_color="#1e1e1e",
                      font=("arial", 18, "bold"))
                label_modal_status.pack(padx=20, pady=20)

                modal.title("Alterar código")
                modal.geometry("400x400")
                modal.transient(self.frame_conteudo)
                modal.update_idletasks()
                modal.grab_set()

                label = ctk.CTkLabel(modal, text="Digite o novo código", font=("Arial", 20, "bold"))
                label.pack(padx=20, pady=20)

                entry = ctk.CTkEntry(modal, textvariable=codigo_novo, width=200, height=50, font=("Arial", 20, "bold"))
                entry.pack(padx=20, pady=20)

                entry.bind("<Return>", lambda e: self.setar_status(resultado=self.controller.alterar_codigo(codigo_atual, codigo_novo.get(), modal), label_status=label_modal_status, var_status=modal_status))
                entry.bind("<Escape>", lambda e: modal.destroy())
                entry.focus_set()


        def carregar_estoque(self, estoque=None):
            for item in self.tabela.get_children():
                self.tabela.delete(item)

            if not estoque:
                estoque = self.referencia_main.estoque.get_banco()

            for produto in estoque:
                _, codigo, nome, tipo, preco_custo, preco_venda, quantidade, _, _ = produto

                self.tabela.insert(
                    "",
                    "end",
                    values=(
                        codigo,
                        nome,
                        quantidade
                    )
                )
        
        def filtrar(self, *args):
            digitado = self.filtro.get()
            filtro = self.referencia_main.estoque.filtrar_produto(self.coluna_filtro, digitado)
            self.carregar_estoque(filtro)

        def atualizar_margem(self, *args):
            try:
                preco_custo = self.preco_custo.get().replace(",", ".")
                preco_custo = float(preco_custo)
                preco_venda = self.preco_venda.get().replace(",", ".")
                preco_venda = float(preco_venda)
            
            except:
                return #tirei o raise porque ficava aparecendo erro toda hora
                raise ValueError
            
            try:
                margem = (preco_venda - preco_custo) / preco_venda * 100
            except:
                raise ZeroDivisionError

            if margem < 0:
                self.margem.set("")
                return

            self.margem.set(f"Margem de lucro: {margem:.2f}%")

        def setar_status(self, resultado, label_status=None, var_status=None):
            if resultado is None:
                return
            
            if label_status:
                label_status.configure(text_color=resultado.cor)
        
            if var_status:
                var_status.set(resultado.mensagem)
                self.after(resultado.tempo, lambda: var_status.set(""))
            
        def voltar(self):
            self.referencia_main.voltar_menu_principal()

        def limpar_tela(self):
            for widget in self.frame_conteudo.winfo_children():
                widget.destroy()

        def proximo_campo(self, indice):
                """Muda o foco do entry pro proximo"""
                if indice + 1 < len(self.entries):
                    self.entries[indice + 1].focus_set()
                else:
                    self.setar_status(resultado=self.controller.criar(), 
                                      label_status=self.label_status, 
                                      var_status=self.status_menu)
                    self.entries[0].focus_set()

        def campo_anterior(self, indice):
            "Muda o foco do entry pro anterior"
            if indice - 1 >= 0:
                self.entries[indice - 1].focus_set()

class ProdutoController:
    def __init__(self, tela, ref_estoque):
        self.tela = tela
        self.ref_estoque = ref_estoque

    
    def criar(self):
        """Recebe as entradas e envia para a classe estoque criar e salvar o produto"""
        dados = self.coletar_dados_produto()
        if not dados:
            return
        
        resultado = self.ref_estoque.criar_produto(**dados)

        if resultado == True:
            self.tela.setar_status(resultado=self.editar(dados), 
                                   label_status=self.tela.label_status, 
                                   var_status=self.tela.status_menu)
            return
        
        self.limpar_variaveis()
        self.tela.carregar_estoque()
        return resultado

    def alterar_codigo(self, codigo_atual, codigo_novo, modal):
        produto = self.ref_estoque.conferir_se_existe_no_estoque(codigo_novo)
        if produto:
            from Utils.Resultado import Resultado
            return Resultado(False, "Já existe um produto com esse código", "erro")
        dados = self.coletar_dados_produto()
        resultado = self.ref_estoque.alterar_codigo(codigo_atual, codigo_novo, dados)
        self.limpar_variaveis()
        self.tela.carregar_estoque()
        modal.destroy()

    def editar(self, dados):
        if dados:
            resultado = self.ref_estoque.atualizar_produto(dados)
            self.tela.carregar_estoque()
            return resultado

    def deletar(self, codigo, modal):
        dados = self.coletar_dados_produto()
        resultado = self.ref_estoque.remover_produto(**dados)
        self.limpar_variaveis()
        self.tela.carregar_estoque()
        modal.destroy()
        return resultado
        
    def mudar_conteudo(self, valor):
        self.tela.tipo.set(valor)
        if self.tela.tipo.get() == "fardo":
            self.tela.label_tipo.configure(text="Quantidade no fardo")
            self.tela.entry_tipo.configure(textvariable=self.tela.qtd_fardo)
            self.tela.referencia_codigo_fardo.set("")
            
        else:
            self.tela.label_tipo.configure(text="Referencia produto")
            self.tela.entry_tipo.configure(textvariable=self.tela.referencia_codigo_fardo)
            self.tela.qtd_fardo.set("")
    
    def produto_selecionado(self):
        selecionado = self.tela.tabela.selection()
        
        if not selecionado:
            return

        item_id = selecionado[0] #id do item
        valores = self.tela.tabela.item(item_id, "values")

        produto = self.ref_estoque.get_produto(valores[0])

        if produto:
            for i, (texto, var) in enumerate(self.tela.entrys):
                if produto[i+1] == None:
                    var.set("")
                    continue
                var.set(produto[i+1])
            self.mudar_conteudo(produto[3])

        else:
            self.limpar_variaveis()
    
    def buscar_produto(self, *args):
        codigo = self.tela.codigo.get()
        produto = self.ref_estoque.get_produto(codigo)

        if not produto:
            self.limpar_variaveis()
            return


        codigo_produto_pai = None
        if produto[7]:
            codigo_produto_pai = self.ref_estoque.codigo_produto_pai(produto[7])

        if produto:
            for i, (texto, var) in enumerate(self.tela.entrys):
                if produto[i+1] == None:
                    var.set("")
                    continue
                if i+1 == 7:
                    var.set(codigo_produto_pai if codigo_produto_pai else "")
                    continue
                var.set(produto[i+1])
            self.mudar_conteudo(produto[3])

        else:
            self.limpar_variaveis()
    
    def limpar_variaveis(self):
        for i, tupla in enumerate(self.tela.entrys):
                if i == 0 or i == 2:
                    continue
                tupla[1].set("")
        self.tela.entries[0].focus_set()

    def coletar_dados_produto(self):
        try:
            codigo = self.tela.codigo.get()
            produto_pai = self.tela.referencia_codigo_fardo.get()
            if produto_pai == codigo:
                self.tela.status_menu.set("Código do produto de referencia nao pode ser o mesmo do produto atual")
                return None
            preco_custo = self.tela.preco_custo.get().replace(",", ".")
            preco_venda = self.tela.preco_venda.get().replace(",", ".")
            nome = self.tela.nome.get()
            quantidade = self.tela.quantidade.get()
            if nome == "":
                self.tela.status_menu.set("Produto precisa de um nome")
                return None
            if quantidade == "":
                self.tela.status_menu.set("Produto precisa de quantidade")
                return None
            dados = {
                "codigo": self.tela.codigo.get(),
                "nome": nome,
                "preco_custo": float(preco_custo),
                "preco_venda": float(preco_venda),
                "quantidade": int(quantidade),
                "tipo": self.tela.tipo.get(),
                "id_produto_pai": self.tela.referencia_codigo_fardo.get()
                    if self.tela.referencia_codigo_fardo.get().strip() else None,
                "quantidade_fardo": int(self.tela.qtd_fardo.get())
                    if self.tela.qtd_fardo.get().strip() else None,
                "funcionario": self.tela.usuario
            }
            return dados
        except ValueError:
            self.tela.status_menu.set("Digite apenas números")
            return None
