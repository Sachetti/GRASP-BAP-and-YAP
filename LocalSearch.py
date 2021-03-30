import random
import sys
import math
import time
n = 2
num_section = 2
cargo = {1:"ferro", 2:"bauxita", 3:"cobre", 4:"prata"}
#print cargo[3]

# time = [0,0,0,0,0,0,0]
num_time = 1000
section = [0,0]

alpha = 3
alphaV = 20

alphaN = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
pAlphaN = [[0,9],[10,19],[20,29],[30,39],[40,49],[50,59],[60,69],[70,79],[80,89],[90,99]]
B = 100
tal = 10

# sorteado = random.randrange(100)
# print (sorteado)

#min mi - Ai + ci
# Input parameters
# Ai = expected arrival time of vessel i 

# Decision variabels
# mi = starting time of handling of vessel i
# ci = total handliing time of vessel i

#class Vessel that has the cargo type, the length from the vessel to 
#allocate in sections and the days is the handling time  

T = 0.1 #tempo necessário pra um crane carrgar/descarregar uma quantidade de carga, 0.1h
cranes = 3 #numero de cranes por vessel por seção
alfa = T/cranes


class Section:
	def __init__(self, name, distance, time, x, y):
		self.n = name
		self.d = distance
		self.t = time
		self.x = x
		self.y = y
	def get_distance(self):
		return self.d 
	def printing(self):
		print("Seção "+self.n)

class Cargo:
	def __init__(self, name, rate):
		self.n = name
		self.r = rate
	def get_rate(self):
		return self.r
	def printing(self):
		print("Carga "+self.n)

class Vessel:
	def __init__(self, name, cargo_type, lenght, arrival):
		self.n = name		
		self.c_t = cargo_type
		self.l = lenght
		self.a = arrival
	def printing(self):
		print ("Vessel "+self.n)
		#print (self.c_t, self.l, self.d)

#class Yard has the cargo type, the distance from the location to the
#berth and the capacity from the yard
class Yard:
	def __init__(self,name, cargo_type, distance, capacity, x, y, ativo, time):
		self.n = name		
		self.c_t = cargo_type
		self.d = distance
		self.c = capacity
		self.x = x
		self.y = y
		self.ativo = ativo
		self.time = time
	def printing(self):
		print ("location "+self.n)
		self.c_t.printing()
		print (self.d, self.c)
	def dist(self, berco):
		return distancia(berco, self)

#class Column has the vessel
class Column:
	def __init__(self, vessel, section, yard, beta, time):
		self.s = section
		self.y = yard
		self.beta = beta
		self.alfa = alfa
		self.h_t = alfa + beta #handling time = tempo de load/unload da carga + tempo de transferencia da carga
		self.v = vessel
		self.s_t = time #starting time
		self.c_t = ""
	def printing(self):
		self.v.printing()
		self.s.printing()
		self.y.printing()
		print ("Starting Time: ",self.s_t, "Handling Time: ", self.h_t, "\n\n")
	def belongs (self, vessel):
		return vessel == self.v

def distance_cargo_section(cargo, yards, section):
	d = 0
	t = 0
	for c in yards:
		if c.c_t == cargo:
			d += c.d
			t += 1
	
	d += section.d/t
	 
	return d


#creating the sections
# section1 = Section("1", 10, 1, 1, 1)
# section2 = Section("2", 10, 1, 5, 1)
# # section3 = Section("3", 30, 1, 11, 1)
# sections = [section1, section2]

#15 berços
# section1 = Section("1", 10, 1,1,1)
# section2 = Section("2", 10, 1,2,1)
# section3 = Section("3", 30, 1,4,1)
# section4 = Section("4", 30, 1,6,1)
# section5 = Section("5", 45, 1,9,1)
# section6 = Section("6", 45, 1,12,1)
# section7 = Section("7", 15, 1,15,1)
# section8 = Section("8", 15, 1,19,1)
# section9 = Section("9", 25, 1,22,1)
# section10 = Section("10", 25, 1,25,1)
# section11 = Section("11", 45, 1,28,1)
# section12 = Section("12", 15, 1,30,1)
# section13 = Section("13", 30, 1,32,1)
# section14 = Section("14", 10, 1,34,1)
# section15 = Section("15", 20, 1,35,1)
# sections = [section1,section2,section3,section4,section5,section6,section7,section8,section9,section10,section11,section12,section13,section14,section15]

