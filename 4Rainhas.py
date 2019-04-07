# Heuristica = quantRainhas em conflito - 1

class NRainhas:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.colunas = []
 
    def inserirNaProxColuna(self, coluna):
        self.colunas.append(coluna)
 
    def removerDaColunaAtual(self):
        return self.colunas.pop()
 
    def verificaProximaColuna(self, coluna, cont):
        linha = len(self.colunas)
        # verifica coluna
        for rainha in self.colunas:
            if coluna == rainha:
                cont += 1
                return cont, False

        # verifica diagonal
        for linhaDaRainha, colunaDaRainha in enumerate(self.colunas):
            if colunaDaRainha - linhaDaRainha == coluna - linha:
                cont += 1
                return cont, False
 
        # verifica outra diagonal
        for linhaDaRainha, colunaDaRainha in enumerate(self.colunas):
            if ((self.tamanho - colunaDaRainha) - linhaDaRainha == (self.tamanho - coluna) - linha):
                cont += 1
                return cont, False
        return cont, True
 
    def printarTabuleiro(self):
        print("\n  Solução -> " + str(self.colunas) + "\n\n")
 
def solucaoComBuscaGulosa(tamanho):
    tabuleiro = NRainhas(tamanho)
    linha = 0
    coluna = 0
    cont = 0
    solucaoEncontrada = False
    while True:
        # inserir rainha na prox linha
        while coluna < tamanho:
            heuristica, verificador = tabuleiro.verificaProximaColuna(coluna, cont)
            if verificador and heuristica == 0:
                tabuleiro.inserirNaProxColuna(coluna)
                linha += 1
                coluna = 0
                break
            else:
                heuristica += 1
                coluna += 1
 
        # se não temos uma coluna para inserir, ou se o tabuleiro está cheio
        if (coluna == tamanho or linha == tamanho):
            # se o tabuleiro está cheio, então temos uma solução
            if linha == tamanho:
                tabuleiro.printarTabuleiro()
                tabuleiro.removerDaColunaAtual()
                linha -= 1
                solucaoEncontrada = True
            try:
                if solucaoEncontrada:
                    break
                else:
                    colunaAnterior = tabuleiro.removerDaColunaAtual()
            except IndexError: #error handler - Index de vetor invalido
                break
            # tentar linha anterior e coluna novamente
            linha -= 1
            coluna = 1 + colunaAnterior

  
 
n = int(input('Tamanho do tabuleiro (n): '))
solucaoComBuscaGulosa(n)