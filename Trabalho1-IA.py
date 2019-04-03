import sys
import csv

class Vertice:
    def __init__(self, nome):
        self.id = nome
        self.adjacentes = {}
        self.descoberto = 0
        self.terminado = 0
        self.cor = 'preto'

    def __str__(self):
        return '| Vizinhos: ' + str([x.id for x in self.adjacentes])

    def addVizinho(self, vizinho, distancia=0):
        self.adjacentes[vizinho] = distancia

    def getArestas(self):
        return self.adjacentes.keys()  

    def getVerticeId(self):
        return self.id

    def getDistancia(self, vizinho):
        return self.adjacentes[vizinho]

class Graph:

    def __init__(self):
        self.vertices = {}
        self.num_vertices = 0
        self.tempo = 0
        self.caminho = []

    def __iter__(self):
        return iter(self.vertices.values())

    def __str__(self):
        string = ''
        for key in sorted(list(self.vertices.keys())):
            string += ' %s' %(self.vertices[key]) + ' | Descoberto: ' + str(self.vertices[key].descoberto) + ' | Terminado: ' + str(self.vertices[key].terminado) + '|  Cor: ' +  str(self.vertices[key].cor) + '\n'
        return string


    def addVertice(self, v):
        self.num_vertices = self.num_vertices + 1
        novoVertice = Vertice(v)
        self.vertices[v] = novoVertice
        return novoVertice

    def getVertice(self, n):
        if n in self.vertices:
            return self.vertices[n]
        else:
            return None

    def addAresta(self, u, v, distancia = 0):
        if u not in self.vertices:
            self.addVertice(u)
        if v not in self.vertices:
            self.addVertice(v)

        self.vertices[u].addVizinho(self.vertices[v], distancia)
        self.vertices[v].addVizinho(self.vertices[u], distancia)

    def getVertices(self):
        return self.vertices.keys()

    def printarGrafo(self):
        for key in sorted(list(self.vertices.keys())):
            print('Cidade: '+key  +' %s' %(self.vertices[key]) )
    
    def buscaProfundidade(self,verticeInicial, verticeFinal, distancia):
        self.vertices[verticeInicial].cor = 'vermelho'
        self.vertices[verticeInicial].descoberto = self.tempo
        self.tempo += 1
        self.caminho.append(verticeInicial)
        for vizinho in self.vertices[verticeInicial].adjacentes:
            if self.vertices[vizinho.id].cor == 'preto' and vizinho.id != verticeFinal:
                distancia = distancia + vizinho.getDistancia(self.vertices[verticeInicial])
                self.buscaProfundidade(vizinho.id,verticeFinal, distancia)
            elif self.vertices[vizinho.id].cor == 'preto' and vizinho.id == verticeFinal:
                distancia = distancia + vizinho.getDistancia(self.vertices[verticeInicial])
                return (self.caminho, distancia)
            elif self.vertices[vizinho.id].cor == 'azul' and vizinho.id == verticeFinal:
                distancia = distancia + vizinho.getDistancia(self.vertices[verticeInicial])
                return (self.caminho, distancia)
            self.vertices[vizinho.id].cor = 'azul'
            self.vertices[vizinho.id].terminado = self.tempo
            self.vertices[vizinho.id].descoberto = 1
            self.tempo += 1  
        return (None, None)

       
    def buscaCustoUniforme(self,verticeInicio,verticeFinal,caminho, distanciaTotal):
        if verticeInicio and verticeFinal in self.vertices:
            self.vertices[verticeInicio].cor = 'vermelho'
            self.vertices[verticeInicio].descoberto = 1
            caminho.append(verticeInicio)
        if verticeInicio == verticeFinal:
            return caminho, distanciaTotal
        for vizinho in self.vertices[verticeInicio].adjacentes:
            distancias = self.vertices[verticeInicio].adjacentes.values()
            menorDistancia = min(distancias)
            if vizinho.getDistancia(self.vertices[verticeInicio]) == menorDistancia and self.vertices[vizinho.id].cor == 'preto':
                distanciaTotal += menorDistancia 
                self.buscaCustoUniforme(vizinho.id,verticeFinal,caminho,distanciaTotal)
            elif vizinho.getDistancia(self.vertices[verticeInicio]) != menorDistancia and self.vertices[vizinho.id].cor == 'preto':
                distanciaTotal += vizinho.getDistancia(self.vertices[verticeInicio]) 
                self.buscaCustoUniforme(vizinho.id,verticeFinal,caminho,distanciaTotal)
            elif vizinho.id == verticeFinal:
                return caminho, distanciaTotal
        self.vertices[vizinho.id].cor = 'azul'
        self.vertices[vizinho.id].descoberto = 1
        return None, None

   # def buscaAprofundamentoIterativo():
        

    def printGrafoComDados(self):
        print('\n')
        for key in sorted(list(self.vertices.keys())):
            print('Cidade: '+key  +' %s' %(self.vertices[key]) + ' | Descoberto: ' + str(self.vertices[key].descoberto) + '|  Cor: ' +  str(self.vertices[key].cor))

def main():
    menu()

