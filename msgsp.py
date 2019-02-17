from collections import OrderedDict
from utils import Sequence, sameSequence, deleteItemFromSequence, sameLengthSizeSequence, reversedSequence
import copy

class MSGsp:
	def __init__(self,S,MS,n,SDC):
		self.S        = S		# Data Sequences
		self.MS       = MS		# Minimum Suupport of items
		self.n        = n		# Total number of unique items
		self.SDC      = SDC		# User defined Support Difference Constraint
		self.M        = None	# Items sorted according to Min. Item Support stored in MS
		self.L        = []		# seeds set for generating the set of candidate sequences of length 2
		self.SC       = {}		# Actual support count of items from given data
		self.di       = {}		# Dictionary for candidate sequence duplicate check
		self.Count    = {}
		self.F        = OrderedDict()	# Frequent k-Sequences
		self.C        = OrderedDict()	# Candidate k-Sequences
		self.filename = "results.txt"	# Output File

		self._msgsp()	# Calls the MS-GSP algorithm
		self._outputResult()	# Writes data to output file

	def _msgsp(self):
		k = 2	# k initialized to 2-length sequence	
		self._sort()								
		self._initPass()
		self._f1()
	
		while (True):
			print ("Generating {} - Sequence".format(k))
			if k == 2:
				self._level2CandidateGenSPM()
			else:
				self._MSCandidateGenSPM(k)

			for s in self.S:
				for c in self.C[k]:
					if c.contained(s):
						c.count += 1
					cc = copy.deepcopy(c)
					cc.removeElement(cc.minMISItem)
					if cc.contained(s):
						if cc in self.di:
							self.di[cc].count += 1

			self._frequentSequence(k)
			if len(self.F[k]) == 0:
				break
			k+=1

	def _sort(self):
		"""Sort items according to Min. Support"""
		print ("Sort")
		self.M = OrderedDict(sorted(self.MS.items(),key=lambda t:t[1]))

	def _initPass(self):
		"""First pass over S
		
		   Produces seed set L for generating C2 and recods support count of items.
		"""
		print ("Init Pass")
		lMISItem  = None	#? unused
		lMIS      = None
		isMatched = False

		self.SC = {item: sum([1 for sequence in self.S if sum(1 for itemset in sequence if item in itemset) > 0])/self.n for item in self.M}
		self.Count = {item: sum([1 for sequence in self.S if sum(1 for itemset in sequence if item in itemset) > 0]) for item in self.M}   #? why count twice

		for item, mis in self.M.items():
			if (not isMatched) and item in self.SC and self.SC[item] >= mis:
				isMatched = True
				lMISItem,lMIS = item,mis
				self.L.append(item)
			elif isMatched and item in self.SC and self.SC[item] >= lMIS:
				self.L.append(item)

	def _f1(self):
		"""Generates Frequent 1-sequences (F1)"""
		F1 = {}
		for item in self.L:
			if self.SC[item] >= self.MS[item]:
				seq = Sequence([[item]],item,self.Count[item]) 
				if seq not in F1:
					F1[seq] = seq
		self.F[1] = F1

	def _level2CandidateGenSPM(self):
		"""Generates candidate 2-sequences (C2)"""
		print ("Level2 Candidate Generation")
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
		"""Generates candidate k-sequences (k>2)"""
		print ("MS Candidate Generation for : {}".format(k))
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
						self._candidateGenSPM(s1,s2,k)
		self._prune(k)

	def _ForwardCandidateGenSPM(self,seq1,seq2,isFirst,k):
		"""Generates candidate sequence for conditions where MIS of first item of first sequence or MIS of last sequence of S2 is less than MIS of other items in candidate generation loop
		
		Args:
			seq1: first sequence
			seq2: second sequence
			isFirst: True/False indicates whether first or second case in above description
			k: k in k-sequence
		"""
		s1 = seq1.sequence if isFirst else [list(reversed(itemset)) for itemset in list(reversed(seq2.sequence))]
		s2 = seq2.sequence if isFirst else [list(reversed(itemset)) for itemset in list(reversed(seq1.sequence))]
		nseq1, nseq2 = None, None
		_s1, _s2 = copy.deepcopy(s1), copy.deepcopy(s2)
		fItemS1  = _s1[0][0]
		lItemS1  = _s1[-1][-1]
		lItemS2  = _s2[-1][-1]
		separate = True if len(_s2[-1]) == 1 else False							# indicated whether last (or first) item in s2 (or s1) is a separate 1-itemset
		sItemS1  = deleteItemFromSequence(_s1,_s2)
		if abs(self.SC[lItemS2] - self.SC[sItemS1]) > self.SDC:
			return
		
		if self.MS[lItemS2] < self.MS[fItemS1]:	# Condition 2
			return

		if sameSequence(_s1,_s2):
			
			minMISItem = seq1.minMISItem if self.MS[lItemS2] >= self.MS[seq1.minMISItem] else lItemS2
			cs1 = copy.deepcopy(s1)
			if separate:
				cs1.append([lItemS2])
				nseq1 = self._newSequence(k,cs1,minMISItem,isFirst)
				if (((lItemS2 > lItemS1) and isFirst) or ((lItemS2 < lItemS1) and not isFirst)) and sameLengthSizeSequence(s1,1):
					cs2 = copy.deepcopy(s1)
					cs2[-1].append(lItemS2)
					nseq2 = self._newSequence(k,cs2,minMISItem,isFirst)
			elif ((((lItemS2 > lItemS1) and isFirst) or ((lItemS2 < lItemS1) and not isFirst)) and sameLengthSizeSequence(s1,2)) or sameLengthSizeSequence(s1,3):
				cs1 = copy.deepcopy(s1)
				cs1[-1].append(lItemS2)
				nseq1 = self._newSequence(k,cs1,minMISItem,isFirst)
		if nseq1:
			if nseq1 not in self.di:
				self.di[nseq1] = nseq1
				self.C[k].append(nseq1)
		if nseq2:
			if nseq2 not in self.di:
				self.di[nseq2] = nseq2
				self.C[k].append(nseq2)

	def _lowestMIS(self,s,isFirst,k):
		"""Generates lowest MIS Item
		
		Args:
			s: sequence to find lowest MIS
			isFirst: True/False determines whether to check first or last item for lowest MIS
			k: k in k-sequence
		"""
		x        = 0 if isFirst else -1
		item     = s[x][x]
		itemMIS  = self.MS[item]
		sequence = enumerate(s) if isFirst else enumerate(reversed(s))
		for idx, iset in sequence:
			sIdx    = 1 if idx == 0 else 0
			itemset = iset if isFirst else list(reversed(iset))
			for item in itemset[sIdx:]:
				if self.MS[item] <= itemMIS:
					return False
		return True

	def _newSequence(self,k,s,minMISItem,isFirst):
		"""Generates candidate sequence for conditions where MIS of first item of first sequence or MIS of last sequence of S2 is less than MIS of other items  in candidate generation loop
		
		Args:
			k: k in k-sequence
			s: sequence
			minMISItem: item with lowest MIS
			isFirst: True/False indicates whether first or second case in above description
		"""		
		sequence = Sequence(s,minMISItem) if isFirst else Sequence(reversedSequence(s),minMISItem)
		return sequence

	def _candidateGenSPM(self,seq1,seq2,k):
		"""Generates candidate sequence for else condition in candidate generation loop
		
		Args:
			seq1: first sequence
			seq2: second sequence
			k: k in k-sequence
		"""
		s1, s2   = seq1.sequence, seq2.sequence
		_s1, _s2 = copy.deepcopy(s1), copy.deepcopy(s2)
		item     = _s2[-1][-1]
		fItemS1  = _s1[0][0]
		if abs(self.SC[item] - self.SC[fItemS1]) > self.SDC:
			return

		separate = True if len(_s2[-1]) == 1 else False
		del _s1[0][0]
		if len(_s1[0]) == 0:
			del _s1[0] 
		del _s2[-1][-1]
		if len(_s2[-1]) == 0:
			del _s2[-1]

		if sameSequence(_s1,_s2):
			cs1 = copy.deepcopy(s1)
			if separate:
				cs1.append([item])
			else:
				cs1[-1].append(item)
			minMISItem = seq1.minMISItem if self.MS[item] >= self.MS[seq1.minMISItem] else item 
			nseq1 = Sequence(cs1,minMISItem)
			if nseq1 not in self.di:
				self.di[nseq1] = nseq1
				self.C[k].append(nseq1)

	def _frequentSequence(self,k):
		"""Generates set Fk of frequent k-sequences from Ck
		
		Args:
			k: k in k-sequence
		"""
		F = {}
		for c in self.C[k]:
			if c.count/self.n >= self.MS[c.minMISItem]:
				if c not in F:
					F[c] = c
		self.F[k] = F

	def _prune(self,k):
		"""Prunes k sequences from Ck
		
		Args:
			k: k in k-sequence
		"""
		toRemove = []
		for idx, c in enumerate(self.C[k]):
			if not self._allFrequentk_1(c,k):
				toRemove.append(c)
				del self.di[c]
		for c in toRemove:
		 	self.C[k].remove(c)
	
	def _allFrequentk_1(self,c,k):
		"""Returns True/False conditioned on whether k-1 sequences (except subsequence formed by removing item with strictly lowest MIS value) are frequent
		
		Args:
			c: candidate sequence for which to extract k-1 frequent sequences
			k: k in k-sequence
		"""
		for i, itemset in enumerate(c.sequence):
			for j, item in enumerate(itemset):
				if item == c.minMISItem and c.minMISItemCount == 1:
					continue
				cc = copy.deepcopy(c.sequence)
				del cc[i][j]
				if len(cc[i]) == 0:
					del cc[i]
				if Sequence(cc,0) not in self.F[k-1]:
					return False
		return True

	def _outputResult(self):
		"""Write frequent k-sequences generated into output file"""
		fp = open(self.filename,"w")
		for k,fk in self.F.items():
			if (len(fk)>0):
				fp.write("\nNumber of Length {} Frequency Sequences: {}\n".format(k,len(fk)))
				for item in fk:
					fp.write('{} Count: {}\n'.format(item.string(),item.count))
