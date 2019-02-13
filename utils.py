import uuid

class Sequence:
	def __init__ (self,l,minMISItem,count=0):
		self.sequence = l
		self.count = count
		self.minMISItem = minMISItem
		tup = tuple([tuple(itemset) for itemset in self.sequence])
		self.uid = hash(tup)
		self.minMISItemCount = sum([1 for itemset in self.sequence for item in itemset if item == minMISItem])


	def reverse(self):
		return [list(reversed(itemset)) for itemset in list(reversed(self.sequence))]

	def __eq__ (self, other):
		return self.uid == other.uid

	def __hash__(self):
		return self.uid