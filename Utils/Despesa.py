from datetime import date, datetime
from Utils.Resultado import Resultado

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
            return Resultado(False, "Data inválida. Use DD/MM/AAAA", "erro", 6000)
        
        if not observacao:
            observacao = ""

        self.cur.execute(
                        "INSERT INTO despesas (nome, valor, data, observacao) VALUES (?, ?, ?, ?)",
                        (nome, valor, data_formatada, observacao)
                    )
        
        self.con.commit()
        return Resultado(True, "Despesa criada", "sucesso")
    
    def editar_despesa(self, id_despesa, nome, valor, data="", observacao=""):
        try:
            if data:
                data = datetime.strptime(data, "%d/%m/%Y").date().isoformat()
        except ValueError:
            return Resultado(False, "Data inválida. Use DD/MM/AAAA", "erro", 6000)
        
        if data == "":
            self.cur.execute("""SELECT data FROM despesas WHERE id=?""", (id_despesa,))
            res = self.cur.fetchone()

            if res is None:
                return Resultado(False, "Data não encontrada no banco de dados", "erro")

            data = res[0]

        if observacao == "":
            self.cur.execute("""SELECT observacao FROM despesas WHERE id=?""", (id_despesa,))
            res = self.cur.fetchone()

            if res is None:
                return Resultado(False, "Observação não encontrada no banco de dados", "erro")
            observacao = res[0]
        
        self.cur.execute(
                """
                UPDATE despesas
                SET nome = ?, valor = ?, data = ?, observacao = ?
                WHERE id = ?
                """,
                (nome, valor, data, observacao, id_despesa)
            )
        
        self.con.commit()
        return Resultado(True, "Editado com sucesso", "sucesso")

    def excluir_despesa(self, id_despesa):
        self.cur.execute("DELETE FROM despesas WHERE id=?",
                        (id_despesa,))
        
        if self.cur.rowcount == 0:
            return Resultado(False, "Despesa não encontrada", "erro")

        self.con.commit()
        return Resultado(True, "Despesa excluida", "sucesso")
        
    def listar_despesas(self):
        self.cur.execute("SELECT * FROM despesas")
        return self.cur.fetchall()

    def total_despesas(self):
        self.cur.execute("SELECT SUM(valor) FROM despesas")
        total = self.cur.fetchone()[0]
        return total or 0
    
    def total_filtrado(self, nome_despesa):
        self.cur.execute("SELECT SUM(valor) FROM despesas WHERE nome=?", (nome_despesa,))
        total = self.cur.fetchone()[0]
        return total or 0
    
    def nome_despesas(self):
        self.cur.execute("SELECT DISTINCT nome FROM despesas")
        return self.cur.fetchall()
    
    def pesquisar_por_nome(self, nome_despesa):
        self.cur.execute("SELECT * FROM despesas WHERE nome=?", (nome_despesa,))
        return self.cur.fetchall()