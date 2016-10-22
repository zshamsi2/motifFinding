import random
import time
import numpy as np
import math

ITERATIONS=2000
nuc = ['A','G','T','C']
freq = [0.25,0.25,0.25,0.25]

def getPWM(sequences,N,W,L):
	## Generate random number from 0,SC for the sequence to be ignored
	random.seed(time.time())
	z=random.randrange(0,N)
	## Generate motif site for the N-1 sequences
	sites=[]
	for i in range(0,N-1):
		k=random.randrange(0,L-W)
		sites.append(k)
	## Calculate PWM
	PWM=np.zeros((4,W))
	count=0 ## count goes from 0,N-1
	for i in range(0,N):
		if (i==z):
			continue;
		else:
			for j in range(0,W):
				if (sequences[i][sites[count]+j]==nuc[0]):
					PWM[0][j]+=1
				elif (sequences[i][sites[count]+j]==nuc[1]):
					PWM[1][j]+=1
				elif (sequences[i][sites[count]+j]==nuc[2]):
					PWM[2][j]+=1
				elif (sequences[i][sites[count]+j]==nuc[3]):
					PWM[3][j]+=1
		count+=1
	return PWM/(N-1),z,sites

def getOdds(PWM,z,sequences,W,L):
	candidates_seq=[]
	for i in range(0,L-W+1):
		candidates_seq.append(sequences[z][i:i+W])
	candidates_odds=[]
	for i in range(0,len(candidates_seq)):
		P=1
		Q=1
		for j in range(0,W):
			if (candidates_seq[i][j]==nuc[0]):
				P*=freq[0]
				Q*=PWM[0][j]
			elif (candidates_seq[i][j]==nuc[1]):
				P*=freq[1]
				Q*=PWM[1][j]
			elif (candidates_seq[i][j]==nuc[2]):
				P*=freq[2]
				Q*=PWM[2][j]
			elif (candidates_seq[i][j]==nuc[3]):
				P*=freq[3]
				Q*=PWM[3][j]
		candidates_odds.append(Q/P)
	normed_odds=candidates_odds/sum(candidates_odds)
	random.seed(time.time())
	x = random.random()
	index = 0
	while(x >= 0 and index 	< len(normed_odds)):
		x -= normed_odds[index]
		index += 1
	return index-1	## This is the position in the z sequence which is chosen proportional to the odds
			
def getIC(sites,sequences,W,N,old_PWM):
	## Calculate new PWM
	new_PWM=np.zeros((4,W))
	count=0 ## count goes from 0,N
	for i in range(0,N):
		for j in range(0,W):
			if (sequences[i][sites[count]+j]==nuc[0]):
				new_PWM[0][j]+=1
			elif (sequences[i][sites[count]+j]==nuc[1]):
				new_PWM[1][j]+=1
			elif (sequences[i][sites[count]+j]==nuc[2]):
				new_PWM[2][j]+=1
			elif (sequences[i][sites[count]+j]==nuc[3]):
				new_PWM[3][j]+=1
		count+=1
	PWM=new_PWM/(N)
	IC=0
	for i in range(0,W):
		for j in range(0,4):	## 4 nucleotides
			if (j==0):
				temp=PWM[j][i]/freq[0]
			elif (j==1):
				temp=PWM[j][i]/freq[1]
			elif (j==2):
				temp=PWM[j][i]/freq[2]
			elif (j==3):
				temp=PWM[j][i]/freq[3]
			if (temp==0):
				continue;
			IC+=PWM[j][i]*math.log(temp,2)
	return IC,PWM

if __name__ == "__main__":
	f_motiflength=open('motiflength.txt','rb')
	for line in f_motiflength:
		W=int(line)	## motiflength
	f_motiflength.close()
	f_sequences=open('sequences.fa','rb')
	sequences=[]
	flag=0
	for line in f_sequences:
		if (flag==0):
			flag=1
		elif (flag==1):
			flag=0
			sequences.append(line.strip('\n'))
	f_sequences.close()	
	N=len(sequences)	## Number of sequences
	L=len(sequences[0])	## Length of sequences, assumed all are of same length)
	info=[['IC'],['sites']]
	for ITER in range(0,ITERATIONS):
		## Calculate PWM for N-1 sequences
		PWM,z,sites=getPWM(sequences,N,W,L)
		## Predict the site in the ignored sequence
		z_site=getOdds(PWM,z,sequences,W,L)
		sites.insert(z,z_site)
		## Calculate information content in the current iteration prediction
		IC,PWM=getIC(sites,sequences,W,N,PWM)
		## Save information for analysis
		info[0].append(IC)
		info[1].append(sites)
	info[1][info[0].index(max(info[0][1:]))]