#10 berços
section1 = Section("1", 10, 1,1,1)
section2 = Section("2", 10, 1,2,1)
section3 = Section("3", 30, 1,4,1)
section4 = Section("4", 30, 1,6,1)
section5 = Section("5", 45, 1,9,1)
section6 = Section("6", 45, 1,12,1)
section7 = Section("7", 15, 1,15,1)
section8 = Section("8", 15, 1,19,1)
section9 = Section("9", 25, 1,22,1)
section10 = Section("10", 25, 1,25,1)
sections = [section1,section2,section3,section4,section5,section6,section7,section8,section9,section10]


#creating the type of cargos
cargo1 = Cargo("cobre", 0.7)
cargo2 = Cargo("ferro", 0.8)
cargo3 = Cargo("bauxita", 0.9)
cargos = [cargo1, cargo2, cargo3]

#creating the vessels
vessel1 = Vessel("1",cargo1, 1, 1)
vessel2 = Vessel("2",cargo2, 1, 20)
vessel3 = Vessel("3",cargo2, 1, 30)
vessel4 = Vessel("4",cargo1, 1, 30)
vessel5 = Vessel("5",cargo2, 1, 30)
vessels = [vessel1, vessel2, vessel3, vessel4, vessel5]
vessels = []

instancias = open("instances50A400","r")
# f = open("saida50New10000.txt","w")

while True:
	nome = instancias.readline()
	if nome == "":
		break
	lenght = int(instancias.readline().split("\n")[0])
	arrival = int(instancias.readline().split("\n")[0])
	cargo_name = instancias.readline().split("\n")[0]
	for c in cargos:
		# print(c.n)
		# print(cargo_name)
		if (c.n == cargo_name):
			# print("entrou")	
			vessel = Vessel(nome, c, lenght, arrival)
			vessels.append(vessel)
			break

#vessel1.printing()

#creating the yards
yard_location_1 = Yard("A",cargo2, 10, 100, 1, 15, True, 1)
yard_location_2 = Yard("B",cargo1, 20, 100, 1, 30, True, 1)
yard_location_3 = Yard("C",cargo2, 30, 100, 7, 15, True, 1)
yard_location_4 = Yard("D",cargo1, 25, 100, 7, 30, False, 1)
yard_location_5 = Yard("E",cargo2, 35, 100, 1, 45, False, 1)
yard_location_6 = Yard("F",cargo1, 40, 100, 1, 60, True, 1)
yard_location_7 = Yard("G",cargo2, 50, 100, 7, 45, True, 1)
yard_location_8 = Yard("H",cargo1, 45, 100, 7, 60, True, 1)
yards = [yard_location_1, yard_location_2, yard_location_3, yard_location_4,yard_location_5,yard_location_6,yard_location_7,yard_location_8]

#yard_location_1.printing()

columns = []

for v in vessels:
	for j in range(len(sections)):
		for i in range(num_time):
			for y in yards:
				if (v.c_t == y.c_t or y.c_t.n == ""):
					distance = distance_cargo_section(y.c_t, yards, sections[j])
					# print (distance)
					beta = distance*v.c_t.get_rate()
					if(v.a <= i):
						column = Column(v, sections[j], y, beta, i)
					else:
						column = Column(v, sections[j], y, beta, v.a)
					# if(y.n == "A" or y.n == "B"):
					# 	column.c_t = y.c_t.n
					# column.y.time = column.h_t
					columns.append(column)

#print columns
# for c in columns:
# 	c.printing()
# 	print("\n")

def select_yard(vessel, yards):
	set_yard = []
	for y in yards:
		if (v.c_t == y.c_t):
			set_yard.append(y)
	y = random.choice(set_yard)
	return y

def distancia(berco, patio):
	d = math.sqrt(pow((berco.x - patio.x),2) + pow((berco.y - patio.y),2))
	return d	

