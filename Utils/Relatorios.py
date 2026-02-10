from datetime import date, datetime
import logging
import sqlite3
from Utils.Produto import Produto
from Utils.Resultado import Resultado

logger = logging.getLogger(__name__)

class Relatorios:
    def __init__(self, con, main):
        self.con = con
        self.cur = self.con.cursor()
        self.relatorio_estoque = RelatoriosEstoque(self.con, main)
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS movimentacao_caixa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            caixa_id INTEGER NOT NULL,
            data DATE NOT NULL,
            hora TIME NOT NULL,
            funcionario TEXT NOT NULL,
            tipo TEXT NOT NULL,
            total REAL NOT NULL,
            valor_pago REAL NOT NULL,
            desconto REAL DEFAULT 0,
            troco REAL DEFAULT 0,
            FOREIGN KEY (caixa_id) REFERENCES caixa(id))""")
        #tipo é sangria, venda_pix, venda_dinheiro

        self.cur.execute("""CREATE TABLE IF NOT EXISTS itens_movimentacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movimentacao_id INTEGER NOT NULL,
            codigo_produto TEXT NOT NULL,
            nome_produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            valor_unitario REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (movimentacao_id) REFERENCES movimentacao_caixa(id))""")

    def registrar_venda(self, produtos, valor_pago, desconto, metodo_pagamento, usuario, caixa_id):
        agora = datetime.now()
        data = date.today().strftime("%d/%m/%Y")
        hora = agora.strftime("%H:%M:%S")

        total_venda = 0
        for produto, quantidade in produtos:
            total_venda += produto.preco_venda * quantidade

        total_venda -= desconto
        troco = valor_pago - total_venda
        
        try:
            self.cur.execute("""
            INSERT INTO movimentacao_caixa
            (caixa_id, data, hora, funcionario, tipo, total, valor_pago, desconto, troco)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            caixa_id,
            data,
            hora,
            usuario,
            metodo_pagamento,
            total_venda,
            valor_pago,
            desconto,
            troco
        ))

            
            movimentacao_id = self.cur.lastrowid

            logger.info("Movimentação caixa criada utilizando o caixa_id=%s | movimentação ID=%s", caixa_id, movimentacao_id)

            for tupla in produtos:
                produto = tupla[0]
                quantidade = tupla[1]

                subtotal = produto.preco_venda * quantidade

                self.cur.execute("""
                    INSERT INTO itens_movimentacao
                    (movimentacao_id, codigo_produto, nome_produto, quantidade, valor_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    movimentacao_id,
                    produto.codigo,
                    produto.nome,
                    quantidade,
                    produto.preco_venda,
                    subtotal
                ))

                logger.info("Movimentação item=%s criado utilizando a movimentação_id=%s", produto.nome, movimentacao_id)
                self.con.commit()

        except (sqlite3.IntegrityError, sqlite3.DatabaseError) as e:
            self.con.rollback()
            logger.error("Erro ao registrar venda no banco de dados | erro=%s", e)

    def registrar_sangria(self, caixa_id, valor, observacao, usuario):
        agora = datetime.now()
        data = date.today().strftime("%d/%m/%Y")
        hora = agora.strftime("%H:%M:%S")

        try:
            self.cur.execute("""
                INSERT INTO movimentacao_caixa
                (caixa_id, data, hora, funcionario, tipo, total, valor_pago, desconto, troco)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                caixa_id,
                data,
                hora,
                usuario,
                "SANGRIA",
                valor,
                valor,
                0,
                0
            ))
            self.con.commit()
            return Resultado(True, "Sangria lançada", "sucesso", 2000)

        except Exception as e:
            self.con.rollback()
            raise e

    def mostrar_vendas(self, data=None):
        self.cur.execute("""SELECT id, caixa_id, data, hora, funcionario, tipo, total FROM movimentacao_caixa""")
        return self.cur.fetchall()
    
    def total_vendas(self, usuario, data):
        self.cur.execute("""SELECT id FROM caixa WHERE funcionario=? AND data=?""", (usuario, data))
        row = self.cur.fetchone()
        if not row:
            return 0  # não teve vendas

        caixa_id = row[0]
        logger.debug("caixa id=%s ",caixa_id)

        self.cur.execute("""
    SELECT COALESCE(SUM(i.valor_unitario * i.quantidade), 0)
    FROM itens_movimentacao i
    JOIN movimentacao_caixa m ON m.id = i.movimentacao_id
    WHERE m.caixa_id = ?
""", (caixa_id,))
        row = self.cur.fetchone()

        logger.debug("total vendas=%s", row[0])

        return row[0]
    
    def total_descontos(self, usuario, data):
        self.cur.execute("""SELECT id FROM caixa WHERE funcionario=? AND data=?""", (usuario, data))
        row = self.cur.fetchone()
        if not row:
            return 0  # não teve vendas

        caixa_id = row[0]
        logger.debug("caixa id=%s ",caixa_id)

        self.cur.execute("""
    SELECT COALESCE(SUM(desconto), 0)
    FROM movimentacao_caixa
    WHERE caixa_id = ?
""", (caixa_id,))
        row = self.cur.fetchone()

        logger.debug("total descontos=%s", row[0])

        return row[0]
    
    def total_sangrias(self, usuario, data):
        self.cur.execute("""SELECT id FROM caixa WHERE funcionario=? AND data=?""", (usuario, data))
        row = self.cur.fetchone()
        if not row:
            return 0  # não teve vendas

        caixa_id = row[0]
        logger.debug("caixa id=%s ",caixa_id)

        self.cur.execute("""
    SELECT COALESCE(SUM(total), 0)
    FROM movimentacao_caixa
    WHERE caixa_id = ? AND tipo = ?
""", (caixa_id, "SANGRIA"))
        row = self.cur.fetchone()

        logger.debug("total sangrias=%s", row[0])

        return row[0]
    
    def filtrar_vendas(self, usuario=None, data=None, forma_pagamento=None):
        if not data:
            data = date.today().strftime("%d/%m/%Y")

        sql = """
            SELECT *
            FROM movimentacao_caixa
            WHERE 1=1 AND data = ?
        """
        params = [data]

        if data:
            data_formatada = datetime.strptime(data, "%d/%m/%Y").date().strftime("%d/%m/%Y")
            params[0] = data_formatada

        if usuario:
            sql += " AND funcionario = ?"
            params.append(usuario)

        if forma_pagamento and forma_pagamento != "Tudo":
            sql += " AND tipo = ?"
            params.append(forma_pagamento)

        self.cur.execute(sql, params)
        return self.cur.fetchall()

    def retornar_produtos(self, mov_id):
        self.cur.execute("""SELECT codigo_produto, nome_produto, quantidade, valor_unitario, subtotal FROM itens_movimentacao WHERE movimentacao_id=?""", mov_id)
        row = self.cur.fetchall()
        return row
    
    def mais_vendidos(self):
        self.cur.execute("""
    SELECT
        i.codigo_produto,
        i.nome_produto,
        SUM(i.quantidade) AS total_vendido
    FROM itens_movimentacao i
    JOIN movimentacao_caixa m ON m.id = i.movimentacao_id
    GROUP BY i.codigo_produto, i.nome_produto
    ORDER BY total_vendido DESC
    LIMIT 10
""")

        rows = self.cur.fetchall()
        return rows

    

