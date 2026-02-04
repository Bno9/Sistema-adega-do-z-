from datetime import date, datetime
import logging
import sqlite3

logger = logging.getLogger(__name__)

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
        data = date.today().isoformat()
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