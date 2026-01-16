from datetime import datetime

class Recibo:
    def gerar_linhas(self, venda, valor_pago):
        linhas = []
        total = 0

        largura = 48
        horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        linhas.append("Adega do ze".center(largura))
        linhas.append("RUA JUAN VICENTE, 461 - OSASCO/SP".center(largura))
        linhas.append("CPF/CPNJ:00000000-0".center(largura))
        linhas.append("-" * largura)
        linhas.append(f"Data/Hora: {horario}")
        linhas.append("Produto" + " " * 10 + "Cod" + " " * 7 + "Quant" + " " * 5 + "Valor")
        linhas.append("-" * largura)

        for item, quantidade in venda:
            subtotal = item.preco_venda * quantidade
            total += subtotal
            linha = f"{item.nome:<18} {item.codigo:<10} {quantidade:<6} {f'R${subtotal:.2f}':>6}"
            linhas.append(linha)

        linhas.append("")
        linhas.append(f'{"Total":<{largura//2}}{f"R${total:.2f}":>{largura//2-4}}')
        linhas.append(f'{"Valor pago":<{largura//2}} {f"R${valor_pago:.2f}":>{largura//2-4}}')
        linhas.append(f'{"Troco":<{largura//2}} {f"R${valor_pago - total:.2f}":>{largura//2-4}}')
        linhas.append("Obrigado pela preferencia".center(largura))
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

    def imprimir(self, linhas: list):
        import win32print
        
        if not hasattr(self, "nome") or not self.nome:
            print("Nome da impressora não definido. Tentando usar impressora padrão")
            try:
                self.nome = win32print.GetDefaultPrinter()
            except Exception as e:
                self.nome = None
                raise RuntimeError("Impressora nao encontrada")

        self.handle = None

        try:
            self.handle = win32print.OpenPrinter(self.nome)
        except Exception as e:
            self.handle = None

        if not self.handle:
            raise RuntimeError("Impressora não disponível")

        try:
            win32print.StartDocPrinter(
                self.handle,
                1,
                ("Recibo", None, "RAW")
            )
            win32print.StartPagePrinter(self.handle)

            texto = "\n".join(linhas)
            texto += b"\n\n\n\n"
            texto+= b"\x1d\x56\x01"

            for linha in linhas:
                win32print.WritePrinter(
                    self.handle,
                    (texto).encode("utf-8")
                )

            win32print.EndPagePrinter(self.handle)
            win32print.EndDocPrinter(self.handle)

        finally:
            win32print.ClosePrinter(self.handle)
            self.handle = None
