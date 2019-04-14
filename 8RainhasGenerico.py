import random
import string

#  5 tabuleiros iniciais
# escolher ponto fixo
# selecionar melhor mutacao do anterior para o prox
# mutacao 1/10

# gerar 5 tabuleiros aleatorios
# ver fitness de cada um de acordo com seus conflitos
# fazer crossover com um ponto fixo 
# gerar nova geracao com os melhores


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
        print("\n  Solucao -> " + str(self.colunas) + "\n\n")
 
    # calculo do fitness de acordo com colisoes
    def fitness(self,individuo):
        colizaoHorizontal = sum([individuo.count(rainha)-1 for rainha in individuo])/2
        colizoesDiagonais = 0

        n = len(individuo)
        diagonalEsquerda = [0] * 2*n
        diagonalDireita = [0] * 2*n
        for i in range(n):
            diagonalEsquerda[i + individuo[i] - 1] += 1
            diagonalDireita[len(individuo) - i + individuo[i] - 2] += 1

        colizoesDiagonais = 0
        for i in range(2*n-1):
            counter = 0
            if diagonalEsquerda[i] > 1:
                counter += diagonalEsquerda[i]-1
            if diagonalDireita[i] > 1:
                counter += diagonalDireita[i]-1
            colizoesDiagonais += counter / (n-abs(i-n+1))
        
        return int(28 - (colizaoHorizontal + colizoesDiagonais))


    def probabilidade(self, individuo, fitness):
        return fitness(individuo) / 28

    def escolherRandom(self, populacao, probabilidades):
        populacaoComProbabilidade = zip(populacao, probabilidades)
        total = sum(w for c, w in populacaoComProbabilidade)
        r = random.uniform(0, total)
        upto = 0
        for c, w in zip(populacao, probabilidades):
            if upto + w >= r:
                return c
            upto += w
        assert False
            
    def crossover(self, x, y):
        n = len(x)
        c = 4 # ponto fixo crossover
        #c = random.randint(0, n - 1)
        return x[0:c] + y[c:n]

    def realizarMutacao(self, x):
        n = len(x)
        c = random.randint(0, n - 1)
        m = random.randint(1, n)
        x[c] = m
        return x

    def solucaoAlgoritmoGenetico(self, populacao, fitness):
        probabilidadeDeMutacao = 0.1 # mutacao 1/10
        novaPopulacao = []
        probabilidades = [self.probabilidade(n, fitness) for n in populacao]
        for _ in range(len(populacao)):
            x = self.escolherRandom(populacao, probabilidades)
            y = self.escolherRandom(populacao, probabilidades)
            filho = self.crossover(x, y)
            if random.random() < probabilidadeDeMutacao:
                filho = self.realizarMutacao(filho)
            self.printIndividuo(filho)
            novaPopulacao.append(filho)
            if fitness(filho) == 28: break
        return novaPopulacao

    def printIndividuo(self, x):
        print("{},  fitness = {}, probabilidade = {:.6f}".format(str(x), self.fitness(x), self.probabilidade(x, self.fitness)))
    
    def randomizarIndividuos(self, tamanho):
        return [random.randint(1, 8) for _ in range(8)]

    def main(self):
        populacao = [self.randomizarIndividuos(8) for _ in range(5)]
        geracao = 1

        while not 28 in [self.fitness(x) for x in populacao]:
            print("=== Geracao {} ===".format(geracao))
            populacao = self.solucaoAlgoritmoGenetico(populacao, self.fitness)
            print("Fitness = {}".format(max([self.fitness(n) for n in populacao])))
            geracao += 1

        print("Resolvido na geracao {}!".format(geracao-1))
        for x in populacao:
            if self.fitness(x) == 28:
                self.printIndividuo(x)

if __name__ == '__main__':
    NRainhas(8).main()