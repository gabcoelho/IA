#!/usr/bin/python3

import random
import csv
import numpy as np
import sklearn
from sklearn import tree

SIMBOLOS = ['♠', '♢', '♡', '♣']
NAIPE = ['Espadas', 'Ouro', 'Copas', 'Paus']
RANK = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'D', 'J', 'Q', 'K']
RANK_VALUE = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'D': 10, 'J': 11, 'Q': 12, 'K': 13}
NAIPE_SIMBOLOS = {'Copas': '♡', 'Paus': '♣', 'Espadas': '♠', 'Ouro': '♢'}

''' Classe modelo para uma unica carta'''
class Carta:
	def __init__(self, rank, naipe):
		self.rank = rank
		self.naipe = naipe
		self.coringa = False

	def __str__(self):
		if self.coringa:
			return (self.rank + NAIPE_SIMBOLOS[self.naipe] + '-J')
		return (self.rank + NAIPE_SIMBOLOS[self.naipe])

	def isCoringa(self):
		return self.coringa

class Baralho:
	def __init__(self, tamanho):
		self.tamanho = tamanho
		self.cartas = []
		self.coringa = None

		# Create all cards in the Deck
		for i in range(tamanho):
			for s in NAIPE:
				for r in RANK:
					self.cartas.append(Carta(r, s))

	def embaralharBaralhoRandom(self):
		random.shuffle(self.cartas)

	def retirarCartaDoBaralho(self):
		carta = self.cartas[0]
		self.cartas.pop(0)
		return carta

	def colocarCoringaNoBaralho(self):
		self.coringa = random.choice(self.cartas)
		self.cartas.remove(self.coringa)
		for carta in self.cartas:
			if self.coringa.rank == carta.rank:
				carta.coringa = True

