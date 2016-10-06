import sys
import random
import time

## Constants
nuc = ['A','G','T','C']
freq = [0.25,0.25,0.25,0.25]
filename='uniform_bg_ICPC_to_p.txt'

def generate_seq(SL,freq):
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
		print "Command line usage: python benchmark.py <ICPC -- value [0,2] with maximum 2 significant digits> <ML -- positive integer> <SL -- postive integer> <SC --positive integer>"
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
	if (ICPC<0 or ICPC>2 or ML<=0 or SL<=0 or SC<=0 or len(str(ICPC))>4):
		raise Exception, 'Incorrect input values.\n<ICPC -- value [0,2] with maximum 2 significant digits> <ML -- positive integer> <SL -- postive integer> <SC --positive integer>'
	## Generate SC random sequences of length SL and store in list, seqs
	seqs=[]
	for i in range(0,SC):
		temp=generate_seq(SL,freq)
		seqs.append(temp)		
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
	for i in range(0,len(icpc_to_p)):
		if (ICPC==icpc_to_p[i][0]):
			p=icpc_to_p[i][1]
	q=(1-p)/3.0
	## Generate a random motif
	random_motif=generate_seq(ML,freq)
	## Generate SC motifs of length ML
#	A,G,T,C
	motifs_temp=[]
	for i in range(0,ML):
		motif_freq=[q,q,q,q]
		for j in range(0,len(nuc)):
			if(random_motif[i]==nuc[j]):
				motif_freq[j]=p
		temp=generate_seq(SC,motif_freq)
		motifs_temp.append(temp)
	motifs=[]
	for i in range(0,SC):
		temp=[]
		for j in range(0,ML):
			temp.append(motifs_temp[j][i])
		motifs.append(''.join(temp))
	## Planting motifs in seqs
