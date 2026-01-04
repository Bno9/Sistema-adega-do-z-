from datetime import date, datetime

class Despesas():
    def __init__(self, con):
        self.con = con
        self.cur = self.con.cursor()
        self.cur.execute("""
                        CREATE TABLE IF NOT EXISTS despesas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        valor REAL NOT NULL,
                        data TEXT NOT NULL,
                        observacao TEXT
                        )""")
        self.con.commit()


    
    def adicionar_despesa(self, nome, valor, data=None, observacao=None):
        data_formatada = date.today().isoformat()
        try:
            if data:
                data_formatada = datetime.strptime(data, "%d/%m/%Y").date().isoformat()
        except ValueError:
            raise ValueError("Data inválida. Use DD/MM/AAAA")

        self.cur.execute(
                        "INSERT INTO despesas (nome, valor, data, observacao) VALUES (?, ?, ?, ?)",
                        (nome, valor, data_formatada, observacao)
                    )
        
        self.con.commit()
    
    def editar_despesa(self, id_despesa, nome, valor, data=None, observacao=None):
        try:
            if data:
                data = datetime.strptime(data, "%d/%m/%Y").date().isoformat()
        except ValueError:
            raise ValueError("Data inválida. Use DD/MM/AAAA")
        
        if data == None:
            self.cur.execute("""SELECT data FROM despesas WHERE id=?""", (id_despesa,))
            res = self.cur.fetchone()

            if res is None:
                raise ValueError("Despesa não encontrada")

            data = res[0]
        
        self.cur.execute(
                """
                UPDATE despesas
                SET nome = ?, valor = ?, data = ?, observacao = ?
                WHERE id = ?
                """,
                (nome, valor, data, observacao, id_despesa)
            )
        
        self.con.commit()

    def excluir_despesa(self, id_despesa):
        self.cur.execute("DELETE FROM despesas WHERE id=?",
                        (id_despesa,))
        
        if self.cur.rowcount == 0:
            raise ValueError("Despesa não encontrada")

        self.con.commit()
        return "Despesa excluida"

    def listar_despesas(self):
        self.cur.execute("SELECT * FROM despesas")
        return self.cur.fetchall()

    def total_despesas(self):
        self.cur.execute("SELECT SUM(valor) FROM despesas")
        total = self.cur.fetchone()[0]
        return total or 0