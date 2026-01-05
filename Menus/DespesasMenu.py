import customtkinter as ctk
from tkinter import ttk

class DespesasMenu(ctk.CTkFrame):
    
    def __init__(self, root, referencia_main) :   
        super().__init__(master=root, fg_color="#1e1e1e")

        self.referencia_main = referencia_main

        self.controller = DespesaController(self, self.referencia_main.despesa)

        #texto
        self.status = ctk.StringVar()

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
        
        self.values = []

        #frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.frame_conteudo = ctk.CTkFrame(self, fg_color="#1e1e1e")
        self.frame_conteudo.grid(row=0, column=0, sticky="nsew")
        self.frame_conteudo.columnconfigure(0, weight=1)
        self.frame_conteudo.rowconfigure((0,1,2,3,4,5,6), weight=1)

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
        self.scroll.grid(row=0, column=1, sticky="ns")

        #tabela
        self.tabela = ttk.Treeview(
            self.frame_conteudo,
            columns=("nome", "valor", "data", "observacao"),
            show="headings",
            style="Custom.Treeview",
            yscrollcommand=self.scroll.set
        )

        #inserção da tabela
        self.tabela.grid(row=0, column=0, sticky="nsew")

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

        self.carregar_tabela()

        self.widgets()

    def widgets(self):
        #botao combobox
        combobox = ctk.CTkComboBox(self.frame_conteudo,
                      values=["Selecione um filtro"],
                      command=self.controller.get_escolha,
                      width=200,
                      height=50
                      )
        combobox.place(x=50, y=450)

        self.controller.atualizar_combobox(combobox)

        #botao voltar
        ctk.CTkButton(self, 
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
                   ).place(x=1600, y=450)
        
        #botao adicionar
        ctk.CTkButton(self, 
                    text="Adicionar despesa", 
                    text_color="black", 
                    corner_radius=20,
                    border_color="black",
                    hover_color="white",
                    width=300,  
                    height=100,
                    font=("Arial", 16, "bold"),
                    fg_color="orange",
                   command=self.tela_cadastrar
                   ).place(x=400, y=1000)
        
        #botao editar
        ctk.CTkButton(self, 
                    text="Editar despesa", 
                    text_color="black", 
                    corner_radius=20,
                    border_color="black",
                    hover_color="white",
                    width=300,  
                    height=100,
                    font=("Arial", 16, "bold"),
                    fg_color="orange",
                   command=self.tela_editar
                   ).place(x=800, y=1000)
        
        #botao excluir
        ctk.CTkButton(self, 
                    text="Excluir despesa", 
                    text_color="black", 
                    corner_radius=20,
                    border_color="black",
                    hover_color="white",
                    width=300,  
                    height=100,
                    font=("Arial", 16, "bold"),
                    fg_color="orange",
                   command=self.tela_deletar
                   ).place(x=1200, y=1000)
        
    def tela_deletar(self):
        try:
            id_despesa = self.pegar_id_selecionado()
        except ValueError as e:
            print(e)
            return
        
        modal_deletar = ctk.CTkToplevel(self.frame_conteudo)

        modal_deletar.title("Confirmação")
        modal_deletar.geometry("300x300")

        modal_deletar.transient(self.frame_conteudo)   #fica sobre a janela principal
        modal_deletar.update_idletasks()
        modal_deletar.grab_set()        #trava interação com a janela principal

        #label confirmação
        ctk.CTkLabel(modal_deletar, 
                     text="Deseja realmente excluir?",
                     font=("arial", 16, "bold")
                     ).place(x=55, y=20)
        
        #botao nao
        ctk.CTkButton(modal_deletar, 
                      text="Não", 
                      width=100,
                      height=80,
                      text_color="black",
                      fg_color="red",
                      font=("arial", 30, "bold"),
                      command=modal_deletar.destroy
                      ).place(x=160, y=150)
        
        #botao sim
        ctk.CTkButton(modal_deletar, 
                      text="Sim",
                      width=100,
                      height=80, 
                      text_color="black",
                      fg_color="green",
                      font=("arial", 30, "bold"),
                      command=lambda: self.controller.deletar(modal_deletar, id_despesa)
                      ).place(x=40, y=150)
        
    def tela_cadastrar(self):
        modal_cadastrar = ctk.CTkToplevel(self.frame_conteudo)

        modal_cadastrar.title("Cadastro")
        modal_cadastrar.geometry("1000x800")

        modal_cadastrar.transient(self.frame_conteudo)   #fica sobre a janela principal
        modal_cadastrar.update_idletasks()
        modal_cadastrar.grab_set()        #trava interação com a janela principal

        #label confirmação
        ctk.CTkLabel(modal_cadastrar, 
                     text="Digite as informações",
                     font=("arial", 32, "bold")
                     ).place(x=300, y=20)
        
        for i, (texto, variavel) in enumerate(self.campos):
            ctk.CTkLabel(modal_cadastrar,
                         text=texto,
                         font=("arial", 32, "bold")
                        ).place(x=600,y=200 + (100*i))
            
            ctk.CTkEntry(modal_cadastrar,
                         textvariable=variavel,
                         font=("Arial", 20, "bold"),
                         width=300).place(x=300,y=200 + (100*i))
        
        #botao cancelar
        ctk.CTkButton(modal_cadastrar, 
                      text="Cancelar", 
                      width=300,
                      height=150,
                      text_color="black",
                      fg_color="red",
                      font=("arial", 30, "bold"),
                      command=modal_cadastrar.destroy
                      ).place(x=600, y=600)
        
        #botao cadastrar
        ctk.CTkButton(modal_cadastrar, 
                      text="Cadastrar",
                      width=300,
                      height=150, 
                      text_color="black",
                      fg_color="green",
                      font=("arial", 30, "bold"),
                      command=lambda: self.controller.adicionar(modal_cadastrar, self.nome.get(), self.valor.get(), self.data.get(), self.observacao.get())
                      ).place(x=150, y=600)
        
    def tela_editar(self):
        try:
            id_despesa = self.pegar_id_selecionado()
        except ValueError as e:
            print(e)
            return
        
        modal_editar = ctk.CTkToplevel(self.frame_conteudo)

        modal_editar.title("Edição")
        modal_editar.geometry("1000x800")

        modal_editar.transient(self.frame_conteudo)   #fica sobre a janela principal
        modal_editar.update_idletasks()
        modal_editar.grab_set()        #trava interação com a janela principal

        #label confirmação
        ctk.CTkLabel(modal_editar, 
                     text="Digite as novas informações",
                     font=("arial", 32, "bold")
                     ).place(x=300, y=20)
        
        for i, (texto, variavel) in enumerate(self.campos):
            ctk.CTkLabel(modal_editar,
                         text=texto,
                         font=("arial", 32, "bold")
                        ).place(x=600,y=200 + (100*i))
            
            ctk.CTkEntry(modal_editar,
                         textvariable=variavel,
                         font=("Arial", 20, "bold"),
                         width=300).place(x=300,y=200 + (100*i))
        
        #botao cancelar
        ctk.CTkButton(modal_editar, 
                      text="Cancelar", 
                      width=300,
                      height=150,
                      text_color="black",
                      fg_color="red",
                      font=("arial", 30, "bold"),
                      command=modal_editar.destroy
                      ).place(x=600, y=600)
        
        #botao editar
        ctk.CTkButton(modal_editar, 
                      text="Editar",
                      width=300,
                      height=150, 
                      text_color="black",
                      fg_color="green",
                      font=("arial", 30, "bold"),
                      command=lambda: self.controller.editar(modal_editar, id_despesa, self.nome.get(), self.valor.get(), self.data.get(), self.observacao.get())
                      ).place(x=150, y=600)


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
            raise ValueError("Nenhuma despesa selecionada")
        return int(selecionado[0])
    
    def confirmar_exclusao(self):
        try:
            id_despesa = self.pegar_id_selecionado()
            self.controller.deletar(id_despesa)
            self.carregar_tabela()
        except ValueError as e:
            print(e)


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
            self.atualizar_combobox()
            modal_cadastrar.grab_release()
            modal_cadastrar.destroy()

        

    def editar(self, modal_editar, id_despesa, nome, valor, data=None, observacao=None):
        if not nome.strip():
            raise ValueError("Nome da despesa é obrigatório")
        
        print(data)
        
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
            modal_editar.grab_release()
            modal_editar.destroy()


    def deletar(self, modal_deletar, id):
        try:
            self.despesa.excluir_despesa(id)
            self.tela.carregar_tabela()
        except ValueError as e:
            print(e)
        finally:
            modal_deletar.grab_release()
            modal_deletar.destroy()

    def listar(self):
        return self.despesa.listar_despesas()

    def total(self):
        return self.despesa.total_despesas()
    
    def atualizar_combobox(self, combobox):
        nomes = self.despesa.nome_despesas()

        for i in nomes:
            if i[0] not in self.tela.values:
                self.tela.values.append(i[0])

        combobox.configure(values=self.tela.values)

    def get_escolha(self, escolha):
       filtro = self.despesa.pesquisar_por_nome(escolha)

       self.tela.carregar_tabela(filtro)