class Player:
	def __init__(self, nome, baralho, game):
		self.cartas = []	# Cartas do Jogador.
		self.nome = nome
		self.baralho = baralho
		self.game = game

	def pegarCarta(self, carta):
		try:
			self.cartas.append(carta)
			if len(self.cartas) > 10:
				raise ValueError('ERRO! Você não pode ter mais de 10 cartas na mão.')
		except ValueError as err:
			print(err.args)

	def descartarCarta(self, carta):
		carta = get_object(self.cartas, carta)
		if carta not in self.cartas:
			return False

		self.cartas.remove(carta)
		self.game.addDescarte(carta)

		return True

	def exitGame(self):
		return True

	def close_game(self):
		conjuntoDeCartas = [self.cartas[:3], self.cartas[3:6], self.cartas[6:9]] #divide cartas em três conjuntinhos
		count = 0

		for s in conjuntoDeCartas:
			if verificaSeguenciaNaipeIgual(s):
				count += 1
				
		if count == 0:
			return False

		for s in conjuntoDeCartas:
			if verificaSeguenciaNaipeIgual(s) == False and verificaSequenciaRANKIgual(s) == False and verificaSequenciaNaipeIgualComJokers(s) == False:
				return False
		return True

	def play(self):
		listaCartas = []
		cartasNormais = self.cartas[:]
		arq = open("dados.csv", "a")

		for i in cartasNormais:
			#valorCarta = i.rank
			if i.naipe == "Copas":
				naipeCarta = 0
			elif i.naipe == "Paus":
				naipeCarta = 1
			elif i.naipe == "Espadas": 
				naipeCarta = 2
			elif i.naipe == "Ouro": 
				naipeCarta = 3	
			valorCarta = RANK_VALUE[i.rank]
			listaCartas.append(valorCarta)
			listaCartas.append(naipeCarta)
		if self.game.descarte[0].naipe == "Copas":
			naipeCartaDescarte = 0
		elif self.game.descarte[0].naipe == "Paus":
			naipeCartaDescarte = 1
		elif self.game.descarte[0].naipe == "Espadas": 
			naipeCartaDescarte = 2
		elif self.game.descarte[0].naipe == "Ouro": 
			naipeCartaDescarte = 3	
		valorCartaDescarte = RANK_VALUE[i.rank]
		listaCartas.append(valorCartaDescarte)
		listaCartas.append(naipeCartaDescarte)
		#c.writerow(listaCartas)

		while True:
			print("\n\n")
			print("***",self.nome,"Suas cartas são:")
			print(printCartas(self.cartas))
			self.game.mostrarCartaDescartada()

			action = input("*** " + self.nome + ", o que gostaria de fazer a seguir? ***, \n(M)over Carta, (P)egar carta do descarte, (B)Pegar carta do baralho, (D)escartar carta, (O)rganizar, (F)inalizar Jogo, (R)egras:, (E)xit ")

			# Mover cartas da mao
			if action == 'M' or action == 'm':
				move_what = input("Selecione a carta que gostaria de mover. \nEntre ela com o seu valor seguido da primeira letra do naipe. Exemplo -> 4C (4 de Copas): ")
				move_what.strip()
				if get_object(self.cartas, move_what.upper()) not in self.cartas:
					input("ERRO! Você não possui essa carta. Presione enter para continuar.")
					continue

				# Pega local da carta para onde gostaria de mover
				move_where = input("Entre com o local para onde gostaria de mover a carta. Entre espaço para mover para o final \nColoque o rank da carta seguido de seu naipe.. Exemplo 4H (4 of Copas):" )
				move_where.strip()
				if move_where != "" and get_object(self.cartas, move_where.upper()) not in self.cartas:
					input("ERRO! Localização de inserção inválida. Pressione enter para continuar")
					continue

				move_what = get_object(self.cartas, move_what.upper())
				if move_where != "":
					move_where = get_object(self.cartas, move_where.upper())
					location = self.cartas.index(move_where)
					if location > self.cartas.index(move_what):
						location = location - 1
					self.cartas.remove(move_what)
					self.cartas.insert(location, move_what)
				else:
					self.cartas.remove(move_what)
					self.cartas.append(move_what)

			# Pegar carta descarte
			if action == 'P' or action == 'p':
				if len(self.cartas) < 10:
					c = self.game.pegarDescarte()
					self.cartas.append(c)
					listaCartas.append(0)
					with arq: 
						writer = csv.writer(arq)
						writer.writerow(listaCartas)
				else:
					input("ERRO! Você possui " + str(len(self.cartas)) + " cartas. Não é possível ficar com mais. Pressione enter para continuar")
		
			# Pegar carta baralho
			if action == 'B' or action == 'b':
				if len(self.cartas) < 10:
					c = self.baralho.retirarCartaDoBaralho()
					self.cartas.append(c)
					listaCartas.append(1)
					with arq: 
						writer = csv.writer(arq)
						writer.writerow(listaCartas)
				else:
					input("ERRO! Você possui " + str(len(self.cartas)) + " cartas. Não é possível ficar com mais. Pressione enter para continuar")

			# Descartar carta baralho
			if action == 'D' or action == 'd':
				if len(self.cartas) == 10:
					drop = input("Que carta gostaria de descartar? \nEntre ela com o seu valor seguido da primeira letra do naipe. Exemplo -> 4C (4 de Copas): ")
					drop = drop.strip()
					drop = drop.upper()
					if self.descartarCarta(drop):
						return False
					else:
						input("ERRO! Carta inválida, pressione enter para continuar")
				else:
					input("ERRO! Você não pode descartar essa carta. Um jogador deve ter pelo menos 13 cartas, pressione enter para continuar")

			# Organizar cartas do jogador
			if action == 'O' or action == 'o':
				organizarCartasRANK(self.cartas)

			# Finalizar jogo
			if action == 'F' or action == 'f':
				if len(self.cartas) == 9:
					if self.close_game():
						print(printCartas(self.cartas))
						# Return True because Close ends the Game.
						return True
					else:
						input("ERRO! Jogo ainda não acabou, pressione enter para continuar. ")
						self.cartas.append(self.game.pegarDescarte())
				else:
					input("ERRO! Você não tem cartas o suficiente para fechar o jogo. selecione enter para continuar.")

			# Regras do jogo
			if action == 'R' or action == 'r':
				print("------------------ Regras --------------------",
					"\n- Cacheta é um jogo que se consiste em fazer conjuntos.",
					"\n- Cada jogador terá 9 cartas na mão, e 3 conjuntos deverão ser criados. (3 de 3 cartas e 1 de 4 cartas).",
					"\n- O conjunto de 3 cartas sempre deverá ser o ultimo a ser montado."
					"\n- Pelo menos um conjunto tem que ser criado sem o coringa."
					"\n- Podemos ter sequência de mesmo naipe. Ex: 4 de copas, 5 de copas e 6 de copas.",
					"\n- E também sequencias de cartas com o mesmo Rank. Ex: 3 de Espadas, 3 de Copas e 3 de Ouro",
					"\n- Um coringa é denotado por '-J' e pode ser usado para completar uma sequência.",
					"\n- A cada rodada um jogador deve pegar uma carta, ou do baralho ou do descarte. Imediatamente, ele também deverá descartar uma carta.",
					"\n- Quando completado todas os conjuntos, selecione F para finalizar o jogo.",
					"\n- Uma carta com rank 10 é representada como D"
					"\n--------------------------------------------" )
				input("Selecione enter para continuar ....")

			if action == 'E'or action == 'e':
				self.exitGame()

