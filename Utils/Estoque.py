class Estoque:
    """Classe que armazena os produtos cadastrados e suas informações"""

    def __init__(self, con):
        self.con = con
        self.cur = self.con.cursor()
        self.cur.execute("""
                        CREATE TABLE IF NOT EXISTS produtos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        codigo INTEGER NOT NULL,
                        nome TEXT NOT NULL,
                        preco_custo REAL NOT NULL,
                        preco_venda REAL NOT NULL,
                        quantidade INTEGER
                        )""")
        self.con.commit()

    def criar_produto(self, *args):
        from Utils.Produto import Produto

        obj_produto = Produto(*args) #Cria o objeto produto usando a classe Produto

        if self.conferir_se_existe_no_estoque(obj_produto.codigo):
            return "Um item já está cadastrado com esse código"
                 
        self.cur.execute("INSERT INTO produtos (codigo, nome, preco_custo, preco_venda, quantidade) VALUES (?,?,?,?,?)",
                         (obj_produto.codigo, obj_produto.nome, obj_produto.preco_custo, obj_produto.preco_venda, obj_produto.quantidade))
        self.con.commit()

        return f"item {obj_produto.nome} criado"
      
    def remover_produto(self, codigo_produto):
        self.cur.execute("DELETE FROM produtos WHERE codigo=?", (codigo_produto,))
        self.con.commit()
        return "Produto removido com sucesso" if self.cur.rowcount>0 else "Produto não encontrado"
    
    def atualizar_produto(self, codigo_produto, atributo, valor_novo):
        colunas_validas = ["codigo", "nome", "preco_custo", "preco_venda", "quantidade"]
        if atributo not in colunas_validas:
            return "Atributo inválido!"
        
        try:
            if atributo in ["codigo", "quantidade"]:
                valor_novo = int(valor_novo)
            elif atributo in ["preco_custo", "preco_venda"]:
                valor_novo = float(valor_novo)
            elif atributo == "nome":
                valor_novo = valor_novo
        except ValueError:
            return "Valor inválido"
    
        sql = f"UPDATE produtos SET {atributo}=? WHERE codigo=?"
        self.cur.execute(sql, (valor_novo, codigo_produto))
        self.con.commit()
        return "Produto alterado com sucesso!"

    def dar_baixa(self, codigo_produto, quantidade_baixa):
        self.cur.execute("SELECT quantidade FROM produtos WHERE codigo=?", (codigo_produto,))
        produto = self.cur.fetchone()
        quantidade_atualizada = produto[0] - quantidade_baixa

        self.cur.execute("UPDATE produtos SET quantidade=? WHERE codigo=?", (quantidade_atualizada, codigo_produto))

        self.con.commit()

    def conferir_se_existe_no_estoque(self, codigo_produto):
        self.cur.execute("SELECT 1 FROM produtos WHERE codigo=? LIMIT 1", (codigo_produto,))
        return self.cur.fetchone() is not None
    
    def get_produto(self,codigo_produto):
        """Retorna uma linha do banco de dados"""
        self.cur.execute("SELECT * FROM produtos WHERE codigo=?", (codigo_produto,))
        return self.cur.fetchone()


    def get_banco(self):
        """Retorna todo o banco de dados"""
        self.cur.execute("SELECT * FROM produtos")
        return self.cur.fetchall()