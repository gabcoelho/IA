class NRainhas:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.colunas = []
 
    def inserirNaProxColuna(self, coluna):
        self.colunas.append(coluna)
 
    def removerDaColunaAtual(self):
        return self.colunas.pop()
 
    def verificaProximaColuna(self, coluna):
        linha = len(self.colunas)
        # verifica coluna
        for rainha in self.colunas:
            if coluna == rainha:
                return False
        # verifica diagonal
        for linhaDaRainha, colunaDaRainha in enumerate(self.colunas):
            if colunaDaRainha - linhaDaRainha == coluna - linha:
                return False
 
        # verifica outra diagonal
        for linhaDaRainha, colunaDaRainha in enumerate(self.colunas):
            if ((self.tamanho - colunaDaRainha) - linhaDaRainha == (self.tamanho - coluna) - linha):
                return False
        return True
 
    def printarTabuleiro(self):
        print("\n  Solução -> " + str(self.colunas) + "\n\n")
 
def solucaoComBuscaGulosa(tamanho):
    tabuleiro = NRainhas(tamanho)
    linha = 0
    coluna = 0
    solucaoEncontrada = False
    while True:
        # inserir rainha na prox linha
        while coluna < tamanho:
            if tabuleiro.verificaProximaColuna(coluna):
                tabuleiro.inserirNaProxColuna(coluna)
                linha += 1
                coluna = 0
                break
            else:
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