class Game:
	def __init__(self, hands, deck):
		self.descarte = []
		self.players = []

		for i in range(hands):
			nome = input("Entre com o seu nome " + str(i) + ": ")
			self.players.append(Player(nome, deck, self))

	def mostrarCartaDescartada(self):
		if len(self.descarte) == 0:
			print("Baralho de descarte vazio.")
		else:
			print("A carta no topo do descarte é: ", self.descarte[0])

	def addDescarte(self, carta):
		self.descarte.insert(0, carta)

	def pegarDescarte(self):
		if len(self.descarte) != 0:
			return self.descarte.pop(0)
		else:
			return None

	def play(self):
		i = 0
		while self.players[i].play() == False:
			print(chr(27)+"[2J")
			i += 1
			if i == len(self.players):
				i = 0
			print("***", self.players[i].nome, "vai jogar agora.")
			input(self.players[i].nome + " pressione enter para continuar...")

		# Game Over
		print("*** GAME OVER ***")
		print("*** ", self.players[i].nome, " GANHOU ***")


#global nonclass functions
def treinarArvoreDecisao():
	with open("/Users/gabriela.coelho/Desktop/Cacheta/dados.csv",'r') as csvfile: 
		leitorCartas = csv.reader(csvfile,delimiter=',',quotechar='"')
    
		#row agora contem os nomes dos atributos
		row = leitorCartas
		nomeAtributos = np.array(row)
		
		#Carrega o conjunto de treino e as classes
		leitorCartasX,leitorCartasY = [],[]
		for row in leitorCartas:
			leitorCartasX.append(row[:-1])
			leitorCartasY.append(row[-1])#A classe é "survived"
			
		leitorCartasX = np.array(leitorCartasX[1:])
		leitorCartasY = np.array(leitorCartasY[1:])
		
	clf = tree.DecisionTreeClassifier(criterion='entropy',max_depth=12,min_samples_leaf=2)
	clf = clf.fit(leitorCartasX,leitorCartasY)
	print(makeAcuracy(clf, leitorCartasX, leitorCartasY))
	return clf

def makeAcuracy(tree,x_test,y_test):
    predictions = tree.predict(x_test)
    erro = 0.0
    for x in range(len(predictions)):
        if predictions[x] != y_test[x]:
            erro += 1.
    acuracy = (1-(erro/len(predictions)))
    return acuracy

def predictAction(tree, x):
	print(tree.predict(np.array(x).reshape(-1,20)))

def verificaSequenciaRANKIgual(sequence):
	# movimenta Coringas para final
	while(sequence[0].coringa == True):
		sequence.append(sequence.pop(0))
	# compara cartas umas com as outras
	for carta in sequence:
		if carta.isCoringa() == True:
			continue
		if carta.rank != sequence[0].rank:
			return False

	return True

