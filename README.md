# Manual Sistema Adega do Zé

## Objetivo

O Sistema Adega do Zé tem como objetivo controlar o fluxo de estoque e vendas, melhorando a qualidade do trabalho e reduzindo o tempo gasto em operações manuais.

O sistema resolve diversos problemas do dia a dia, como:
	-	Controle eficiente de estoque e pedidos
	-	Baixa automática de produtos vendidos
	-	Avisos de produtos com baixo estoque
	-	Gestão de despesas e caixa
	-	Geração de relatórios para análise (em desenvolvimento)

⸻

# Funcionalidades do Sistema

## Menu Principal

Tela inicial do programa.

Ao iniciar o sistema, é solicitada uma senha de acesso para abertura do programa. Atualmente, a senha é padrão, porém o sistema foi projetado para permitir:
	-	Alteração da senha (funcionalidade em desenvolvimento)
	-	Cadastro de usuários (atualização futura)
	-	Senha individual por usuário (atualização futura)

A tela principal conta com:
	-	Botões para navegação entre as telas
	-	Uma barra superior com opções de configuração, acesso ao manual, cadastro de usuários e alteração de senhas

Atalhos disponíveis:
	-	1 – Tela de Caixa
	-	2 – Tela de Estoque
	-	3 – Tela de Cadastro
	-	4 – Tela de Despesas
	-	5 – Tela de Relatórios
	-	Esc – Fechar o programa

⸻

## Menu de Cadastro de Produtos

Responsável pelo cadastro, edição e exclusão de produtos no sistema.

### Cadastro de Produto

Ao informar um código de barras inexistente no banco de dados, o sistema permite cadastrar um novo produto com os seguintes dados:
	-	Código de barras
	-	Nome
	-	Preço de custo
	-	Preço de venda
	-	Quantidade
	-	Tipo
	-	Produto pai ou quantidade por fardo (dependendo do tipo escolhido) (produto pai é s referência para baixa automática, utilizada no módulo de Caixa)

### Edição de Produto

Ao digitar o código de um produto já existente:
	-	Os dados são automaticamente carregados do estoque para a tela
	-	O usuário pode alterar apenas os campos desejados e salvar as mudanças

### Alteração de Código

Existe um menu específico para alteração do código de um produto.

### Exclusão de Produto

Ao digitar o código de um produto existente:
	-	O usuário pode selecionar a opção de excluir
	-	Uma confirmação é solicitada antes da exclusão definitiva

### Tabela de Produtos

O menu conta com uma tabela que exibe todos os produtos cadastrados no estoque. A tabela permite:
	-	Selecionar um produto e pressionar Enter para editar ou excluir
	-	Pesquisa por nome
	-	Exclusão direta pressionando Delete

A tabela é atualizada automaticamente após qualquer alteração.

Atalhos disponíveis:
	-	F1 – Salvar alterações
	-	F2 – Alterar código do produto
	-	Delete – Excluir produto
	-	Esc – Voltar

⸻

## Menu de Estoque

Exibe uma tabela com todos os produtos cadastrados, contendo:
	-	Código
	-	Nome
	-	Quantidade
    -   Preço de custo
	-	Preço de venda
	-	Margem de lucro

Funcionalidades adicionais:
	-	Filtro por nome ou código
	-	Ordenação clicando no topo das colunas codigo/nome (A–Z ou Z–A)

⸻

## Menu de Caixa

Responsável pelo registro de vendas.

O caixa possui uma tabela onde os itens são registrados informando:
	-	Código do produto
    -   Nome do produto
	-	Quantidade (por padrão, 1)
    -   Preço de venda

O sistema:
	-	Calcula automaticamente o valor total da compra
	-	Exibe o total de itens
	-	Realiza a baixa automática no estoque após finalização da compra

### Finalização da Compra

Ao finalizar a compra:
	1.	Abre uma tela para informar o valor pago
	2.	Exibe o valor do troco
	3.	Após confirmação, abre a tela de impressão do recibo

Na tela de impressão é possível:
	-	Informar CPF para envio ao SAT (em desenvolvimento)
	-	Imprimir cupom simples sem CPF
	-	Não imprimir cupom

Baixa Automática com Produto Pai:

Ao final da compra, o sistema verifica:
	-	Se o produto filho chegou a quantidade zero
	-	Se o produto pai possui estoque disponível

Caso ambas as condições sejam atendidas:
	-	O sistema adiciona automaticamente a quantidade do fardo ao produto filho
	-	Diminui 1 unidade do produto pai

Funcionalidades adicionais do Caixa
	-	Aplicação de desconto
	-	Consulta de produtos
	-	Reimpressão de cupons (em desenvolvimento)
	-	Registro de duas vendas simultâneas (em desenvolvimento)
	-	Exclusão de itens da venda

Atalhos disponíveis:
	-	F1 – Finalizar compra
	-	F2 - Pesquisar produto
	-	F5 – Aplicar desconto
	-	F7 – Próxima venda / voltar para venda anterior
	-	F10 – Consultar produto
	-	F12 – Reimprimir cupom
	-	Delete – Excluir item da venda
	-	Esc – Voltar

⸻

## Menu de Despesas

Responsável pela gestão de despesas do sistema.

### Adicionar Despesa

Permite adicionar despesas informando:
	-	Nome
	-	Valor
	-	Data (opcional)
	-	Observação (opcional)

Caso nenhuma data seja informada, o sistema utiliza automaticamente a data do dia.

Após o cadastro, o nome da despesa passa a ser utilizado como referência para filtros por categoria.

### Editar Despesa

Selecionando uma despesa na tabela e optando por editar:
	-	É possível editar todos os seus dados

### Excluir Despesa

Ao selecionar uma despesa e optar pela exclusão:
	-	Uma janela de confirmação é exibida antes da exclusão definitiva

### Tabela

-	Exibe o valor total das despesas
-	Permite filtrar por categorias/nomes
-	Atualiza automaticamente o total com base no filtro aplicado

Atalhos disponíveis:
	-	F1 – Adicionar despesa
	-	F2 – Editar despesa
	-	Delete – Excluir despesa
	-	Esc – Voltar

⸻

## Menu de Relatórios (em desenvolvimento)

Permite visualizar relatórios do sistema.

O usuário pode escolher entre:
	-	Relatórios de Caixa
	-	Relatórios de Estoque

Relatório de Caixa
	-	Permite selecionar um dia específico
	-	Exibe todas as compras registradas no caixa naquele dia
    -	Exibe abertura de caixa e saldo final 


Relatório de Estoque
	-	Permite selecionar um dia específico
	-	Exibe todos os registros, alterações e baixas de estoque daquele dia

⸻

## Banco de Dados e Backup

O sistema utiliza banco de dados para garantir a permanência das informações.

Além disso, conta com:
	-	Backup automático diário (em desenvolvimento)
	-	Exclusão automática de backups com mais de uma semana, evitando acúmulo desnecessário de arquivos
