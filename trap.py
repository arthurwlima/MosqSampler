
class arma:
	''' Defines the trap class. The main diference between traps and
	reservoir is traps nominal attractiveness, a measure of the relative
	preference a mosquito has for a trap, compared to a reservoir. 
	A list of trap attractiveness ('eficiencia') is passed to the method, 
	in order to evaluate traps with different nominal attractiveness in 
	exactly the same simulation (Easier comparisons and better computation time)'''
	def __init__ (self,area,eficiencia,armtype='O'):
		self.area=area
		self.e  = eficiencia    # List of traps attractiveness
		self.contagem = [0,0,0,0,0,0]
		self.eggs = [0,0,0,0,0,0]
		self.type = armtype

    

class poca:
	''' Defines the reservoir class.'''
	def __init__(self,area):
		self.area=area
		self.eggs =  [0,0,0,0,0,0]
		self.contagem =  [0,0,0,0,0,0]
