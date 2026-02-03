class Relatorios:
    def __init__(self, con, main):
        self.con = con
        self.cur = self.con.cursor()
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS movimentacao_caixa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            caixa_id INTEGER NOT NULL,
            data DATE NOT NULL,
            hora TIME NOT NULL,
            funcionario TEXT NOT NULL,
            tipo TEXT NOT NULL,
            valor REAL NOT NULL,
            troco REAL DEFAULT 0,
            FOREIGN KEY (caixa_id) REFERENCES caixa(id))""")
        #tipo é sangria, venda_pix, venda_dinheiro