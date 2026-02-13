from datetime import date, datetime
from Utils.Resultado import Resultado
import logging

logger = logging.getLogger(__name__)

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
        data_formatada = datetime.today().isoformat()

        if data:
                try:
                    if isinstance(data, str):
                        data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
                    else:
                        data_formatada = data.strftime("%Y-%m-%d")
                except Exception:
                    logger.warning("Data recebida inválida -> Data=%s", data)
                    return Resultado(False, "Data inválida. Use DD/MM/AAAA", "erro", 6000)
        
        if not observacao:
            observacao = ""

        self.cur.execute(
                        "INSERT INTO despesas (nome, valor, data, observacao) VALUES (?, ?, ?, ?)",
                        (nome, valor, data_formatada, observacao)
                    )
        
        self.con.commit()
        logger.info("Despesa criada | nome=%s | valor=%.2f | data=%s | observacao=%s", nome, valor, data_formatada, observacao)
        return Resultado(True, "Despesa criada", "sucesso")
    
    def editar_despesa(self, id_despesa, nome, valor, data="", observacao=""):
        if data:
            try:
                if isinstance(data, str):
                    data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
                else:
                    data_formatada = data.strftime("%Y-%m-%d")
            except Exception:
                logger.warning("Data recebida inválida -> Data=%s", data)
                return Resultado(False, "Data inválida. Use DD/MM/AAAA", "erro", 6000)


        if data == "":
            self.cur.execute("""SELECT data FROM despesas WHERE id=?""", (id_despesa,))
            res = self.cur.fetchone()

            if res is None:
                logger.warning("Data não encontrada no banco de dados | Data=%s | resultado_Banco=%s", data, res)
                return Resultado(False, "Data não encontrada no banco de dados", "erro")

            data_formatada = res[0]

        if observacao == "":
            self.cur.execute("""SELECT observacao FROM despesas WHERE id=?""", (id_despesa,))
            res = self.cur.fetchone()

            if res is None:
                logger.warning("Obersvaçao não encontrada no banco de dados | Observacao=%s | resultado_Banco=%s", observacao, res)
                return Resultado(False, "Observação não encontrada no banco de dados", "erro")
            observacao = res[0]
        
        self.cur.execute(
                """
                UPDATE despesas
                SET nome = ?, valor = ?, data = ?, observacao = ?
                WHERE id = ?
                """,
                (nome, valor, data_formatada, observacao, id_despesa)
            )
        
        self.con.commit()
        logger.info("Despesa editada | nome=%s | valor=%.2f | data=%s | observacao=%s", nome, valor, data, observacao)
        return Resultado(True, "Editado com sucesso", "sucesso")

    def excluir_despesa(self, id_despesa):
        self.cur.execute("DELETE FROM despesas WHERE id=?",
                        (id_despesa,))
        
        if self.cur.rowcount == 0:
            logger.warning("Despesa não encontrada para exclusao | id_despesa=%s", id_despesa)
            return Resultado(False, "Despesa não encontrada", "erro")

        self.con.commit()
        logger.info("Despesa excluida | id_despesa=%s", id_despesa)
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