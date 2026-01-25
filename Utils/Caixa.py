from Utils.Recibo import Recibo, ImpressoraBase, ImpressoraTxt, ImpressoraWindows
from Utils.Resultado import Resultado
import logging

logger = logging.getLogger(__name__)

class Caixa:
    
    def __init__(self, estoque, iniciar_impressora, con):
        self.recibo = Recibo()
        self.iniciar_impressora = iniciar_impressora
        self.estoque = estoque
        self.con = con
        self.vendas = []
        self.itens_no_carrinho = []
        self.itens_passados = []
        self.desconto = 0

    def carrinho_caixa(self, produto, quantidade=1):
        """Método que adiciona os produtos a tela de soma do caixa"""

        for i, (item, quantidade_atual) in enumerate(self.itens_no_carrinho):
            if produto.codigo == item.codigo:
                self.itens_no_carrinho[i] = (item, quantidade_atual + quantidade)
                logger.info("Quantidade=%d adicionada ao produto=%s", quantidade, item.nome)
                return

        self.itens_no_carrinho.append((produto, quantidade))

    def finalizar_compra(self, valor_pago, metodo_pagamento):
        """Método que finaliza a compra e da baixa no estoque"""
        
        if not self.itens_no_carrinho:
            return Resultado(False, "Nenhum item registrado", "aviso", 5000)

        total = self.total()

        try:
            valor_pago = float(valor_pago)
        except ValueError:
            logger.error("Erro ao converter valor pago para float | valor_pago=%s", valor_pago)
            return Resultado(False, "Erro de processamento", "erro", 5000)

        if valor_pago < total or valor_pago > 100000:
            logger.warning("Valor recebido inválido | valor=%s", valor_pago)
            return Resultado(False, "Valor recebido inválido", "aviso", 5000)

        troco = valor_pago - total
        
        for item, quantidade in self.itens_no_carrinho:
            self.estoque.dar_baixa(item.codigo, quantidade)

        self.vendas.append({
            "itens": [{"codigo": p.codigo, "nome": p.nome, "quantidade": q, "total_produto": p.preco_venda*q} for p, q in self.itens_no_carrinho],
            "total": total,
            "recebido": valor_pago,
            "metodo pagamento": metodo_pagamento,
            "troco": troco
        })

        linhas = self.recibo.gerar_linhas(self.itens_no_carrinho, valor_pago, self.desconto)
        itens = [i[0].codigo for i in self.itens_no_carrinho]
        logger.info("Compra finalizada | valor_total=%s | metodo_pagamento=%s | troco=%s | itens=%s", total, metodo_pagamento, troco, itens)

        self.itens_no_carrinho.clear()
        self.alternar_compra()

        return Resultado(True, "", "info", 1000000, {"total": total,
                                                                              "troco": troco,
                                                                              "linhas": linhas})
    
    def aplicar_desconto(self, valor):
        if valor == "":
            self.desconto = 0
            return self.total()
        
        try:
            valor = int(valor)
        except ValueError:
            logger.error("Valor de desconto inválido | valor=%s", valor)
            return Resultado(False, "Digite apenas numeros", "erro", 5000)
        
        if valor < 0:
            self.desconto = 0
            return self.total()
        
        self.desconto = valor
        
        if self.total() < 0:
            self.desconto = 0
            logger.warning("Entrada de desconto maior que valor total dos produtos")
            return Resultado(False, "Desconto maior que o valor dos produtos", "erro", 5000)
        
        return self.total()
        
    def imprimir_recibo(self, linhas, cpf=None):
        logger.debug("Cpf=%s recebido", cpf)
        logger.debug("linhas=%s", linhas)
        if cpf == "":
            return
        
        impressora = self.iniciar_impressora() #se for trocar aqui pra testes nao posso esquecer que o quee ta vindo no self é uma função, então vai dar nonetype caso eu nao mude a main
        impressora.imprimir(linhas)

    def total(self):
        if self.desconto:
            logger.debug("Desconto aplicado | Desconto=%s", self.desconto)
            return sum(item.preco_venda * quantidade for item, quantidade in self.itens_no_carrinho) - self.desconto
    
        return sum(item.preco_venda * quantidade for item, quantidade in self.itens_no_carrinho)
    
    def listar_vendas(self): 
        for venda in self.vendas:
            print(venda) #ainda incompleto (pretendo fazer uma tela ou um bloco de notas para exibir essa parte)

    def validar_compra_existente(self):
        """Método para validar se existe uma compra pendente
        Usado para evitar o fechamento do caixa sem finalizar a compra"""

        if self.itens_no_carrinho:
            logger.warning("Tentativa de fechar caixa com produto registrado")
            return Resultado(False, "Finalize a compra primeiro", "info")

        return Resultado(True)

    def validar_codigo(self, codigo_produto, quantidade=1):
        if quantidade < 0:
             logger.warning("Quantidade não pode ser negativa")
             return Resultado(False, "Quantidade não pode ser negativa", "erro", 5000)

        if self.estoque.conferir_se_existe_no_estoque(codigo_produto):
            cursor_estoque = self.estoque.cur
            cursor_estoque.execute("SELECT * FROM produtos WHERE codigo=?", (codigo_produto,))
            row = cursor_estoque.fetchone()

            try:
                dados = {
                    "codigo": row[1],
                    "nome": row[2],
                    "tipo": row[3],
                    "preco_custo": float(row[4]),
                    "preco_venda": float(row[5]),
                    "quantidade": int(row[6]),
                    "id_produto_pai": int(row[7])
                        if row[7] is not None  else None,
                    "quantidade_fardo": int(row[8])
                        if row[8] is not None else None
                }
            except ValueError:
                logger.error("Erro ao processar dados")
                return Resultado(False, "Erro de processamento", "erro")

            from Utils.Produto import Produto
            produto = Produto(**dados)
        
            self.carrinho_caixa(produto, quantidade) 
            logger.info("Item registrado no caixa | item=%s quantidade=%d", produto, quantidade)
            return Resultado(True)

        logger.warning("Produto não encontrado")
        return Resultado(False, "Produto não encontrado", "aviso", 5000)

    def excluir_do_carrinho(self, produto_codigo):
        for i, (item, _) in enumerate(self.itens_no_carrinho):
            if produto_codigo == item.codigo:
                del self.itens_no_carrinho[i]
                logger.info("Produto excluido do carrinho | nome=%s", item.nome)
                return True
            
    def alternar_compra(self):
        if self.itens_passados:
            logger.debug("Itens da compra pendente copiados para tela atual")
            intermediario = self.itens_no_carrinho
            self.itens_no_carrinho = self.itens_passados.copy()
            self.itens_passados = intermediario
            self.desconto = 0
            logger.debug(self.itens_no_carrinho)
            if not self.itens_passados:
                print("retomou")
                return "Retomou"

            return "Pendente"
        
        if not self.itens_no_carrinho:
            return False
        
        self.itens_passados = self.itens_no_carrinho.copy()
        self.itens_no_carrinho.clear()
        self.desconto = 0
        logger.debug("Itens da tela colocados em pendencia")
        logger.debug(self.itens_passados)
        
        return "Pendente"