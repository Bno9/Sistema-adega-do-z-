import customtkinter as ctk
from tkinter import ttk

class DespesasMenu(ctk.CTkFrame):
    
    def __init__(self, root, referencia_main) :   
        super().__init__(master=root, fg_color="#1e1e1e")

        self.referencia_main = referencia_main

        self.controller = DespesaController(self, self.referencia_main.despesa)

        self.pode_usar_atalho = True
        self.entries = []

        #texto
        self.status = ctk.StringVar()
        self.total = ctk.StringVar()

        #atributos
        self.despesa_selecionada = ctk.IntVar() #id da despesa
        self.nome = ctk.StringVar()
        self.valor = ctk.StringVar()
        self.data = ctk.StringVar()
        self.observacao = ctk.StringVar()

        self.campos = [("Nome", self.nome),
                       ("Valor", self.valor),
                       ("Data", self.data),
                       ("Observação", self.observacao)]
        
        self.values = ["Tudo"]

        #frame

        #botao combobox
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.frame_conteudo = ctk.CTkFrame(self, fg_color="#1e1e1e")
        self.frame_conteudo.grid(row=0, column=0, sticky="nsew")
        self.frame_conteudo.columnconfigure(0, weight=1) #uma unica coluna que ocupa a tela toda
        self.frame_conteudo.rowconfigure(1, weight=1)
        self.frame_conteudo.rowconfigure((0,2), weight=0) #divide a tela em 3 partes, com a linha do meio tendo uma proporção maior

        self.master.bind("<Escape>", lambda e: self.referencia_main.voltar_menu_principal())

        #combobox
        self.combobox = ctk.CTkComboBox(self.frame_conteudo,
                      values=["Selecione um filtro"],
                      command=self.controller.get_escolha,
                      width=200,
                      height=50
                      )

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

        #scroll
        self.scroll = ttk.Scrollbar(self.frame_conteudo)
        self.scroll.grid(row=1, column=1, sticky="ns")

        #tabela
        self.tabela = ttk.Treeview(
            self.frame_conteudo,
            columns=("nome", "valor", "data", "observacao"),
            show="headings",
            style="Custom.Treeview",
            yscrollcommand=self.scroll.set
        )

        #inserção da tabela
        self.tabela.grid(row=1, column=0, sticky="nsew") #tabela inserida na linha do meio, pois ela ocupa mais espaço que as outras linhas

        #inserção do scroll
        self.scroll.config(command=self.tabela.yview)

        #Cabeçalhos da tabela
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("valor", text="Valor")
        self.tabela.heading("data", text="Data")
        self.tabela.heading("observacao", text="Observação")

        #Coluna da tabela
        self.tabela.column("nome", width=150)
        self.tabela.column("valor", width=80)
        self.tabela.column("data", width=80)
        self.tabela.column("observacao", width=200)

        self.master.bind("<Delete>", lambda e: self.tela_deletar())

        self.carregar_tabela()

        self.widgets()

    def widgets(self):
        
        self.combobox.grid(row=0, column=0, sticky="w")

        self.controller.atualizar_combobox(self.combobox)
        self.controller.atualizar_total("Tudo")

        frame_botoes = ctk.CTkFrame(self.frame_conteudo, fg_color="#1e1e1e")
        frame_botoes.grid(row=2, column=0, sticky="ew", pady=20) #cria o frame na terceira linha do frame_conteudo (linha 2 é a tabela e linha 1 a combobox. a coluna 0 com peso 1 ocupa todo espaço da tela, entao precisa desse fram pra separar o rodapé em 3 colunas porque se separar no frame conteudo vai quebrar a tabela)

        frame_botoes.columnconfigure((0,1,2,3), weight=1) #divide em 3 colunas iguais

        #Label total
        ctk.CTkLabel(self.frame_conteudo,
                     textvariable=self.total,
                    font=("Arial", 44, "bold"),
                    text_color="white"
                     ).grid(row=0, column=0, sticky="e")
        
        #botao adicionar
        ctk.CTkButton(frame_botoes, 
                    text="Adicionar despesa", 
                    text_color="black", 
                    corner_radius=20,
                    border_color="black",
                    hover_color="white",
                    width=300,  
                    height=100,
                    font=("Arial", 16, "bold"),
                    fg_color="orange",
                   command=lambda: self.escolha_tela(1)
                   ).grid(column=0, row=0)
        
        #botao editar
        ctk.CTkButton(frame_botoes, 
                    text="Editar despesa", 
                    text_color="black", 
                    corner_radius=20,
                    border_color="black",
                    hover_color="white",
                    width=300,  
                    height=100,
                    font=("Arial", 16, "bold"),
                    fg_color="orange",
                   command=lambda: self.escolha_tela(2)
                   ).grid(column=1, row=0)
        
        #botao excluir
        ctk.CTkButton(frame_botoes, 
                    text="Excluir despesa", 
                    text_color="black", 
                    corner_radius=20,
                    border_color="black",
                    hover_color="white",
                    width=300,  
                    height=100,
                    font=("Arial", 16, "bold"),
                    fg_color="orange",
                   command=lambda: self.escolha_tela(3)
                   ).grid(column=2, row=0)

        #botao voltar
        ctk.CTkButton(frame_botoes, 
                    text="Voltar", 
                    text_color="black", 
                    corner_radius=20,
                    border_color="black",
                    hover_color="white",
                    width=300,  
                    height=100,
                    font=("Arial", 16, "bold"),
                    fg_color="orange",
                   command=self.referencia_main.voltar_menu_principal
                   ).grid(row=0, column=3)
        

    def escolha_tela(self, escolha):
        mapa = {1: self.tela_cadastrar,
                2: self.tela_editar,
                3: self.tela_deletar,
                4: self.referencia_main.voltar_menu_principal}
        
        try:
            escolha = int(escolha)
        except ValueError:
            raise ValueError("Valor recebido inválido")
        
       
        escolhido = mapa[escolha]
        self.pode_usar_atalho = False

        escolhido()
        
    def tela_cadastrar(self):
        modal_cadastrar = ctk.CTkToplevel(self.frame_conteudo, fg_color="#1e1e1e")

        modal_cadastrar.title("Cadastro")
        modal_cadastrar.geometry("1000x800")

        modal_cadastrar.transient(self.frame_conteudo)   #fica sobre a janela principal
        modal_cadastrar.update_idletasks()
        modal_cadastrar.grab_set()        #trava interação com a janela principal

        modal_cadastrar.bind("<Escape>", lambda e: self.fechar_modal(modal_cadastrar))

        modal_cadastrar.columnconfigure(0, weight=1)
        modal_cadastrar.rowconfigure((0,2), weight=1)
        modal_cadastrar.rowconfigure(1, weight=2)
        header =  ctk.CTkFrame(modal_cadastrar, fg_color="#1e1e1e")
        entrys =  ctk.CTkFrame(modal_cadastrar)
        botoes = ctk.CTkFrame(modal_cadastrar, fg_color="#1e1e1e")

        header.grid(row=0, column=0)

        entrys.rowconfigure(0, weight=1)
        entrys.columnconfigure((0,1), weight=1)
        entrys.grid(row=1, column=0)

        botoes.rowconfigure(0, weight=1)
        botoes.columnconfigure((0,1), weight=1)
        botoes.grid(row=2, column=0)

        #label confirmação
        ctk.CTkLabel(header, 
                     text="Digite as informações",
                     font=("arial", 36, "bold")
                     ).grid(column=0, row=0)
        
        for i, (texto, variavel) in enumerate(self.campos):
            ctk.CTkLabel(entrys,
                         text=texto,
                         font=("arial", 32, "bold")
                        ).grid(column=1, row=i, sticky="w", padx=10, pady=20)
            
            entry = ctk.CTkEntry(entrys,
                         textvariable=variavel,
                         font=("Arial", 20, "bold"),
                         width=200)
            entry.grid(column=0, row=i, padx=10, pady=20)
            self.entries.append(entry)
        

        self.entries[0].focus_set()
        
        #botao cancelar
        ctk.CTkButton(botoes, 
                      text="Cancelar", 
                      width=300,
                      height=150,
                      text_color="black",
                      fg_color="red",
                      font=("arial", 30, "bold"),
                      command=lambda: self.fechar_modal(modal_cadastrar)
                      ).grid(row=0, column=1, padx=70)
        
        #botao cadastrar
        botao_cadastro = ctk.CTkButton(botoes, 
                      text="Cadastrar",
                      width=300,
                      height=150, 
                      text_color="black",
                      fg_color="green",
                      font=("arial", 30, "bold"),
                      command=lambda: self.controller.adicionar(modal_cadastrar, self.nome.get(), self.valor.get(), self.data.get(), self.observacao.get())
                      )
        botao_cadastro.grid(row=0, column=0, padx=70)
        

        for i, entry in enumerate(self.entries):
                entry.bind("<Return>", lambda e, idx=i: self.proximo_campo(idx, botao_cadastro)) #enter
                entry.bind("<Down>", lambda e, idx=i: self.proximo_campo(idx, botao_cadastro)) #seta pra baixo
                entry.bind("<Up>", lambda e, idx=i: self.campo_anterior(idx)) #seta pra cima
        
    def tela_editar(self):
        try:
            id_despesa = self.pegar_id_selecionado()
        except ValueError as e:
            print(e)
            return
        
        modal_editar = ctk.CTkToplevel(self.frame_conteudo, fg_color="#1e1e1e")

        modal_editar.title("Edição")
        modal_editar.geometry("1000x800")

        modal_editar.transient(self.frame_conteudo)   #fica sobre a janela principal
        modal_editar.update_idletasks()
        modal_editar.grab_set()        #trava interação com a janela principal

        modal_editar.bind("<Escape>", lambda e: self.fechar_modal(modal_editar))

        modal_editar.columnconfigure(0, weight=1)
        modal_editar.rowconfigure((0,2), weight=1)
        modal_editar.rowconfigure(1, weight=2)
        header =  ctk.CTkFrame(modal_editar, fg_color="#1e1e1e")
        entrys =  ctk.CTkFrame(modal_editar)
        botoes = ctk.CTkFrame(modal_editar, fg_color="#1e1e1e")

        header.grid(row=0, column=0)

        entrys.rowconfigure(0, weight=1)
        entrys.columnconfigure((0,1), weight=1)
        entrys.grid(row=1, column=0)

        botoes.rowconfigure(0, weight=1)
        botoes.columnconfigure((0,1), weight=1)
        botoes.grid(row=2, column=0)

        #label confirmação
        ctk.CTkLabel(header, 
                     text="Digite as novas informações",
                     font=("arial", 32, "bold")
                     ).grid(row=0, column=0)
        
        for i, (texto, variavel) in enumerate(self.campos):
            ctk.CTkLabel(entrys,
                         text=texto,
                         font=("arial", 32, "bold")
                        ).grid(row=i, column=1,  padx=10, pady=20)
            
            entry = ctk.CTkEntry(entrys,
                         textvariable=variavel,
                         font=("Arial", 20, "bold"),
                         width=200)
            entry.grid(row=i, column=0, padx=10, pady=20)
            self.entries.append(entry)

        
        self.entries[0].focus_set()

        #botao editar
        botao_editar = ctk.CTkButton(botoes, 
                      text="Editar",
                      width=300,
                      height=150, 
                      text_color="black",
                      fg_color="green",
                      font=("arial", 30, "bold"),
                      command=lambda: self.controller.editar(modal_editar, id_despesa, self.nome.get(), self.valor.get(), self.data.get(), self.observacao.get())
                      )
        botao_editar.grid(row=0, column=1, padx=70)
        
        #botao cancelar
        ctk.CTkButton(botoes, 
                      text="Cancelar", 
                      width=300,
                      height=150,
                      text_color="black",
                      fg_color="red",
                      font=("arial", 30, "bold"),
                      command=lambda: self.fechar_modal(modal_editar)
                      ).grid(row=0, column=2, padx=70)
        

        for i, entry in enumerate(self.entries):
                entry.bind("<Return>", lambda e, idx=i: self.proximo_campo(idx, botao_editar)) #enter
                entry.bind("<Down>", lambda e, idx=i: self.proximo_campo(idx, botao_editar)) #seta pra baixo
                entry.bind("<Up>", lambda e, idx=i: self.campo_anterior(idx)) #seta pra cima

        
       
    def tela_deletar(self):
        try:
            id_despesa = self.pegar_id_selecionado()
        except ValueError as e:
            print(e)
            return
        
        modal_deletar = ctk.CTkToplevel(self.frame_conteudo, fg_color="#1e1e1e")

        modal_deletar.title("Confirmação")
        modal_deletar.geometry("500x300")

        modal_deletar.transient(self.frame_conteudo)   #fica sobre a janela principal
        modal_deletar.update_idletasks()
        modal_deletar.grab_set()        #trava interação com a janela principal

        modal_deletar.bind("<Escape>", lambda e: self.fechar_modal(modal_deletar))
        modal_deletar.bind("<Return>", lambda e: self.controller.deletar(modal_deletar, id_despesa))
        
        modal_deletar.rowconfigure((0,1), weight=1)
        modal_deletar.columnconfigure(0, weight=1)

        header = ctk.CTkFrame(modal_deletar, fg_color="#1e1e1e")
        botoes = ctk.CTkFrame(modal_deletar, fg_color="#1e1e1e")
        botoes.columnconfigure((0,1,2), weight=1)

        header.grid(column=0, row=0)
        botoes.grid(column=0, row=1)

        #label confirmação
        ctk.CTkLabel(header, 
                     text="Deseja realmente excluir?",
                     font=("arial", 32, "bold")
                     ).grid(row=0, column=0)
        
        #botao nao
        ctk.CTkButton(botoes, 
                      text="Não", 
                      width=100,
                      height=80,
                      text_color="black",
                      fg_color="red",
                      font=("arial", 30, "bold"),
                      command=lambda e: self.fechar_modal(modal_deletar)
                      ).grid(row=0, column=2, padx=30)
        
        #botao sim
        ctk.CTkButton(botoes, 
                      text="Sim",
                      width=100,
                      height=80, 
                      text_color="black",
                      fg_color="green",
                      font=("arial", 30, "bold"),
                      command=lambda e: self.controller.deletar(modal_deletar, id_despesa)
                      ).grid(row=0, column=0, padx=30)

    def carregar_tabela(self, despesas=None):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        if not despesas:
            despesas = self.referencia_main.despesa.listar_despesas()

        for desp in despesas: #pega o objeto no banco de dados e insere na tabela
            id_despesa, nome, valor, data, observacao = desp
            #primeiro valor é o id

            self.tabela.insert(
                "",
                "end",
                iid=id_despesa,
                values=(
                    nome,
                    f"R$: {valor:.2f}",
                    data,
                    observacao
               )
            )

    def pegar_id_selecionado(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            self.pode_usar_atalho = True
            raise ValueError("Nenhuma despesa selecionada")
        return int(selecionado[0])
    
    def confirmar_exclusao(self):
        try:
            id_despesa = self.pegar_id_selecionado()
            self.controller.deletar(id_despesa)
            self.carregar_tabela()

        except ValueError as e:
            print(e)

    def fechar_modal(self, modal):
        modal.grab_release()
        modal.destroy()
        self.pode_usar_atalho = True
        self.entries.clear()

    def teclas_menu(self, tecla):
        if tecla.char in ["1", "2", "3", "4"] and self.pode_usar_atalho:
            self.escolha_tela(int(tecla.char))

    def proximo_campo(self, indice, botao):
            """Muda o foco do entry pro proximo"""
            if indice + 1 < len(self.entries):
                self.entries[indice + 1].focus_set()
            else:
                botao.invoke()

    def campo_anterior(self, indice):
        "Muda o foco do entry pro anterior"
        if indice - 1 >= 0:
            self.entries[indice - 1].focus_set()

class DespesaController:
    from Utils.Despesa import Despesas
    def __init__(self, tela, despesa_ref: Despesas): #acredito que assim nao vai dar certo porque eu ja tenho a despesa criada na main e conectada no banco de dados
        #até funcionaria porque nao vai dar erro acredito eu, mas ou eu vou ter que excluir ela da main e criar apenas aqui, ou excluir daqui e referenciar a main aqui
        self.tela = tela
        self.despesa = despesa_ref

    def adicionar(self, modal_cadastrar, nome, valor, data=None, observacao=None):
        if not nome.strip():
            raise ValueError("Nome da despesa é obrigatório")
        
        try:
            valor = float(valor)

        except ValueError:
            raise ValueError("Valor inválido")

        if valor <= 0:
            raise ValueError("Valor deve ser maior que zero")
        
        try:
            self.despesa.adicionar_despesa(
            nome=nome.strip(),
            valor=valor,
            data=data,
            observacao=observacao
        )
            self.tela.carregar_tabela()
        except ValueError as e:
            print(e)
        finally:
            self.atualizar_combobox(self.tela.combobox)
            self.tela.entries.clear()
            self.tela.fechar_modal(modal_cadastrar)

        

    def editar(self, modal_editar, id_despesa, nome, valor, data="", observacao=""):
        if not nome.strip():
            raise ValueError("Nome da despesa é obrigatório")
        
        try:
            valor = float(valor)

        except ValueError:
            raise ValueError("Valor inválido")

        if valor <= 0:
            raise ValueError("Valor deve ser maior que zero")

        try:
            self.despesa.editar_despesa(id_despesa,
            nome=nome.strip(),
            valor=valor,
            data=data,
            observacao=observacao)

            self.tela.carregar_tabela()
        except ValueError as e:
            print(e)
        finally:
            self.atualizar_combobox(self.tela.combobox) 
            self.tela.entries.clear()
            self.tela.fechar_modal(modal_editar)


    def deletar(self, modal_deletar, id):
        try:
            self.despesa.excluir_despesa(id)
            self.tela.carregar_tabela()
        except ValueError as e:
            print(e)
        finally:
            self.atualizar_combobox(self.tela.combobox)
            self.tela.entries.clear()
            self.tela.fechar_modal(modal_deletar)

    def listar(self):
        return self.despesa.listar_despesas()

    def total(self):
        return self.despesa.total_despesas()
    
    def atualizar_combobox(self, combobox):
        nomes = self.despesa.nome_despesas()

        self.tela.values = ["Tudo"] + [nome[0] for nome in nomes] #o banco de dados ja ta filtrando nomes repetidos

        combobox.configure(values=self.tela.values)
        combobox.set("Tudo")
    
    def atualizar_total(self, nome_despesa):
        valor = self.despesa.total_filtrado(nome_despesa)

        if nome_despesa == "Tudo":
            valor = self.despesa.total_despesas()

        self.tela.total.set(f"Total: R$ {valor:.2f}")

    def get_escolha(self, escolha):
       self.atualizar_total(escolha)
       filtro = self.despesa.pesquisar_por_nome(escolha)

       if escolha == "Tudo":
           filtro = None

        
       print(filtro)
       self.tela.carregar_tabela(filtro)