def select_yard_best(berco, yards, cargo_type):
	menor = yards[0]
	#menord = distancia(berco, yards[0])
	yardsort = sorted(yards,key=lambda y: y.dist(berco))
	# for y in yardsort:
	# 	print(distancia(berco,y))

	# for i in range(len(yardsort)):
	# 	if(yardsort[i].ativo ==  True or (y.ativo == False and y.c_t == cargo_type)):
	# 		flag = 1
	# 		break
	

	flag = 0
	menort = yards[0].time
	menord = sys.maxsize
	for y in yards:
		if (menord > distancia(berco,y) and (y.ativo == True or (y.ativo == False and y.c_t == cargo_type))):
			flag = 1
			menord = distancia(berco,y)
			menor = y
	if(flag == 0):
		for y in yards:
			if(menort > y.time and (y.c_t == cargo_type)):
				menort = y.time
				menor = y
	else:
		menor.ativo = False
		menor.c_t = cargo_type
	return menor

def select_yard_random(berco,yards):
	return 

def compatible (column, columns):
	for c in columns:
		# if (c.s == column.s and c.s_t <= column.s_t and (column.s_t + column.h_t) <= (c.s_t + c.h_t)):
		# 	return False

		if(column.s != c.s):
			if(column.c_t == c.c_t or c.c_t == ""):
			# if(c.y == column.y):
			# 	if(c.y.time <= (column.y.time - column.h_t)): #  terminar isto, tempo de pátio
			# 		continue
			# 	else:
			# 		return False
			# else:
			# 	continue
				continue
			
		if((column.s_t + column.h_t <= c.s_t) or (column.s_t >= (c.s_t + c.h_t))):
			if(column.c_t == c.c_t or c.c_t == ""):
			# if(c.y == column.y):
			# 	if(c.y.time <= (column.y.time - column.h_t)):
			# 		continue
			# 	else:
			# 		return False
			# else:
			# 	continue
				continue
			
		else: 
			return False 	
		# elif (c.s_t == column.s_t and c.y == column.y):
		# 	return False
	return True

	
def reset():
	for s in sections:
		s.t = 1
	for y in yards:
		y.time = 1

def heuristic(vessels, columns):
	best = []
	for v in vessels:
		for c in columns:
			if best == []:
				best.append(c)
				c.c_t = v.c_t.n
				break
			elif c.belongs(v) and compatible(c, best):
				best.append(c)
				if(c.c_t == ""):
					c.c_t = v.c_t.n
				# c.y.time += c.h_t
				break
	return best

def fo(columns):
	soma = 0
	for c in columns:
		soma += c.s_t - c.v.a + c.h_t 
	return soma

def new_heuristic(vessels, sections, yards, alfaqqr):
	vesselsord = sorted(vessels, key=lambda vessel: vessel.a)
	# for v in vessels:
	# 	v.printing()
	columns = []
	menor = sections[0]
	menorTime = sections[0].t
	while(vesselsord != []):

		#pegando o melhor navio
		# v = vesselsord.pop(0)

		#pegando os alpha melhores navios
		melhoresVessels = []
		if(int(len(vesselsord)*alfaqqr) <= 1):
			alfaV = 1
		else:
			alfaV = int(len(vesselsord)*alfaqqr)
		for i in range(alfaV):
			melhoresVessels.append(vesselsord[i])
		v = random.choice(melhoresVessels)
		vesselsord.remove(v)

		newsort = sorted(sections, key=lambda x: x.t)
		# for k in newsort:
		# 	print (k.t)

		# for k in sections:
		# 	if (menorTime > k.t):
		# 		menor = k
		# 		menorTime = k.t

		#pegando o melhor berço
		# menor = newsort[0]
		# menorTime = menor.t

		#pegando os alpha melhores berços
		sectionRandom = []
		r = int(alfaqqr*len(sections))
		for i in range(r):
			sectionRandom.append(newsort[i])
		menor = random.choice(sectionRandom)
		menorTime = menor.t


		yard = select_yard_best(menor, yards, v.c_t)
		distance = distance_cargo_section(yard.c_t, yards, menor)
		beta = distance*v.c_t.get_rate()
		# if(v.a > menorTime and v.a > yard.time):
		# 	inicio_tempo = v.a
		# elif(yard.time > menorTime and yard.time > v.a):
		# 	inicio_tempo = yard.time
		# else:
		# 	inicio_tempo = menorTime
		if(v.a > menorTime):
			if(v.a > yard.time):
				inicio_tempo = v.a
			else:
				inicio_tempo = yard.time
		else:
			if(menorTime > yard.time):
				inicio_tempo = menorTime
			else:
				inicio_tempo = yard.time
		# print(v.a, menorTime, yard.time )
		column = Column(v, menor, yard, beta, inicio_tempo)
		columns.append(column)
		menor.t = column.s_t + column.h_t
		yard.time = column.s_t + column.h_t #aqui
		menorTime = sys.maxsize
	return columns
	
