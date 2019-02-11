from parser import Parser
from msgsp import MSGsp

parser = Parser("para1-1.txt","data-1.txt")
parser.parse()
msGSP = MSGsp(parser.S,parser.MS,parser.n,parser.SDC)