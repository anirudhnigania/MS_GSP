from collections import OrderedDict

class MSGsp:
	def __init__(self,S,MS,n,SDC):
		self.S = S
		self.MS = MS
		self.n = n
		self.SDC = SDC
		self.M = None
		self.L = []
		self.SC = {}
		self.F = OrderedDict()
		self.C = OrderedDict()
		self.F1 = []

		self._sort()
		self._initPass()
		self._f1()
		self._level2Candidategen()
		print (self.M)
		print (self.SC)
		print (self.L)
		print (self.F1)
		print (self.C[2])

	def _sort(self):
		self.M = OrderedDict(sorted(self.MS.items(),key=lambda t:t[1]))

	def _initPass(self):
		lMISItem = None
		lMIS = None
		isMatched = False

		self.SC = {item: sum([1 for sequence in self.S if sum(1 for itemset in sequence if item in itemset) > 0])/self.n for item in self.M}

		for item, mis in self.M.items():
			if (not isMatched) and item in self.SC and self.SC[item] >= mis:
				isMatched = True
				lMISItem,lMIS = item,mis
				self.L.append(item)
			elif isMatched and item in self.SC and self.SC[item] >= lMIS:
				self.L.append(item)

	def _f1(self):
		for item in self.L:
			if self.SC[item] >= self.MS[item]:
				self.F1.append(item)

	def _level2Candidategen(self):
		C2 = []
		for idx, l in enumerate(self.L):
			if self.SC[l] >= self.MS[l]:
				for h in self.L[idx+1:]:
					if self.SC[h] >= self.MS[l] and abs(self.SC[h] - self.SC[l]) <= self.SDC:
						C2.append([[l],[h]])
						C2.append([[h],[l]])
						if h > l:
							C2.append([[l,h]])
						else:
							C2.append([[h,l]])
		self.C[2] = C2
					