def swap(s1, s2):
    s1, s2 = s2, s1

def reset(sections, yards):
	for s in sections:
		s.t = 1	
	for y in yards:
		y.time = 1

def new_heuristic_2opt(vessels, sections, yards, alfaqqr):
	# vesselsord = sorted(vessels, key=lambda vessel: vessel.a)
	vesselsord = vessels
	# for v in vessels:
	# 	v.printing()
	columns = []
	menor = sections[0]
	menorTime = sections[0].t
	while(vesselsord != []):

		#pegando o melhor navio
		# v = vesselsord.pop(0)

		#pegando os alpha melhores navios
		melhoresVessels = []
		if(int(len(vesselsord)*alfaqqr) <= 1):
			alfaV = 1
		else:
			alfaV = int(len(vesselsord)*alfaqqr)
		for i in range(alfaV):
			melhoresVessels.append(vesselsord[i])
		v = random.choice(melhoresVessels)
		vesselsord.remove(v)

		newsort = sorted(sections, key=lambda x: x.t)
		# for k in newsort:
		# 	print (k.t)

		# for k in sections:
		# 	if (menorTime > k.t):
		# 		menor = k
		# 		menorTime = k.t

		#pegando o melhor berço
		# menor = newsort[0]
		# menorTime = menor.t

		#pegando os alpha melhores berços
		sectionRandom = []
		r = int(alfaqqr*len(sections))
		for i in range(r):
			sectionRandom.append(newsort[i])
		menor = random.choice(sectionRandom)
		menorTime = menor.t


		yard = select_yard_best(menor, yards, v.c_t)
		distance = distance_cargo_section(yard.c_t, yards, menor)
		beta = distance*v.c_t.get_rate()
		# if(v.a > menorTime and v.a > yard.time):
		# 	inicio_tempo = v.a
		# elif(yard.time > menorTime and yard.time > v.a):
		# 	inicio_tempo = yard.time
		# else:
		# 	inicio_tempo = menorTime
		if(v.a > menorTime):
			if(v.a > yard.time):
				inicio_tempo = v.a
			else:
				inicio_tempo = yard.time
		else:
			if(menorTime > yard.time):
				inicio_tempo = menorTime
			else:
				inicio_tempo = yard.time
		# print(v.a, menorTime, yard.time )
		column = Column(v, menor, yard, beta, inicio_tempo)
		columns.append(column)
		menor.t = column.s_t + column.h_t
		yard.time = column.s_t + column.h_t #aqui
		menorTime = sys.maxsize
	return columns	

# def trocar_berços(vessel1, vessel2, columns):
# 	for c1 in columns:
# 		for c2 in columns:
# 			if(c1.vessel == vessel1 and c2.vessel == vessel2):

# 	return true

# def fo_trocado(vessel1, vessel2):


# def troca(vessel1, vessel2):
	

# def busca_local(vessels, sections, yards, alpha):
# 	best = new_heuristic(vessels, sections, yards, alphaN[i])
# 	neighbor = []
# 	new_best = best
# 	for v1 in vessels:
# 		menor = v1
# 		for v2 in vessels:
# 			if(v1 != v2 and trocar_berços(v1,v2, best)):
# 				neighbor.append(v2)
		
# 		if(neighbor != []):
# 			for n in neighbor:
# 				if (fo_trocado(v1, n) < new_best):
# 					new_best = fo_trocado(v1, n)
# 					menor = n
# 		if(new_best < best ):
# 			troca(v1, menor)
# 	return new_best

