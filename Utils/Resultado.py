class Resultado:
    def __init__(self, sucesso: bool, mensagem="", tipo="info", tempo=3000, dados=None):
        self.sucesso = sucesso
        self.mensagem = mensagem
        self.tipo = tipo
        self.tempo = tempo
        self.dados = {} if dados is None else dados
        self.mapa = {"sucesso": "green",
                "erro": "red",
                "aviso": "yellow",
                "info": "white"
                }
        self.cor = self.mapa.get(self.tipo, "white")