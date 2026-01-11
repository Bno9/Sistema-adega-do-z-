class Recibo:
    def gerar_linhas(self, venda, valor_pago):
        linhas = []
        total = 0

        largura = 32

        linhas.append("Adega do zé".center(largura))
        linhas.append("CPNJ:00000000-0  TEL:11988334998")
        linhas.append("-" * 32)
        linhas.append("Produto     Cód     Qtd    Valor")
        linhas.append("-" * 32)

        for item, quantidade in venda:
            subtotal = item.preco_venda * quantidade
            total += subtotal
            linha = f"{item.nome:<10} {item.codigo:<8} {quantidade:<3} R${subtotal:>6.2f}"
            linhas.append(linha)

        linhas.append("")
        linhas.append(f"{'Total':<22} R${total:>6.2f}")
        linhas.append(f"Pago R${valor_pago:.2f}     {'Troco R$':>10}{valor_pago - total:.2f}")
        linhas.append("Obrigado pela prefêrencia".center(largura))
        linhas.append("")
        return linhas


class ImpressoraBase: #classe base para polimorfismo
    def imprimir(self, linhas: list[str]):
        raise NotImplementedError


class ImpressoraTxt(ImpressoraBase): #classe pra teste
    def imprimir(self, linhas):
        with open("recibo_teste.txt", "w", encoding="utf-8") as f:
            for linha in linhas:
                f.write(linha + "\n")

class ImpressoraWindows(ImpressoraBase): #classe para cliente
    def __init__(self, nome_impressora):
        self.nome = nome_impressora

    def imprimir(self, linhas):
        import win32print

        handle = win32print.OpenPrinter(self.nome)
        try:
            win32print.StartDocPrinter(handle, 1, ("Recibo", None, "RAW"))
            win32print.StartPagePrinter(handle)

            for linha in linhas:
                win32print.WritePrinter(handle, (linha + "\n").encode("utf-8"))

            win32print.EndPagePrinter(handle)
            win32print.EndDocPrinter(handle)
        finally:
            win32print.ClosePrinter(handle)