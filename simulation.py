# from visual import * 
#import random,math,pylab, visual
import random, math

from area import *

class simulacao:
    '''Creates each replicate of a simulation and sore its results in the 
    appropriate files: ArqArmadilhas - trap sampling results, ArqMosquito - Mosquito population results'''
    def __init__(self, nmosq, narms, eficiencia, fator, npocas, rovip, padraoArmas, padraoPocas, padraoDesloc, arqArmadilha, arqMosquito, reps=1):
        self.numero=reps
        
        self.diversasRep(nmosq, narms, eficiencia, fator, npocas, rovip, padraoArmas, padraoPocas, padraoDesloc, arqArmadilha, arqMosquito)
        
    def diversasRep(self, nmosq, narms, eficiencia, fator, npocas, rovip, padraoArmas, padraoPocas, padraoDesloc, arqArmadilha, arqMosquito, reps=5):
        ## A higher level method to prepare and instantiate different replicates
        for r in xrange(reps):
            self.replica=area(nmosq,narms,npocas,rovip,eficiencia,fator)
            if padraoArmas==0:
                self.replica.armaRandom(eficiencia, narms, rovip)
            else:
                self.replica.armaRegular(eficiencia, narms, rovip)
            
            if padraoPocas==0:
                self.replica.pocaRandom(npocas, rovip)
            else: 
                self.replica.pocaCluster(npocas, rovip, fator)
            
            self.rodar(padraoDesloc, arqArmadilha, arqMosquito, r)
        
    def rodar(self, padraoDesloc, arqArmadilha, arqMosquito, nReplic, ndias=10):            
		## Mosquitoes will update its gonotrophic status, move and oviposit during 'ndays' in simulation time 
        if(padraoDesloc==0):
            for d in xrange(ndias):
                self.r=[( i.age(),i.desloc(), i.oviposit() ) for i in self.replica.LM]
                if (d+1)%10==0:
                    arma =1
                    mos = 1
                    for a in self.replica.LA:
                        iCtrl=0
                        for e in a.e:
                            arqArmadilha.write( str(self.replica.narms)+','+str(e)+','+str(self.replica.npocas)+','+str(self.replica.nmosq)+','+str(nReplic)+','+str(arma)+','+str(a.pos[0])+','+str(a.pos[1])+','+str(a.contagem[iCtrl])+'\n')
                            iCtrl+=1
                        arma += 1
                    
                    for m in self.replica.LM:
                        arqMosquito.write( str(self.replica.narms)+','+str(self.replica.npocas)+','+str(self.replica.nmosq)+','+str(nReplic)+','+str(mos)+','+str(m.pos[0])+','+str(m.pos[1])+'\n')
                        mos +=1

        else:
            # An estabilization time is required in cases of clustered oviposition sites and habitat-dependent random walks            
			for d in xrange(400):
				self.r=[( i.age(),i.desloc2(), i.oviposit() ) for i in self.replica.LM]
			
			for a in self.replica.LA:
				a.contagem=[0,0,0,0,0,0]
            
            # Sampling period
			for d in xrange(ndias):
				self.r=[( i.age(),i.desloc2(), i.oviposit() ) for i in self.replica.LM]
				if (d+1)%10==0:
					arma = 1
					mos = 1
					for a in self.replica.LA:
						iCtrl=0
						for e in a.e:
							arqArmadilha.write( str(self.replica.narms)+','+str(e)+','+str(self.replica.npocas)+','+str(self.replica.nmosq)+','+str(nReplic)+','+str(arma)+','+str(a.pos[0])+','+str(a.pos[1])+','+str(a.contagem[iCtrl])+'\n')
							iCtrl+=1
						arma += 1
                    
					for m in self.replica.LM:
						arqMosquito.write( str(self.replica.narms)+','+str(self.replica.npocas)+','+str(self.replica.nmosq)+','+str(nReplic)+','+str(mos)+','+str(m.pos[0])+','+str(m.pos[1])+'\n')
						mos +=1


def run(nmosq, narms,npocas,eficiencia,rovip, CENARIO, grafico=0):
    '''Each 'CENARIO' (scenarium) is a combination of mosquitoes'
    moving behaviour (desloc) and natural reservoirs distribution pattern (padraoPoca).
    For each environmental scenarium, different sampling schemes are evaluated and 
    snd the results stored in the files fArmas (trap results), and fMosq
    (Mosquito population results).
    CENARIO = 0 -> Random walks / Natural reservoirs randomly distributed in the area
    CENARIO = 1 -> Random walks / Natural reservoirs clustered in the area
    CENARIO = 2 -> Habitat-dependent random walks / Natural reservoirs randomly distributed in the area
    CENARIO = 3 -> Habitat-dependent random walks / Natural reservoirs clustered in the area
    CENARIO = 4 -> Habitat-dependent random walks / Natural reservoirs clustered in the area (higher clustering)'''

    for c in CENARIO:
        print 'Cenario ', c
        idSim = 'A0_Cenario'+str(c)
        fArmas = open('Armadilhas_'+idSim+'.csv', 'w')
        fArmas.write('narms, eficiencia, nPocas, nMosq, Semana, Armadilha, posX, posY, Contagem\n')
        fMosq = open('Mosq_'+idSim+'.csv', 'w')
        fMosq.write('narms, nPocas, nMosq, Semana, Mosquito, posX, posY\n')
        for p in npocas:
            for a in narms:
                for n in nmosq:
                    print n, a, p
                    if c==0:	
                        cen = simulacao(n, a, eficiencia, 1, p, rovip, 0, 0, 0, fArmas, fMosq)
                        
                    elif c==1: 
                        cen = simulacao(n, a, eficiencia, 0.06, p, rovip, 0, 0, 1, fArmas, fMosq)
                        
                    elif c==2:           
                        cen = simulacao(n, a, eficiencia, 0.06, p, rovip, 0, 0, 1, fArmas, fMosq)
                        
                    elif c==3:			
                        cen = simulacao(n, a, eficiencia, 0.06, p, rovip, 0, 1, 1, fArmas, fMosq)
                        
                    elif c==4:          
                        cen = simulacao(n, a, eficiencia, 0.05, p, rovip, 0, 1, 1, fArmas, fMosq)
        fMosq.close()
        fArmas.close()


if __name__=="__main__":


   run ( nmosq=[100], narms=[1000], npocas=[2000], eficiencia=[0.5], rovip = 30, CENARIO = [0,1,2,3,4])  