def verificaSeguenciaNaipeIgual(sequence):
	RANK_VALUE["A"] = 1 # resetando valor

	organizarCartasRANK(sequence)
	# Checar se as cartas possuem o mesmo naipe
	for carta in sequence:
		if carta.naipe != sequence[0].naipe:
			return False
	# organiza sequencia que possui K Q ou A 
	if sequence[0].rank == "A":
		if sequence[1].rank == "Q" or sequence[1].rank == "J" or sequence[1].rank == "K":
			RANK_VALUE[sequence[0].rank] = 10
			organizarCartasRANK(sequence)

	# comparar valor RANK 
	for i in range(1,len(sequence)):
		if RANK_VALUE[sequence[i].rank] != RANK_VALUE[(sequence[i-1].rank)]+1:
			return False
	return True

def verificaSequenciaNaipeIgualComJokers(sequence):
	RANK_VALUE["A"] = 1 

	# Ordena cartas em sequencia
	organizarCartasRANK(sequence)

	colocarJokerNoFinal(sequence)
	joker_count = 0
	for carta in sequence:
		if carta.isCoringa() == True:
			joker_count += 1

	# Verifica se naipe é igual memsmo
	for carta in sequence:
		if carta.isCoringa() == True:
			continue
		if carta.naipe != sequence[0].naipe:
			return False

	# Para verificar reis, rainhas e etc. 
	if sequence[0].rank == "A":
		if sequence[1].rank == "Q" or sequence[1].rank == "J" or sequence[1].rank == "K":
			RANK_VALUE[sequence[0].rank] = 10
			organizarCartasRANK(sequence)
			colocarJokerNoFinal(sequence)

	rank_inc = 1
	for i in range(1,len(sequence)):
		if sequence[i].isCoringa() == True:
			continue

		while (RANK_VALUE[sequence[i].rank] != RANK_VALUE[(sequence[i-1].rank)]+rank_inc):
			if joker_count > 0:
				rank_inc += 1
				joker_count -= 1
				continue
			else:
				if RANK_VALUE[sequence[i].rank] != RANK_VALUE[(sequence[i-1].rank)]+1:
					return False
				else:
					break
	return True

def colocarJokerNoFinal(sequence):
	organizarCartasRANK(sequence)
	joker_list = []
	for carta in sequence:
		if carta.isCoringa()== True:
			sequence.remove(carta)
			joker_list.append(carta)
	sequence += joker_list
	return sequence

def get_object(arr, str_card):
	if len(str_card) != 2:
		return None

	for item in arr:
		if item.rank == str_card[0] and item.naipe[0] == str_card[1]:
			return item

	return None

def printCartas(arr):
	s = ""
	for carta in arr:
		s = s + " " + str(carta)
	return s

def organizarCartasRANK(sequencia):
	organizado = False

	while organizado == False:
		organizado = True
		for i in range(0, len(sequencia)-1):
			if RANK_VALUE[sequencia[i].rank] > RANK_VALUE[sequencia[i+1].rank]:
				a = sequencia[i+1]
				sequencia[i+1] = sequencia[i]
				sequencia[i] = a
				organizado = False
	return sequencia

def main():
	""" Main Program """
	baralho = Baralho(1)
	baralho.embaralharBaralhoRandom()
	action = input("Gostaria de jogar contra outra (p)essoa ou contra o (b)ot: ")
	if action == 'p' or action == 'P':
		g = Game(2, baralho)
		for i in range(9):
			for hand in g.players:
				carta = baralho.retirarCartaDoBaralho()
				hand.pegarCarta(carta)

		first_card = baralho.retirarCartaDoBaralho()
		g.addDescarte(first_card)
		g.play()

	if action == 'B' or action == 'b':
		arvore = treinarArvoreDecisao()
		while True:
			listaEntrada = []
			for i in range(20): 
				entrada = input("Escreva o proximo valor: ")
				listaEntrada.append(int(entrada))
			predictAction(arvore, listaEntrada)

if __name__ == "__main__":
    main()





