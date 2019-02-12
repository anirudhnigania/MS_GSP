from collections import OrderedDict
from utils import Sequence

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
		self._sort()
		self._initPass()
		self._f1()
		print (self.SC)
		k = 2
		while (True):
			if k == 2:
				self._level2Candidategen()
			else:
				break
			#sk = 0
			for s in self.S:
				#ck = 0
				for c in self.C[k]:
					#if sk == 1 and ck == 0:
					if self._contains(c.sequence,s):
						c.count += 1
					#ck += 1
				#sk += 1
			self._frequentSequence(k)
			k+=1

		#for item in self.C[2]:
		#	print ("{} --- {}".format(item.sequence,item.count))
		print (self.F[2])

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
		F1 = []
		for item in self.L:
			if self.SC[item] >= self.MS[item]:
				F1.append(item)
		self.F[1] = F1

	def _level2Candidategen(self):
		C2 = []
		for idx, l in enumerate(self.L):
			if self.SC[l] >= self.MS[l]:
				C2.append(Sequence([[l],[l]],l))
				for h in self.L[idx+1:]:
					if self.SC[h] >= self.MS[l] and abs(self.SC[h] - self.SC[l]) <= self.SDC:
						cMinMISItem = l
						if self.MS[l] > self.MS[h]:
							cMinMISItem = h
						C2.append(Sequence([[l],[h]],cMinMISItem))
						C2.append(Sequence([[h],[l]],cMinMISItem))
						if h > l:
							C2.append(Sequence([[l,h]],cMinMISItem))
						else:
							C2.append(Sequence([[h,l]],cMinMISItem))
		self.C[2] = C2
	
	def _contains(self,c,s):
		#print ("{} ---- {}".format(c,s))
		sIdx = 0
		sSize = len(s)
		cSize = len(c)
		#print ("sSize : {}, cSize : {}".format(sSize,cSize))
		if cSize > sSize:
			return False

		for cIdx, cItemSet in enumerate(c):
			cRemSize = cSize - cIdx
			#print ("cRemSize : {}, cItemSet : {}".format(cRemSize,cItemSet))
			while sIdx < sSize and not self._subSequence(cItemSet,s[sIdx]):
				sIdx += 1
				if (sSize - sIdx) < cRemSize:
					return False
			sIdx += 1
		return True

	def _subSequence(self,c,s):
		sLen = len(s)
		sPrvIdx = -1
		for cIdx, cItem in enumerate(c):
			if cItem in s and s.index(cItem) >= sPrvIdx:
				sPrvIdx = s.index(cItem)
			else:
				return False
		return True

	def _frequentSequence(self,k):
		F = []
		for c in self.C[k]:
			#print (c.sequence)
			if c.count/self.n >= self.MS[c.minMISItem]:
				F.append(c.sequence)
		self.F[k] = F


			







