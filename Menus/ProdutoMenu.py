class ProdutoMenu:

    def __init__(self, referencia_main):
        self.referencia_main = referencia_main


    def Menu(self):
        print("""
        Menu de cadastro de produtos
        
        1- Cadastrar produto
        2- Editar produto
        3- Sair
        """)

        escolha = int(input("Digite a opção desejada: "))

        if escolha == 1:
            from Utils.Produto import Produto

            print("Digite as informações do produto")

            codigo = int(input("Leia ou digite o codigo do produto: "))
            nome = input("Nome do produto: ")
            preco_custo = float(input("Preço de custo: "))
            preco_venda = float(input("Preço de venda: "))
            quantidade = int(input("Quantidade: "))

            objeto_produto = Produto(codigo, nome, preco_custo, preco_venda, quantidade)
            self.referencia_main.estoque.adicionar_produto(objeto_produto)

        elif escolha == 2:

            codigo_produto = int(input("Digite ou leia o código do produto que deseja alterar: "))

            if codigo_produto in self.referencia_main.estoque.itens:

                produto = self.referencia_main.estoque.itens[codigo_produto]

                mapa = {
                    "1": "codigo",
                    "2": "nome",
                    "3": "preco_custo",
                    "4": "preco_venda",
                    "5": "quantidade"
                }

                print("""Escolha o que deseja alterar
                1- Código
                2- Nome
                3- Preço custo
                4- Preço venda
                5- Quantidade
                """)

                opcao = input(" ")

                if opcao not in mapa:
                    print("Escolha uma das opções disponiveis")
                    return

                atributo_escolhido = mapa[opcao]
                novo_valor = input("Digite o novo valor: ")         

                if atributo_escolhido in ["preco_custo", "preco_venda"]:
                    novo_valor = float(novo_valor)

                elif atributo_escolhido in ["codigo", "quantidade"]:
                    novo_valor = int(novo_valor)   

                if atributo_escolhido == "codigo":
                    codigo_antigo = produto.codigo
                    self.referencia_main.estoque.itens[novo_valor] = self.referencia_main.estoque.itens.pop(codigo_antigo)

                produto.editar_produto(atributo_escolhido, novo_valor)

                print("Produto alterado com sucesso!")
                
            else:
                print("Produto não encontrado, tente cadastrar")
                return

        elif escolha == 3:
            self.referencia_main.change_state(self.referencia_main)

        else:
            print("Escolha uma das opções disponiveis")