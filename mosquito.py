import random,math
#import psyco
#psyco.full()

class mosq:
    ''' Classe mosq cria mosquitos que voam em uma area de tamanho dim'''

    def __init__(self, area , gono , rovip , desloc=30  , eggs=10, poca = None,  gene = [ 'S' , 'R' ] , geneNeutro = [ 'A' , 'B'] ):
        ''' area e' o landscape onde os mosquitos habitam. Mosquitos estao distribuidos aleatoriamente no momento inicial. 'gono' e' o estado gonotrofico inicial (mosquitos oscilam entre nao ovipondo e ovipondo. 'desloc'  e' a unidade de deslocamento diario max do mosquito, 'eggs' e o numero medio de ovos '''
                # variaveis de localizacao inicial e deslocamento
        self.area = area
        if poca == None:
            self.pos=((random.uniform(0,self.area.dim)),(random.uniform(0,self.area.dim)))
        else: self.pos =poca.pos
            
        self.d = desloc
        # variaveis fisiologicas iniciais
        self.idade=0
        self.gonostate = gono
        self.egg = eggs
        # contador do estagio gonotrofico (ha quantos dias esta no estado gonostate) 
        self.statecount = 0
        # duracao dos estados gono =0 e gono=1
        self.gono0 = 2
        self.gono1 = 2
        # raio de busca local de sitios para ovipor
        self.r = rovip
        self.LinventarioA = []
        self.LinventarioP = []

        # flag para identificar os objetos que serao retirados da lista de mosquitos
        self.morto = 0

        # Genes de resistencia
        self.gene = gene
        # Genes Neutros
        self.geneNeutro = geneNeutro

        # Posicao na grade
        self.posX = int(self.pos[0])/int(self.r)
        self.posY = int(self.pos[1])/int(self.r)
        self.celula = self.area.M[self.posX][self.posY]
        self.area.M[self.posX][self.posY].LM.append(self)

        
    def desloc(self, distancia = 30):
        ''' O deslocamento e' um random walk na superficie de um torus'''
        self.pos=((self.pos[0]+random.uniform(-distancia,distancia)),(self.pos[1]+random.uniform(-distancia,distancia)))
        if self.pos[0] > self.area.dim: self.pos = (self.pos[0] - self.area.dim,self.pos[1])
        if self.pos[1] > self.area.dim: self.pos = (self.pos[0], self.pos[1] - self.area.dim)
        if self.pos[0] < 0: self.pos = (self.area.dim + self.pos[0],self.pos[1])
        if self.pos[1] < 0: self.pos = (self.pos[0],self.area.dim + self.pos[1])

        if self.pos[0] <0 or   self.pos[1] <0 or self.pos[0] > self.area.dim or self.pos[0] > self.area.dim:
            print "mosquitos estao saindo da area"

        self.posX = int(self.pos[0])/int(self.r)
        self.posY = int(self.pos[1])/int(self.r)
        self.celula = self.area.M[self.posX][self.posY]
        
    def age(self):
        '''Mosquitos envelhecem e transitam entre o estagio gonotrofico 0 (nao ovipondo) e estagio gonotrofico 1 (ovipondo)'''
        self.idade +=1
        # se ja tiver chegado ao fim do estagio gonotrofico, mudar de etagio e resetar o contador
        # senao apenas avancar o contador
        if self.gonostate == 0:
            if self.statecount == self.gono0:
                self.gonostate = 1
                self.statecount = 0
            else: self.statecount +=  1
            
        elif self.gonostate == 1:
            if self.statecount == self.gono1:
                self.gonostate = 0
                self.statecount = 0
            else:  self.statecount +=  1


    def inventario(self):
        '''fazer inventario dos sitios para ovipor na vizinhanca, buscando aqueles que estao a menos de um raio r
        Busca atraves da matriz de vizinhancas, cada celula tem lado = rovip'''
        self.LinventarioA = []
        self.LinventarioP = []
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                x=self.posX+i
                y=self.posY+j 
                if (x <0 or y<0):
                    pass
                if (x>=self.area.nLinhas or y>=self.area.nLinhas): 
                    pass
                
                else:
                    for p in self.area.M[ x ][ y ].LR:
                        ##math.sqrt
                        if (self.pos[0] - p.pos[0])**2 + (self.pos[1] - p.pos[1])**2  < self.r:
                            self.LinventarioP.append(p)
                
                    for a in self.area.M[ x ][ y ].LA:
                        if (self.pos[0] - a.pos[0])**2 + (self.pos[1] - a.pos[1])**2  <self.r:
                            self.LinventarioA.append(a)
            
        
    def oviposit(self):
        ''' Se a femea esta no estagio gono 1, ele fara um inventario para ovipor, caso controrio voa'''
        if self.gonostate == 0:
            return 0
        else:
            iCtrl = 0
            self.inventario()
            armef = self.area.LA[0]
            for e in armef.e:
                np=len(self.LinventarioP)
                na=len(self.LinventarioA)
                np=len(self.LinventarioP)*(1-e)
                na=len(self.LinventarioA)*(e)
                n=np+na
                if n:
                    x=random.uniform(0,1)
                    if x>((na)/n): # eficiencia ou numero de armadilhas baixos; ovoposicao nas pocas
                        if self.LinventarioP:
                            alvo = random.sample(self.LinventarioP,1)
                            alvo[0].contagem[iCtrl]+=1
                            
                    else:  #  a eficiencia das armadilhas e alta, ou so ha aramadilhas; ovoposicao nas armadilhas
                        if self.LinventarioA:
                            alvo = random.sample(self.LinventarioA,1)
                            alvo[0].contagem[iCtrl] +=1
                iCtrl+=1
        
    
    def desloc2(self):
		''' O deslocamento e' um random walk adaptativo na superficie de um torus'''

		if self.gonostate==0:
			self.desloc(self.d)
			return 0
		else:
			self.n = len(self.LinventarioA) + len(self.LinventarioP)
			self.d = 30./(self.n+1)
        ##      	  print self.n, self.d, self.dr
			self.pos = ((self.pos[0]+random.uniform(-self.d,self.d)),(self.pos[1]+random.uniform(-self.d,self.d)))
        ##        print self.pos
			if self.pos[0] > self.area.dim: self.pos = (self.pos[0] - self.area.dim,self.pos[1])
			if self.pos[1] > self.area.dim: self.pos = (self.pos[0], self.pos[1] - self.area.dim)
			if self.pos[0] < 0: self.pos = (self.area.dim + self.pos[0],self.pos[1])
			if self.pos[1] < 0: self.pos = (self.pos[0],self.area.dim + self.pos[1])
            
			if self.pos[0] <0 or   self.pos[1] <0 or self.pos[0] > self.area.dim or self.pos[0] > self.area.dim:
				print "mosquitos estao saindo da area"
			self.posX = int(self.pos[0])/int(self.r)
			self.posY = int(self.pos[1])/int(self.r)
			self.celula = self.area.M[self.posX][self.posY]