#função que verifica se é possivel trocar berços
def trocar_berços(vessel, section, column, columns):
	#salva o berço anterior
	berco_anterior = column.s
	#troca o berço
	column.s = section

	#calcula o novo handling time
	distance = distance_cargo_section(column.y.c_t, yards, section)
	beta = distance*vessel.c_t.get_rate()

	#salva as variaveis antigas e troca o beta e handling time
	old_beta = column.beta
	old_h_t = column.h_t
	column.beta = beta
	column.h_t = column.alfa + column.beta

	#calcula o tempo de inicio e fim do navio naquele berço
	inicio = column.s_t
	fim = column.s_t + column.h_t

	#verifica se é possível encaixar a nova coluna no conjunto
	for c in columns:
		if(c != column and c.s == section):
			if(c.s_t <= inicio and (c.s_t+c.h_t >= inicio)):
				return False
			elif(c.s_t <= fim and (c.s_t+c.h_t >= fim)):
				return False
			elif(c.s_t >= inicio and (c.s_t+c.h_t <= fim)):
				return False

	#Se passou pelo for quer dizer que a coluna pode ser trocada
	#retorna as variaveis pros seus valores anteriores 
	column.s = berco_anterior
	column.beta = old_beta
	column.h_t = old_h_t
	return True

def fo_trocado(vessel, section, column, columns):
	#calculo a fo atual
	fo_atual = fo(columns)
	
	#salva o berço anterior
	berco_anterior = column.s
	#troca o berço
	column.s = section
	

	#calcula o novo handling time
	distance = distance_cargo_section(column.y.c_t, yards, section)
	beta = distance*vessel.c_t.get_rate()

	#salva as variaveis antigas e troca o beta e handling time
	old_beta = column.beta
	old_h_t = column.h_t
	column.beta = beta
	column.h_t = column.alfa + column.beta

	#calcula o fo da nova
	fo_nova = fo(columns)

	#retorna as variaveis pros seus valores anteriores 
	column.s = berco_anterior
	column.beta = old_beta
	column.h_t = old_h_t

	if(fo_nova < fo_atual):
		print(fo_atual, fo_nova)
		return True
	else:
		return False


def troca(vessel, section, column, columns):
	#troca o berço
	column.s = section

	#calcula o novo handling time
	distance = distance_cargo_section(column.y.c_t, yards, section)
	beta = distance*vessel.c_t.get_rate()

	#atualiza o handling time
	column.beta = beta
	column.h_t = column.alfa + column.beta


def busca_local(vessels, sections, yards, a):
	vesselscpy = vessels.copy()
	best = new_heuristic(vesselscpy, sections, yards, a)
	neighbor = []
	new_best = best
	navios = 1
	colunas = 1
	# for v in vessels: # para cada navio
	# 	for c in best: #para cada coluna
	# 		#procurando a coluna do návio
	# 		if (c.v == v):
	# 			for s in sections: #para cada berço
	# 				if(c.s != s):
	# 					#se for possível trocar o berço e se a fo dele trocado for melhor, ele troca
	# 					if(trocar_berços(v, s, c, best) and fo_trocado(v, s, c, best)):
	# 						troca(v, s, c, best)
	# 						print("navios: ", navios)
	# 	navios+=1
	
	vesselsord = sorted(vessels, key=lambda vessel: vessel.a)
	# best = new_heuristic(vessels, sections, yards, a)
	# new_best = best
	menor = fo(best)
	reset(sections, yards)
	entrou = False
	menori = 0
	menorj = 0
	fos = []
	for i in range(10):	
		for i in range(len(vesselsord)):
			for j in range(i+1,len(vesselsord)):
				if i!=j :
					print("i:", i , " j:", j)
					swap(vesselsord[i], vesselsord[j])
					vesselscopy = vesselsord.copy()
					new_best = new_heuristic_2opt(vesselscopy, sections, yards, a)
					print("menor: ", menor, " novo: ", fo(new_best))
					if fo(new_best) < menor:
						menor = fo(new_best)
						menori = i
						menorj = j
						entrou = True

					swap(vesselsord[i], vesselsord[j])
					reset(sections, yards)

		if entrou:
			swap(vesselsord[menori], vesselsord[menorj])
			entrou = False
			print("menor fo:", menor)
			fos.append(menor)
	
	for f in fos:
		print(f)
	
	for c in new_best:
		c.printing()
		
		


		
						


				

			 

