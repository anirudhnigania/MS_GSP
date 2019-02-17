import uuid

class Sequence:
	def __init__ (self,l,minMISItem,count=0):
		self.sequence        = l
		self.count           = count
		self.minMISItem      = minMISItem
		tup                  = tuple([tuple(itemset) for itemset in self.sequence])
		self.uid             = hash(tup)
		self.minMISItemCount = sum([1 for itemset in self.sequence for item in itemset if item == minMISItem])


	def reverse(self):
		return [list(reversed(itemset)) for itemset in list(reversed(self.sequence))]

	def __eq__ (self, other):
		return self.uid == other.uid

	def __hash__(self):
		return self.uid

	def contained(self,s):
		sIdx  = 0
		sSize = len(s) 
		cSize = len(self.sequence)
		if cSize > sSize:
			return False

		for cIdx, cItemSet in enumerate(self.sequence):
			cRemSize = cSize - cIdx
			while sIdx < sSize and not self._subSequence(cItemSet,s[sIdx]):
				sIdx += 1
				if (sSize - sIdx) < cRemSize:
					return False
			sIdx += 1
		return True

	def _subSequence(self,c,s):
		for cIdx, cItem in enumerate(c):
			if cItem not in s:
				return False
		return True

	def string(self):
		return '<{' + '}{'.join(', '.join(map(str,sl)) for sl in self.sequence) + '}>'

def reversedSequence(s):
		return [list(reversed(itemset)) for itemset in list(reversed(s))]

def sameSequence(s1,s2):
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

def deleteItemFromSequence(_s1,_s2):
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

def sameLengthSizeSequence(s,typ):
		items = list()
		for itemset in s:
			for item in itemset:
				items.append(item)

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