class RelatoriosEstoque():
    def __init__(self, con, main):
        self.con = con
        self.cur = self.con.cursor()
        self.main = main

        self.cur.execute("""CREATE TABLE IF NOT EXISTS movimentacao_estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATE NOT NULL,
            hora TIME NOT NULL,
            funcionario TEXT NOT NULL,
            tipo_movimento TEXT NOT NULL,
                         
            produto_codigo_antes TEXT,
            produto_codigo_depois TEXT,
            
            produto_nome_antes TEXT,
            produto_nome_depois TEXT,
                         
            preco_antes REAL,
            preco_depois REAL,
                         
            observacao TEXT,
                         
            quantidade_antes INTEGER,
            quantidade_depois INTEGER)"""
                         )
        #tipo é saída, entrada, alteração

    def registrar_movimento_estoque(self, produto: Produto, tipo, usuario):
        agora = datetime.now()
        data = date.today().strftime("%d/%m/%Y")
        hora = agora.strftime("%H:%M:%S")

        self.cur.execute("""INSERT INTO movimentacao_estoque (data, hora, funcionario, tipo_movimento, produto_codigo_depois, produto_nome_depois, preco_depois, quantidade_depois) VALUES (?,?,?,?,?,?,?,?)""", (data, hora, usuario, tipo, produto.codigo, produto.nome, produto.preco_venda, produto.quantidade))
        self.con.commit()

    def registrar_alteracao_estoque(self, produto_antes: Produto, produto_depois: Produto, tipo, usuario, observacao=None):
        agora = datetime.now()
        data = date.today().strftime("%d/%m/%Y")
        hora = agora.strftime("%H:%M:%S")

        self.cur.execute("""
            INSERT INTO movimentacao_estoque (
                data, hora, funcionario, tipo_movimento,

                produto_codigo_antes,
                produto_codigo_depois,

                produto_nome_antes,
                produto_nome_depois,

                preco_antes,
                preco_depois,

                quantidade_antes,
                quantidade_depois,

                observacao
            )
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            data,
            hora,
            usuario,
            tipo,

            produto_antes.codigo,
            produto_depois.codigo,

            produto_antes.nome,
            produto_depois.nome,

            produto_antes.preco_venda,
            produto_depois.preco_venda,

            produto_antes.quantidade,
            produto_depois.quantidade,

            observacao
        ))

        self.con.commit()
    
    def filtrar_movimentos(self, usuario=None, data=None, tipo=None):
        if not data:
            data = date.today().strftime("%d/%m/%Y")

        sql = """
            SELECT *
            FROM movimentacao_estoque
            WHERE 1=1 AND data = ?
        """
        params = [data]

        if data:
            data_formatada = datetime.strptime(data, "%d/%m/%Y").date().strftime("%d/%m/%Y")
            params[0] = data_formatada

        if usuario:
            sql += " AND funcionario = ?"
            params.append(usuario)

        if tipo and tipo != "Tudo":
            sql += " AND tipo_movimento = ?"
            params.append(tipo)

        self.cur.execute(sql, params)
        return self.cur.fetchall()

    def retornar_movimentacao_estoque(self, id):
        self.cur.execute("""SELECT * FROM movimentacao_estoque WHERE id=?""", id)
        row = self.cur.fetchone()
        return row