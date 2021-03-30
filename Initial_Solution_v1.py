# -*- coding: utf-8 -*-
import random
import sys
import copy
n = 2
num_section = 2
cargo = {1:"ferro", 2:"bauxita", 3:"cobre", 4:"prata"}
# cargo_type = ["ferro", "bauxita", "cobre"]

cargo_type = ["cobre", "ferro"]

#print cargo[3]

time = [0,0,0,0,0,0,0]
num_time = 1000
section = [0,0]

instancias = open("instances50L400", "w")
# instancias = open("instances50","r")
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
	def __init__(self, name, distance, time):
		self.n = name
		self.d = distance
		self.t = time
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
		self.c_t.printing()
		print (self.a)

#class Yard has the cargo type, the distance from the location to the
#berth and the capacity from the yard
class Yard:
	def __init__(self,name, cargo_type, distance, capacity):
		self.n = name		
		self.c_t = cargo_type
		self.d = distance
		self.c = capacity
	def printing(self):
		print ("location "+self.n)
		self.c_t.printing()
		print (self.d, self.c)

#class Column has the vessel
class Column:
	def __init__(self, vessel, section, yard, beta, time):
		self.s = section
		self.y = yard
		self.h_t = alfa + beta #handling time = tempo de load/unload da carga + tempo de transferencia da carga
		self.v = vessel
		self.s_t = time #starting time
	def printing(self):
		self.v.printing()
		self.s.printing()
		self.y.printing()
		print ("Starting Time: ",self.s_t, "Handling Time: ", self.h_t)
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
section1 = Section("1", 10, 1)
section2 = Section("2", 10, 1)
section3 = Section("3", 30, 1)
section4 = Section("4", 30, 1)
section5 = Section("5", 45, 1)
section6 = Section("6", 45, 1)
section7 = Section("7", 15, 1)
section8 = Section("8", 15, 1)
section9 = Section("9", 25, 1)
section10 = Section("10", 25, 1)
section11 = Section("11", 45, 1)
section12 = Section("12", 15, 1)
section13 = Section("13", 30, 1)
section14 = Section("14", 10, 1)
section15 = Section("15", 20, 1)

sections = [section1,section2,section3,section4,section5,section6,section7,section8,section9,section10,section11,section12,section13,section14,section15]

#creating the type of cargos
# cargo1 = Cargo("cobre", 0.7)
# cargo2 = Cargo("ferro", 0.8)
# cargo3 = Cargo("bauxita", 0.9)
# cargos = [cargo1, cargo2, cargo3]

cargo1 = Cargo("cobre", 0.7)
cargo2 = Cargo("ferro", 0.8)
cargos = [cargo1, cargo2]

# #creating the vessels
# vessel1 = Vessel("1",cargo1, 1, 1)
# vessel2 = Vessel("2",cargo2, 1, 20)
# vessel3 = Vessel("3",cargo2, 1, 30)
# vessels = [vessel1, vessel2, vessel3]

vessels = []

# while True:
# 	nome = instancias.readline()
# 	if nome == "":
# 		break
# 	lenght = int(instancias.readline().split("\n")[0])
# 	arrival = int(instancias.readline().split("\n")[0])
# 	cargo_name = instancias.readline().split("\n")[0]
# 	for c in cargos:
# 		# print(c.n)
# 		# print(cargo_name)
# 		if (c.n == cargo_name):
# 			# print("entrou")	
# 			vessel = Vessel(nome, c, lenght, arrival)
# 			vessels.append(vessel)
# 			break
# for v in vessels:
# 	v.printing()
	 
		

for i in range(50):
	vessel = Vessel(str(i), random.choice(cargos), 1, random.randint(1,400))
	vessels.append(vessel)

for v in vessels:
	instancias.write(v.n)
	instancias.write("\n")
	instancias.write(str(v.l))
	instancias.write("\n")
	instancias.write(str(v.a))
	instancias.write("\n")
	instancias.write(v.c_t.n)
	instancias.write("\n")

#creating the yards
# yard_location_1 = Yard("A",cargo2, 10, 100)
# yard_location_2 = Yard("B",cargo3, 20, 100)
# yard_location_3 = Yard("C",cargo3, 30, 100)
# yard_location_4 = Yard("D",cargo1, 25, 100)
# yards = [yard_location_1, yard_location_2, yard_location_3, yard_location_4]


yard_location_4 = Yard("D",cargo1, 25, 100)
yard_location_1 = Yard("A",cargo2, 10, 100)
yards = [yard_location_4, yard_location_1]

#yard_location_1.printing()

columns = []

for v in vessels:
	for j in range(len(sections)):
		for i in range(num_time):
			for y in yards:
				if (v.c_t == y.c_t):
					distance = distance_cargo_section(y.c_t, yards, sections[j])
					# print (distance)
					beta = distance*v.c_t.get_rate()
					if(v.a <= i):
						column = Column(v, sections[j], y, beta, i)
					else:
						column = Column(v, sections[j], y, beta, v.a)
					columns.append(column)

#print columns
# for c in columns:
# 	c.printing()
# 	print("\n")

def select_yard(vessel, yards):
	set_yard = []
	for y in yards:
		# y.printing()
		if (vessel.c_t == y.c_t):
			# y_copy = copy.deepcopy(y)
			set_yard.append(y)
	yard = random.choice(set_yard)
	return yard


def compatible (column, columns):
	for c in columns:
		# if (c.s == column.s and c.s_t <= column.s_t and (column.s_t + column.h_t) <= (c.s_t + c.h_t)):
		# 	return False
		if(column.s != c.s):
			continue
		if((column.s_t + column.h_t <= c.s_t) or (column.s_t >= (c.s_t + c.h_t))):
			continue
		else: 
			return False 	
		# elif (c.s_t == column.s_t and c.y == column.y):
		# 	return False
	return True

	


def heuristic(vessels, columns):
	best = []
	for v in vessels:
		for c in columns:
			if best == []:
				best.append(c)
				break
			elif c.belongs(v) and compatible(c, best):
				best.append(c)
				break
	return best

def fo(columns):
	soma = 0
	for c in columns:
		soma += c.s_t - c.v.a + c.h_t 
	return soma

def new_heuristic(vessels, sections, yards):
	new_v = sorted(vessels, key=lambda vessel: vessel.a)
	# for v in new_v:
	# 	v.printing()
	columns = []
	menor = sections[0]
	menorTime = sections[0].t
	while(new_v != []):
		v = new_v.pop(0)
		for k in sections:
			if (menorTime > k.t):
				menor = k
				menorTime = k.t
		# y = copy.deepcopy(yards)
		yard = select_yard(v, yards)
		distance = distance_cargo_section(yard.c_t, yards, menor)
		beta = distance*v.c_t.get_rate()
		if(v.a > menorTime):
			inicio_tempo = v.a
		else:
			inicio_tempo = menorTime
		column = Column(v, menor, yard, beta, inicio_tempo)
		columns.append(column)
		menor.t += column.h_t
		menorTime = sys.maxsize
	return columns
	


# best = heuristic(vessels, columns)

# best_new = new_heuristic(vessels, sections, yards)


# print("Solução: \n")
# for c in best:
# 	c.printing()
# 	print("\n")

# print("Valor da FO = ", fo(best))
# print("Valor da FO nova = ", fo(best_new))



	
