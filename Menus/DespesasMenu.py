import customtkinter as ctk

class DespesasMenu(ctk.CTkFrame):
    
    def __init__(self, root, referencia_main) :   
        super().__init__(master=root, fg_color="#1e1e1e")

        self.referencia_main = referencia_main

        #texto
        self.status = ctk.StringVar()

        #frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.frame_conteudo = ctk.CTkFrame(self, fg_color="#1e1e1e")
        self.frame_conteudo.grid(row=0, column=0, sticky="nsew")
        self.frame_conteudo.columnconfigure(0, weight=1)
        self.frame_conteudo.rowconfigure((0,1,2,3,4,5,6), weight=1)
