import re

class Parser:
	def __init__ (self,parameterFileName,dataFileName):
		self.parameterFile = parameterFileName
		self.dataFile = dataFileName
		self.MS = {}
		self.SDC = None
		self.S = []
		self.n = 0

	def parse(self):
		self._parseParameterFile()
		self._parseDataFile()

	def _parseParameterFile (self):
		file = open(self.parameterFile,"r")
		lines = file.readlines()

		for line in lines: 
			if (re.search("MIS*",line)):
				item = int(line.split('(')[1].split(')')[0])
				mis = float(line.split('=')[1].strip())
				self.MS[item] = mis
			elif (re.search("SDC*",line)):
				self.SDC = float(line.split('=')[1].strip())
		file.close()

	def _parseDataFile (self):
		file = open(self.dataFile,"r")
		lines = file.readlines()
		lines = [line.strip()[1:-1].replace(" ", "") for line in lines]

		for line in lines:
			sequence = [[int(a) for a in itemset[0:-1].split(',')] if "," in itemset else [int(itemset[0:-1])] 
															for itemset in line.split('{') if len(itemset) > 0]
			self.n+= len(sequence)
			self.S.append(sequence)

		file.close()