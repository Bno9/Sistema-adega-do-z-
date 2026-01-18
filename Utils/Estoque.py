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
                        tipo TEXT NOT NULL,
                        preco_custo REAL NOT NULL,
                        preco_venda REAL NOT NULL,
                        quantidade INTEGER,
                        id_produto_pai INTEGER,
                        quantidade_fardo INTEGER
                        )""")
        self.con.commit()

    def criar_produto(self, *args):
        from Utils.Produto import Produto

        obj_produto = Produto(*args) #Cria o objeto produto usando a classe Produto

        if self.conferir_se_existe_no_estoque(obj_produto.codigo):
            return {"Status": "Erro",
                    "Mensagem": "Um item já está cadastrado com esse código"}
        
        #busca o código do produto referenciado e pega o id dele
        self.cur.execute("SELECT id FROM produtos WHERE codigo=?", (obj_produto.id_produto_pai,))
        produto = self.cur.fetchone()
        if produto:
            obj_produto.id_produto_pai = produto[0]

        #insere o produto na tabela         
        self.cur.execute("INSERT INTO produtos (codigo, nome, tipo, preco_custo, preco_venda, quantidade, id_produto_pai, quantidade_fardo) VALUES (?,?,?,?,?,?,?,?)",
                         (obj_produto.codigo, obj_produto.nome, obj_produto.tipo, obj_produto.preco_custo, obj_produto.preco_venda, obj_produto.quantidade, obj_produto.id_produto_pai, obj_produto.qtd_fardo))
        self.con.commit()

        return {"Status": "Sucesso",
                "Mensagem": f"{obj_produto.nome} criado"}
      
    def remover_produto(self, codigo_produto):
        self.cur.execute("DELETE FROM produtos WHERE codigo=?", (codigo_produto,))
        self.con.commit()
        return "Produto removido com sucesso" if self.cur.rowcount>0 else "Produto não encontrado"
    
    def atualizar_produto(self, codigo_produto, atributos: list):
        colunas_validas = ["codigo", "nome", "preco_custo", "preco_venda", "quantidade"]
        if atributo not in colunas_validas:
            return "Atributo inválido!"
        
        if atributo == "codigo":
            if self.conferir_se_existe_no_estoque(valor_novo):
                return"Já existe um item com o mesmo código"
        
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

    def conferir_se_existe_no_estoque(self, codigo_produto):
        self.cur.execute("SELECT 1 FROM produtos WHERE codigo=? LIMIT 1", (codigo_produto,))
        return self.cur.fetchone() is not None
    
    def get_produto(self,codigo_produto):
        """Retorna uma linha do banco de dados"""
        self.cur.execute("SELECT * FROM produtos WHERE codigo=?", (codigo_produto,))
        return self.cur.fetchone()
    
    def filtrar_produto(self, coluna, digitado):
        """
        Método que busca itens por nome ou codigo no banco de dados
        
        :param self: Classe EstoqueMenu
        :param coluna: coluna de nome ou código do banco de dados
        :param digitado: string digitada no entry da interface

        return: todas linhas do banco que comecem com o que foi digitado
        """

        digitado = f"{digitado}%"
        self.cur.execute(f"SELECT * FROM produtos WHERE {coluna} LIKE ?", (digitado,))
        return self.cur.fetchall()

    def get_banco(self):
        """Retorna todo o banco de dados"""
        self.cur.execute("SELECT * FROM produtos")
        return self.cur.fetchall()

    def dar_baixa(self, codigo_produto, quantidade_baixa):
        """
        Docstring para dar_baixa
        
        :param self: Classe EstoqueMenu
        :param codigo_produto: Descrição
        :param quantidade_baixa: Valor para diminuir 
        """

        self.cur.execute("SELECT * FROM produtos WHERE codigo=?", (codigo_produto,))
        produto = self.cur.fetchone()
        quantidade_atualizada = produto[6] - quantidade_baixa
        tem_pai = produto[7] is not None

        self.cur.execute("UPDATE produtos SET quantidade=? WHERE codigo=?", (quantidade_atualizada, codigo_produto))
        self.con.commit()

        print(f"produto {produto[3]} tem {quantidade_atualizada} quantidade e tem pai:{tem_pai}")
        if quantidade_atualizada <= 0 and tem_pai:
            self.cadastro_automatico(codigo_produto)

    def cadastro_automatico(self, codigo_produto):
        """
        Docstring para cadastro_automatico
        
        :param self: Classe EstoqueMenu
        :param codigo_produto: produto com quantidade menor que 0
        """

        print("Chegou no cadastro automatico")

        self.cur.execute("SELECT quantidade,id_produto_pai FROM produtos WHERE codigo=?", (codigo_produto,))
        produto_filho = self.cur.fetchone()
        produto_pai_id = produto_filho[1]

        self.cur.execute("SELECT quantidade,quantidade_fardo FROM produtos WHERE id=?", (produto_pai_id,))
        produto_pai = self.cur.fetchone()
        if produto_pai[0] <=0:
            return
        
        quantidade_pai_atualizada = produto_pai[0] - 1
        quantidade_fardo = produto_pai[1]

        self.cur.execute("UPDATE produtos SET quantidade=? WHERE id=?", (quantidade_pai_atualizada, produto_pai_id))
        self.con.commit()

        self.cur.execute("UPDATE produtos SET quantidade=? WHERE codigo=?", (quantidade_fardo, codigo_produto))
        self.con.commit()

        #tambem preciso arrumar o coisa de editar produto e o deletar item do caixa