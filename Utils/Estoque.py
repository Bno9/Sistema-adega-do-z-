from Utils.Resultado import Resultado
from Utils.Produto import Produto
import logging

logger = logging.getLogger(__name__)

class Estoque:
    """Classe que armazena os produtos cadastrados e suas informações"""

    def __init__(self, con, relatorios):
        self.con = con
        self.cur = self.con.cursor()
        self.relatorios = relatorios
        self.cur.execute("""
                        CREATE TABLE IF NOT EXISTS produtos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        codigo TEXT NOT NULL,
                        nome TEXT NOT NULL,
                        tipo TEXT NOT NULL,
                        preco_custo REAL NOT NULL,
                        preco_venda REAL NOT NULL,
                        quantidade INTEGER,
                        id_produto_pai INTEGER,
                        quantidade_fardo INTEGER
                        )""")
        self.con.commit()

    def criar_produto(self, **dados: dict):
        obj_produto = Produto(**dados) #Cria o objeto produto usando a classe Produto

        if obj_produto.preco_custo <= 0 or obj_produto.preco_venda <= 0:
            return Resultado(False, "Preço nao pode ser igual ou menor que 0", "aviso", 2000)

        if self.conferir_se_existe_no_estoque(obj_produto.codigo):
            return True
        
        #busca o código do produto referenciado e pega o id dele
        if obj_produto.id_produto_pai:
            self.cur.execute("SELECT id FROM produtos WHERE codigo=?", (obj_produto.id_produto_pai,))
            produto = self.cur.fetchone()
            obj_produto.id_produto_pai = produto[0] if produto else None

        #insere o produto na tabela         
        self.cur.execute("INSERT INTO produtos (codigo, nome, tipo, preco_custo, preco_venda, quantidade, id_produto_pai, quantidade_fardo) VALUES (?,?,?,?,?,?,?,?)",
                         (obj_produto.codigo, obj_produto.nome, obj_produto.tipo, obj_produto.preco_custo, obj_produto.preco_venda, obj_produto.quantidade, obj_produto.id_produto_pai, obj_produto.qtd_fardo))
        self.con.commit()

        self.relatorios.relatorio_estoque.registrar_movimento_estoque(obj_produto, "Registro", dados.get("funcionario", "Erro"))

        logger.info("Produto=%s criado com sucesso", obj_produto.nome)
        return Resultado(True, f"{obj_produto.nome} criado", "sucesso")
      
    def remover_produto(self, **dados):
        obj_produto_antes = Produto(**dados)
        obj_produto_depois = Produto()
        self.cur.execute("DELETE FROM produtos WHERE codigo=?", (dados.get("codigo"),))
        self.con.commit()
        if self.cur.rowcount>0:
            logger.info("Código=%s removido com sucesso", dados.get("codigo"))
            self.relatorios.relatorio_estoque.registrar_alteracao_estoque(obj_produto_antes, obj_produto_depois, "Exclusao", dados.get("funcionario", "Erro"))
            return Resultado(True, "Produto removido com sucesso", "sucesso") 
            
        
        logger.info("Produto com código=%s não encontrado", dados.get("codigo"))
        Resultado(False, "Produto não encontrado", "info")
    
    def atualizar_produto(self, dados: dict):
        self.cur.execute("SELECT * FROM produtos WHERE codigo=?", (dados.get("codigo"),))
        row = self.cur.fetchone()
        try:
            dados_antigo = {
                "codigo": row[1],
                "nome": row[2],
                "tipo": row[3],
                "preco_custo": row[4],
                "preco_venda": row[5],
                "quantidade": row[6],
                "id_produto_pai": row[7]
                    if row[7] else None,
                "quantidade_fardo": row[8]
                    if row[8] else None
            }
        except ValueError:
            logger.error("Erro ao gerar dados para atualizar produto")
            return None
        

        if dados["preco_custo"] <= 0 or dados["preco_venda"] <= 0:
            return Resultado(False, "Preço nao pode ser igual ou menor que 0", "aviso", 2000)
        
        codigo = dados.pop("codigo")

        campos = []
        valores = []

        for campo, valor in dados.items():
            if campo == "funcionario":
                continue
            campos.append(f"{campo} = ?")
            valores.append(valor)

        valores.append(codigo)

        sql = f"""
            UPDATE produtos
            SET {', '.join(campos)}
            WHERE codigo = ?
        """

        self.cur.execute(sql, valores)
        self.con.commit()

        if self.cur.rowcount == 0:
            logger.info("Produto não encontrado")
            return Resultado(False, "Produto não encontrado", "info")

        dados["codigo"] = dados_antigo.get("codigo")
        produto_novo = Produto(**dados)
        produto_antigo = Produto(**dados_antigo)
        self.relatorios.relatorio_estoque.registrar_alteracao_estoque(produto_antigo, produto_novo, "Alteraçao_dados", dados.get("funcionario", "Erro"))     
        logger.info("Produto=%s atualizado com sucesso", dados["nome"])
        return Resultado(True, "Produto atualizado com sucesso", "sucesso")
    
    def alterar_codigo(self, codigo_atual, codigo_novo, dados):
        self.cur.execute(f"SELECT * FROM produtos WHERE codigo=?", (codigo_atual,))
        produto = self.cur.fetchone()
        id_produto = produto[0]
        self.cur.execute(f"UPDATE produtos SET codigo=? WHERE id=?", (codigo_novo, id_produto))
        self.con.commit()
        produto_antigo = Produto(**dados)
        dados["codigo"] = codigo_novo
        produto_novo = Produto(**dados)
        self.relatorios.relatorio_estoque.registrar_alteracao_estoque(produto_antigo, produto_novo, "Alteraçao_codigo", dados.get("funcionario", "Erro"))
        logger.info("Código do produto=%s alterado para código=%s | Código_antigo=%s", produto[2], codigo_novo, codigo_atual)

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

        if quantidade_atualizada <= 0 and tem_pai:
            self.cadastro_automatico(codigo_produto)

    def cadastro_automatico(self, codigo_produto):
        """
        Docstring para cadastro_automatico
        
        :param self: Classe EstoqueMenu
        :param codigo_produto: produto com quantidade menor que 0
        """

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

    def estoque_baixo(self, quantidade_aviso):
        self.cur.execute("SELECT * FROM produtos")
        row = self.cur.fetchall()

        produtos = []

        for produto in row:
            quantidade = produto[6]

            if quantidade <= quantidade_aviso:
                produtos.append(produto)
        

        return produtos if produtos else None