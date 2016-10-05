import sys

## Constants
#Frequencies of A, G, T, C
freq = [0.25,0.25,0.25,0.25]


if __name__ == "__main__":
	## Inputs
	if (len(sys.argv)>0 and len(sys.argv)<5):
		print "Command line usage: python benchmark.py <ICPC> <ML> <SL> <SC>"
		print "Information content per column (ICPC):",
		ICPC = int(raw_input())
		print "motif lenght (ML):",
		ML = int(raw_input())
		print "sequence length (SL):",
		SL = int(raw_input())
		print "sequence count (SC):",
		SC = int(raw_input())
	else:
		ICPC = int(sys.argv[1])
		ML = int(sys.argv[2])
		SL = int(sys.argv[3])
		SC = int(sys.argv[4])
	sum_freq=sum(freq)
	if sum_freq != 1:
		raise Exception, 'Sum of frequency of nucleotides is not 1.'
	if (ICPC<=0 or ML<=0 or SL<=0 or SC<=0):
		raise Exception, 'Incorrect input values.'
		
	
#	sum = [freq[i] for i in range(0,len(freq))]
#	print ICPC
#	print ML
#	print SL
#	print SC