# best = heuristic(vessels, columns)
# best_new = new_heuristic(vessels, sections, yards, alfaqqr)

# i = 0
# for c in best:
# 	i += 1

# j = 0
# print("Solução: \n")
# for c in best_new:
# 	c.printing()
# 	j += 1
# 	print("\n")


# print(i)

# print(j)

# print("Valor da FO = ", fo(best))

# print("Valor da FO nova = ", fo(best_new))



random.seed(0)

best = []

#alfa reativo

# for k in range(100):
# 	indice = 0
# 	medias = [0,0,0,0,0,0,0,0,0,0]
# 	soma = [0,0,0,0,0,0,0,0,0,0]

# 	vetor_fo = [0,0,0,0,0,0,0,0,0,0]

# 	qi = [0,0,0,0,0,0,0,0,0,0]
# 	for j in range(B):
# 		sorteado = random.randrange(100)
# 		# print (sorteado)
# 		for i in range(10):
# 		#    print(pAlphaN[i][0])
# 			if(pAlphaN[i][0] <= sorteado and pAlphaN[i][1] >= sorteado):
# 				indice = i
# 				soma[i] += 1.0
# 				# print(alphaN[i])

# 				# inicio = time.time()
# 				best = new_heuristic(vessels, sections, yards, alphaN[i])
# 				# fim = time.time()
# 				# print(fim - inicio)

# 				f.write("alfa = ")  
# 				f.write(str(alphaN[i]))
# 				f.write("\n")
# 				f.write("Valor da FO nova = ")
# 				f.write(str(fo(best)))
# 				f.write("\n")
# 				vetor_fo[i] += fo(best)
# 				reset()
# 				break
#         # print (sorteado, alphaN[indice])

# 	for i in range(10):
# 		if(soma[i] == 0):
# 			qi[i] = 0
# 		else:
# 			medias[i] = vetor_fo[i]/soma[i]
# 			qi[i] = (1/medias[i])*pow(10,5)
# 		frase = "i: " + str(i) + "soma: " + str(soma[i]) + "FO: " + str(vetor_fo[i]) + "medias: " + str(medias[i]) + "qi: " + str(qi[i])
# 		f.write(frase)
# 		f.write("\n")

# 	q = 0
# 	for i in range(10):
# 		q += qi[i]

# 	print(q)

# 	novopAlphaN =[]

# 	somaP = 0

# 	for i in range(10):
# 		pAlphaN[i] = qi[i]/q*100
# 		print(pAlphaN[i])
# 		if(qi[i] == 0):
# 			novopAlphaN.append([somaP, somaP])
# 		else:	
# 			novopAlphaN.append([somaP, somaP + pAlphaN[i] - 1])
# 		somaP += pAlphaN[i]
# 		# print(soma)

# 	for i in range(10):
# 		f.write(str(novopAlphaN[i]))
# 		f.write("\n")

# 	pAlphaN = novopAlphaN

# for a in alphaN:
# 	print("alpha: ", a)
# 	busca_local(vessels, sections, yards, a)
	
#fazendo a busca local
busca_local(vessels, sections, yards, 0.1)


#criar novo laço para testar a solução viável da literatura
#continuar a tabela, valores iguais no começo e intercalando depois
#aleatoridade com berço e pátio
#tentar fazer uma função gulosa onde para cada navio verifica a combinação de berço e pátio e vê qual a melhor, ou seja,
#fazer as colunas para cada navio
#cuspir a resposta num arquivo, csv talvez, automatizar a coleta de dados


#marcar o tempo de execução do algoritmo - gprof
#implementar o alfa reativo, alfa 1 e alfa 2, um para navio e um para berço, e a intercalação dos dois.
#Escrever no papel o problema e o algoritmo de solução, heurística proposta no formato de pseudo-código
#cuspir a resposta num arquivo, csv talvez, automatizar a coleta de dados
#Testar com 10 instâncias de cada tamanho

#Automatizar a saida
#Colocar o guloso junto na tabela, e executar com 100000 
#Escrever no papel o problema e o algoritmo de solução, heurística proposta no formato de pseudo-código
#Busca Local e GRASP

#busca local
