from collections import OrderedDict
from utils import Sequence
import copy

class MSGsp:
	def __init__(self,S,MS,n,SDC):
		self.S = S
		self.MS = MS
		self.n = n
		self.SDC = SDC
		self.M = None
		self.L = []
		self.SC = {}
		self.C = {}
		self.F = OrderedDict()
		self.C = OrderedDict()
		self.di = set()
		self._sort()
		self._initPass()
		self._f1()
		#print (self.SC)
		k = 2
		while (True):
			if k == 2:
				self._level2CandidateGenSPM()
			elif k == 3:
				self._MSCandidateGenSPM(k)
			else:
				break
			for s in self.S:
				for c in self.C[k]:
					if self._contains(c.sequence,s):
						c.count += 1
			self._frequentSequence(k)
			k+=1

		#print (self.C.items())
		for item in self.C[3]:
		 	print ("{} --- {}".format(item.sequence,item.count))

	def _sort(self):
		self.M = OrderedDict(sorted(self.MS.items(),key=lambda t:t[1]))

	def _initPass(self):
		lMISItem = None
		lMIS = None
		isMatched = False

		self.SC = {item: sum([1 for sequence in self.S if sum(1 for itemset in sequence if item in itemset) > 0])/self.n for item in self.M}
		self.C = {item: sum([1 for sequence in self.S if sum(1 for itemset in sequence if item in itemset) > 0]) for item in self.M}

		for item, mis in self.M.items():
			if (not isMatched) and item in self.SC and self.SC[item] >= mis:
				isMatched = True
				lMISItem,lMIS = item,mis
				self.L.append(item)
			elif isMatched and item in self.SC and self.SC[item] >= lMIS:
				self.L.append(item)

	def _f1(self):
		F1 = {}
		for item in self.L:
			if self.SC[item] >= self.MS[item]:
				seq = Sequence([[item]],item,self.C[item]) 
				if seq not in F1:
					F1[seq] = seq
		self.F[1] = F1

	def _level2CandidateGenSPM(self):
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
	

	def _MSCandidateGenSPM(self,k):
		F = self.F[k-1]
		self.C[k] = []
		for s1 in F:
			if self._lowestMIS(s1.sequence,True,k):
				for s2 in F:
					self._ForwardCandidateGenSPM(s1,s2,True,k)
			else:
				for s2 in F:
					if self._lowestMIS(s2.sequence,False,k):
						self._ForwardCandidateGenSPM(s1,s2,False,k)
					else:
						idd = 2
						self._candidateGenSPM(s1,s2,k)
		#self._prune(k)

	def _lowestMIS(self,s,isFirst,k):
		x = 0 if isFirst else -1
		item = s[x][x]
		itemMIS = self.MS[item]
		sequence = enumerate(s) if isFirst else enumerate(reversed(s))
		for idx, iset in sequence:
			sIdx = 1 if idx == 0 else 0
			itemset = iset if isFirst else list(reversed(iset))
			for item in itemset[sIdx:]:
				if self.MS[item] <= itemMIS:
					return False
		return True

	def _ForwardCandidateGenSPM(self,seq1,seq2,isFirst,k):
		s1 = seq1.sequence if isFirst else [list(reversed(itemset)) for itemset in list(reversed(seq2.sequence))]
		s2 = seq2.sequence if isFirst else [list(reversed(itemset)) for itemset in list(reversed(seq1.sequence))]
		nseq1, nseq2 = None, None
		_s1, _s2 = copy.deepcopy(s1), copy.deepcopy(s2)
		fItemS1 = _s1[0][0]
		lItemS1 = _s1[-1][-1]
		lItemS2 = _s2[-1][-1]
		separate = True if len(_s2[-1]) == 1 else False
		sItemS1 = self._deleteItemFromSequence(_s1,_s2)
		if abs(self.MS[lItemS2] - self.MS[sItemS1]) > self.SDC:
			return;
		
		if self.MS[lItemS2] <= self.MS[fItemS1]:	# Condition 2
			return

		if self._sameSequence(_s1,_s2):
			minMISItem = seq1.minMISItem if self.MS[lItemS2] >= self.MS[seq1.minMISItem] else lItemS2
			cs1 = copy.deepcopy(s1)
			if separate:
				cs1.append([lItemS2])
				neq1 = self._newSequence(k,cs1,minMISItem,isFirst)
				if (((lItemS2 > lItemS1) and isFirst) or ((lItemS2 < lItemS1) and not isFirst)) and self._sameLengthSizeSequence(s1,1):
					cs2 = copy.deepcopy(s1)
					cs2[-1].append(lItemS2)
					nseq2 = self._newSequence(k,cs2,minMISItem,isFirst)
			elif ((((lItemS2 > lItemS1) and isFirst) or ((lItemS2 < lItemS1) and not isFirst)) and self._sameLengthSizeSequence(s1,2)) or self._sameLengthSizeSequence(s1,3):
				cs1 = copy.deepcopy(s1)
				cs1[-1].append(lItemS2)
				nseq1 = self._newSequence(k,cs1,minMISItem,isFirst)
		if nseq1:
			if nseq1 not in self.di:
				self.di.add(nseq1)
				self.C[k].append(nseq1)
		elif nseq2:
			if nseq2 not in self.di:
				self.di.add(nseq2)
				self.C[k].append(nseq2)

	def _newSequence(self,k,s,minMISItem,isFirst):
		sequence = Sequence(s,minMISItem) if isFirst else Sequence(self._reversedSequence(s),minMISItem)
		return sequence

	def _reversedSequence(self,s):
		return [list(reversed(itemset)) for itemset in list(reversed(s))]

	def _deleteItemFromSequence(self,_s1,_s2):
		sItemS1 = None

		del _s2[-1][-1]
		if len(_s2[-1]) == 0:
			del _s2[-1]

		if len(_s1) == 1:
			sItemS1 = _s1[0][1]
			del _s1[0][1]
			if len(_s1[0]) == 0:
				del _s1[0]
		else:
			if len(_s1[0]) > 1:
				sItemS1 = _s1[0][1]
				del _s1[0][1]
				if len(_s1[0]) == 0:
					del _s1[0]
			else:
				sItemS1 = _s1[1][0]
				del _s1[1][0]
				if len(_s1[1]) == 0:
					del _s1[1]
		return sItemS1

	def _sameLengthSizeSequence(self,s,typ):
		items = set()
		for itemset in s:
			for item in itemset:
				items.add(item)

		if (typ == 1):
			if len(items) == len(s):
				return True
			else:
				return False
		elif (typ == 2):
			if len(items) == 2 and len(s) == 1:
				return True
			else:
				return False
		elif typ == 3:
			if len(items) > 2:
				return True
			else:
				return False


	def _candidateGenSPM(self,seq1,seq2,k):
		s1, s2 = seq1.sequence, seq2.sequence
		_s1, _s2 = copy.deepcopy(s1), copy.deepcopy(s2)
		item = _s2[-1][-1]
		fItemS1 = _s1[0][0]

		if abs(self.MS[item] - self.MS[fItemS1]) > self.SDC:
			return;

		separate = True if len(_s2[-1]) == 1 else False
		del _s1[0][0]
		if len(_s1[0]) == 0:
			del _s1[0] 
		del _s2[-1][-1]
		if len(_s2[-1]) == 0:
			del _s2[-1]

		if self._sameSequence(_s1,_s2):
			cs1 = copy.deepcopy(s1)
			if separate:
				cs1.append([item])
			else:
				cs1[-1].append(item)
			minMISItem = seq1.minMISItem if self.MS[item] >= self.MS[seq1.minMISItem] else item 
			nseq1 = Sequence(cs1,minMISItem)
			if nseq1 not in self.di:
				self.di.add(nseq1)
				self.C[k].append(nseq1)

	def _sameSequence(self,s1,s2):
		if len(s1) != len (s2):
			return False
		for i in range(len(s1)):
			if len(s1[i]) != len(s2[i]):
				return False
			else:
				for j in range(len(s1[i])):
					if s1[i][j] != s2[i][j]:
						return False
		return True
		

	def _contains(self,c,s):
		#print ("{} ---- {}".format(c,s))
		sIdx = 0
		sSize = len(s)
		cSize = len(c)
		if cSize > sSize:
			return False

		for cIdx, cItemSet in enumerate(c):
			cRemSize = cSize - cIdx
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
		F = {}
		for c in self.C[k]:
			if c.count/self.n >= self.MS[c.minMISItem]:
				if c not in F:
					F[c] = c;
		self.F[k] = F



			







