import customtkinter as ctk

class RelatoriosMenu(ctk.CTkToplevel):
    def __init__(self, master, main):
        self.main = main
        super().__init__(master=master, fg_color="#1e1e1e")

        self.title("Relatórios")
        self.geometry("400x400")

        self.transient(master)
        self.update_idletasks()
        self.grab_set()   

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0,1), weight=1)
        header =  ctk.CTkFrame(self, fg_color="#1e1e1e")
        checks =  ctk.CTkFrame(self, fg_color="#1e1e1e")

        header.grid(row=0, column=0)
        header.rowconfigure(0, weight=1)

        checks.rowconfigure((0,1), weight=1)
        checks.columnconfigure(0, weight=1)
        checks.grid(row=1, column=0, sticky="nsew")

        ctk.CTkLabel(header, 
                    text="Escolha um relatorio",
                    width=300,
                    font=("arial", 32, "bold")
                    ).grid(row=0, column=0)
        
        self.protocol("WM_DELETE_WINDOW", self.master.quit)
