import random,math
from mosquito import *
from trap import *


class cell:
	'''Defines units of a grid in the landscape ('area'). Just a suuport 
	to avoid the burden of mosquitoes searching the entire landscape for
    oviposition sites. Though, the search is still continuous space.
	'Cells' keeps the record of mosquitoes, traps and reservoirs inside''' 
	def __init__(self, area):
		self.area=area
		self.LR =  []
		self.LA = []
		self.LM = []

class area:
	''' The object 'area' defines the bi-dimensional landscape where the 
	mosquitoes live. The dimension 'sideSize' is necessary to instantiate 
	the area. "area' objects have methods for creating the population of 
	mosquitoes, traps and reservoirs.  For automatic instantiation of 
	these objects, the specific attributes must be provided.'''
	def __init__(self, nmosq, narms, npocas, rovip, eficiencia, fator, sideSize=900):
		self.dim = sideSize  # Side of the square area
		self.LA = []    # Empty list of traps 
		self.LM =[]    # Empty list of mosquitoes
		self.LR=[]   # Empty list of reservoirs
		self.M = [] # Empty matrix for optimizing search
		self.narms = narms
		self.npocas = npocas
		self.nmosq = nmosq
		
		if sideSize%rovip:
			self.nLinhas = (sideSize/rovip) +1
		else: self.nLinhas = sideSize/rovip

		self.criaMatriz(self.nLinhas)

		if nmosq:
			self.createMosqPop(nmosq,rovip) # creating the mosquito population





	def criaMatriz(self, nLines):
		'''Matrix to define the grid in the area. Grid size is defined 
		based  on mosquito's oviposition radius, to limit the mosquito 
		searching region to its adjacent cells'''

		for i in xrange(nLines):
			self.M.append([])
		for l in self.M:
			for c in xrange(nLines):
				l.append(cell(self))
                 
	def createMosqPop(self,nmosq,rovip):
		'''Creates a population of mosquitoes, randomly distributed in 
		the area. Mosquitoes are created with age '1', oviposition radius
		'rovip' and randomly assigned a gonotrophic stage 'gono' '''
		self.LM=[mosq(self,(random.choice([0,1])),rovip) for i in xrange(nmosq)] 

	def armaRandom(self,eficiencia,narms, rovip):
		''' Creates 'narms' trap objects and sets them randomly in the area'''
		for i in xrange(narms):
			a=arma(self,eficiencia)
			a.pos=(random.uniform(20,(self.dim-20)),random.uniform(20,(self.dim-20)))
			self.LA.append(a)
			posX = int(a.pos[0])/int(rovip)
			posY = int(a.pos[1])/int(rovip)
			self.M[posX][posY].LA.append(a)
        
	def armaRegular(self, eficiencia, narms, rovip):
		''' Creates 'narms' trap objects and sets them in a regular grid'''
		self.q = math.sqrt(narms) 
		self.d = self.dim / self.q
		self.b = int( self.q)
		for i in xrange (self.b):
			for j in xrange (self.b):
				a=arma(self,eficiencia)
				a.pos = ( self.d/2 + i*self.d , self.d/2 + j*self.d)
				self.LA.append(a)
				posX = int(a.pos[0])/int(rovip)
				posY = int(a.pos[1])/int(rovip)
				self.M[posX][posY].LA.append(a)
            
	def pocaRandom(self,npocas, rovip):
		''' Creates 'npocas' reservoirs objects and sets them randomly in the area'''
		for i in xrange(npocas):
			p=poca(self)
			p.pos = (random.uniform(20,(self.dim-20)),random.uniform(20,(self.dim-20)))
			self.LR.append(p)
			posX = int(p.pos[0])/int(rovip)
			posY = int(p.pos[1])/int(rovip)
			self.M[posX][posY].LR.append(p)
        
	def pocaCluster(self, npocas, rovip, fator, nKey=4):
		''' Creates 'npocas' reservoir objects and sets them clusterd 
		around 'nKey' key-points in the area. For now, key-points are 
		distributed in a regular grid. Position of the remaining reservoirs
		defined by a normal distribution, centered in the position of the
		key-points and with standard deviation equals 'sideSize*factor'. 
		Factor should be in the interval ]0,1[, the lower the factor, 
		more clustered is the distribution'''
		self.restante = (npocas - nKey)/nKey
		self.a = math.floor ( math.sqrt(nKey) )
		self.d = self.dim / self.a
		self.b = int( self.a)
		self.DP = self.dim * fator
        
		for i in xrange (self.b):
			for j in xrange (self.b):
				p = poca(self)
				p.pos = ( self.d/2 + i*self.d , self.d/2 + j*self.d)
				self.LR.append(p)
				posX = int(p.pos[0])/int(rovip)
				posY = int(p.pos[1])/int(rovip)
				self.M[posX][posY].LR.append(p)
                
				for m in xrange(self.restante):
					p2 =poca(self)
					pos0 = pos1 = -1
					while pos0 < 0 or pos0 > self.dim or pos1 < 0 or pos1 > self.dim:
						pos0 = random.normalvariate(p.pos[0], self.DP)
						pos1 = random.normalvariate(p.pos[1], self.DP)
					p2.pos = (pos0, pos1)
					posX = int(p2.pos[0])/int(rovip)
					posY = int(p2.pos[1])/int(rovip)
					self.LR.append(p2)
					self.M[posX][posY].LR.append(p2)
       

def teste():
	t = area(2,100,100,20,20,[.5],400)
	t.armaRandom([0.5],100,20)
	t.pocaRandom(100,20)      
	print t.LA, t.LR
	for d in xrange(5):
		for i in t.LM:
			i.age()
			i.desloc()
			i.oviposit()
			print i.LinventarioA, i.LinventarioP

if __name__=="__main__":

    teste()
 
