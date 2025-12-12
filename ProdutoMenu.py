class ProdutoMenu:

    def __init__(self, referencia_main):
        self.referencia_main = referencia_main

    def Menu(self):
        print("Testando menu de produto")
        
        self.referencia_main.change_state(self.referencia_main)