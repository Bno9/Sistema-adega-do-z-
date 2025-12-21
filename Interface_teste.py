from tkinter import ttk 
from tkinter import *



class Menu:


    def escolha(self):
        escolha = int(escolha_menu.get())


        if escolha == 1:
            print("Entrou no caixa da classe")
    
        elif escolha == 2:
            print("Entrou no estoque da classe")

        elif escolha == 3:
            print("Entrou no cadastro da classe")

        else:
            print("Opção inválida")

m = Menu()
        

def menus():
    
    escolha = int(escolha_menu.get())


    if escolha == 1:
        print("Entrou no caixa")
    
    elif escolha == 2:
        print("Entrou no estoque")

    elif escolha == 3:
        print("Entrou no cadastro")

    else:
        print("Opção inválida")


root = Tk()
root.title("Menu principal")

mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))

mainframe.grid(column=10, row=10, sticky=(N, W, E, S))

escolha_menu = StringVar()
escolha_menu_entry = ttk.Entry(mainframe, width=20, textvariable=escolha_menu)
escolha_menu_entry.grid(column=3, row=1, sticky=(W, E))

ttk.Label(mainframe, text="""Escolha uma das opções:
1- caixa
2- estoque
3- cadastro""").grid(column=1, row=1, sticky=W)

ttk.Button(mainframe, text="Escolher", command=m.escolha).grid(column=5, row=1, sticky=W)

root.mainloop()

