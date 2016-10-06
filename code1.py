import sys
import random
import time

## Constants
nuc = ['A','G','T','C']
freq = [0.25,0.25,0.25,0.25]
filename='uniform_bg_ICPC_to_p.txt'

def generate_seq(SL):
	seq=[]
	random.seed(time.time())
	for i in range(0,SL):
		x=random.random()
		if (x<freq[0]):
			seq.append(nuc[0])
		elif (x<freq[0]+freq[1]):
			seq.append(nuc[1])
		elif (x<freq[0]+freq[1]+freq[2]):
			seq.append(nuc[2])
		else:
			seq.append(nuc[3])
	return ''.join(seq)

if __name__ == "__main__":
	## Inputs
	if (len(sys.argv)>0 and len(sys.argv)<5):
		print "Command line usage: python benchmark.py <ICPC> <ML> <SL> <SC>"
		print "Information content per column (ICPC):",
		ICPC = float(raw_input())
		print "motif lenght (ML):",
		ML = int(raw_input())
		print "sequence length (SL):",
		SL = int(raw_input())
		print "sequence count (SC):",
		SC = int(raw_input())
	else:
		ICPC = float(sys.argv[1])
		ML = int(sys.argv[2])
		SL = int(sys.argv[3])
		SC = int(sys.argv[4])
	sum_freq=sum(freq)
	if sum_freq != 1:
		raise Exception, 'Sum of frequency of nucleotides is not 1.'
	if (ICPC<=0 or ML<=0 or SL<=0 or SC<=0):
		raise Exception, 'Incorrect input values.'
	## Generate SC random sequences of length SL and store in list, seqs
	seqs=[]
	for i in range(0,SC):
		temp=generate_seq(SL)
		seqs.append(temp)		
#	sum = [freq[i] for i in range(0,len(freq))]
#	print ICPC
#	print ML
#	print SL
#	print SC
#	print seqs
	## Read ICPC to p mapping
	f=open(filename,'rb')
	icpc_to_p=[]
	flag=0
	for line in f:
		if (flag==0):
			flag=1
			continue;
		temp=line.strip().split()
		temp = [float(x) for x in temp]
		icpc_to_p.append(temp)
	