def menu():
    grafo = Graph()
    grafo.addVertice('Arad')
    grafo.addVertice('Zerind')
    grafo.addVertice('Oradea')
    grafo.addVertice('Sibiu')
    grafo.addVertice('Rimnicu Vilcea')
    grafo.addVertice('Timisoara')
    grafo.addVertice('Mehadia')
    grafo.addVertice('Dobreta')
    grafo.addVertice('Craiova')
    grafo.addVertice('Pitesti')
    grafo.addVertice('Fagaras')
    grafo.addVertice('Giurgiu')
    grafo.addVertice('Bucharest')
    grafo.addVertice('Urziceni')
    grafo.addVertice('Eforie')
    grafo.addVertice('Hirsova')
    grafo.addVertice('Vaslui')
    grafo.addVertice('Iasi')
    grafo.addVertice('Neamt') 

    grafo.addAresta('Arad','Zerind',75)
    grafo.addAresta('Arad','Sibiu',140)
    grafo.addAresta('Arad','Timisoara',118)
    grafo.addAresta('Zerind','Oradea',71)
    grafo.addAresta('Sibiu','Oradea',151)
    grafo.addAresta('Sibiu','Fagaras',99)
    grafo.addAresta('Sibiu','Rimnicu Vilcea',80)
    grafo.addAresta('Pitesti','Rimnicu Vilcea',97)
    grafo.addAresta('Craiova','Rimnicu Vilcea',146)
    grafo.addAresta('Lugoj','Timisoara',111)
    grafo.addAresta('Lugoj','Mehadia',70)
    grafo.addAresta('Dobreta','Mehadia',75)
    grafo.addAresta('Dobreta','Craiova',120)
    grafo.addAresta('Pitesti','Craiova',138)
    grafo.addAresta('Pitesti','Bucharest',101)
    grafo.addAresta('Bucharest','Fagaras',211)
    grafo.addAresta('Giurgiu','Bucharest',90)
    grafo.addAresta('Urziceni','Bucharest',85)
    grafo.addAresta('Urziceni','Hirsova',98)
    grafo.addAresta('Urziceni','Vaslui',142)
    grafo.addAresta('Eforie','Hirsova',86)
    grafo.addAresta('Iasi','Vaslui',92)
    grafo.addAresta('Iasi','Neamt',87)

    print(' ------------------------------------')
    print(' --------------- MENU ---------------\n')
    print('1 - Busca em profundidade')
    print('2 - Busca de custo uniforme')
    print('3 - Busca em superficie')
    print('4 - Busca com aprofundamento iterativo')
    print('5 - Printar grafo')
    task = input('\nDeseja realizar alguma tarefa? ')
    if task == '1':
        verticeInicial = input("De que cidade gostaria de iniciar sua busca? ")
        verticeFinal = input("Em qual cidade gostaria de finalizar? ")
        d = 0
        caminho, distancia = grafo.buscaProfundidade(verticeInicial, verticeFinal,d)
        print('Caminho: ' + str(caminho), ' -     Distancia percorrida: ' + str(distancia))
        print('\n')
        continueMenu = input("Gostaria de realizar uma nova tarefa? \n    S/N:  ")
        if continueMenu == "S" or continueMenu == "s":
            print("\n")
            menu()
        elif continueMenu == "N" or continueMenu == "n":
            print('\n')
            print("Programa finalizado!")
           
    elif task == '2':
        caminho = []
        verticeInicial = input("De que cidade gostaria de iniciar sua busca? ")
        verticeFinal = input("Em qual cidade gostaria de finalizar? ")
        distanciaTotal = 0 
        caminho, distancia = grafo.buscaCustoUniforme(verticeInicial, verticeFinal,caminho, distanciaTotal)
        print('\nMenor caminho encontrado -> '+ str(caminho) + '    Distancia percorrida: ' + str(distancia))
        print('\n')
        continueMenu = input("Gostaria de realizar uma nova tarefa? \n    S/N:  ")
        if continueMenu == "S" or continueMenu == "s":
            print("\n")
            menu()
        elif continueMenu == "N" or continueMenu == "n":
            print("Programa finalizado!")

    elif task == '3':
        print('Não implementado ainda')
        continueMenu = input("Gostaria de realizar uma nova busca? \n    S/N:  ")
        if continueMenu == "S" or continueMenu == "s":
            print("\n")
            menu()
        elif continueMenu == "N" or continueMenu == "n":
            print('\n')
            print("Programa finalizado!")
    
    elif task == '4':
        print('Não implementado ainda')
        continueMenu = input("Gostaria de realizar uma nova busca? \n    S/N:  ")
        if continueMenu == "S" or continueMenu == "s":
            print("\n")
            menu()
        elif continueMenu == "N" or continueMenu == "n":
            print('\n')
            print("Programa finalizado!")

    elif task == '5':
        grafo.printarGrafo()
        print('\n')
        continueMenu = input("Gostaria de realizar uma nova busca? \n    S/N:  ")
        if continueMenu == "S" or continueMenu == "s":
            print("\n")
            menu()
        elif continueMenu == "N" or continueMenu == "n":
            print('\n')
            print("Programa finalizado!")

    else:
        print('Digite novamente.')
        menu() 

main()
   