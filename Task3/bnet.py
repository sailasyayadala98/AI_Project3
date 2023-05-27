import sys
import pandas as pd

# read text file
df = pd.read_fwf('training_data.txt', names=['B', 'G', 'C', 'F'])
k=len(df)

#calculating the B probability 
counts = df['B'].value_counts() # count the occurrences of each unique value in the 'B' column
prob_zero_b = counts[0] / k # divide the count of zeros by the total number of rows
prob_one_b = counts[1] / k # divide the count of ones by the total number of rows

#calculating C probability 
c_counts = df['C'].value_counts() # count the occurrences of each unique value in the 'C' column
prob_zero_c = c_counts[0] / k # divide the count of zeros by the total number of rows
prob_one_c = c_counts[1] / k # divide the count of ones by the total number of rows

#calculating conditional probability for B,G
# group the rows by values in column 'B'
grouped = df.groupby('B')

# loop over the groups and calculate the conditional probability for column 'G'
for b, group in grouped:
    counts = group['G'].value_counts() # count the occurrences of each unique value in column 'G' within the group
    total_count = counts.sum() # count the total number of values in column 'G' within the group
    prob_given_b = counts / total_count # divide the counts by the total count to get the conditional probability 
    if b == 0:
        prob_given_b0 = prob_given_b
    elif b == 1:
        prob_given_b1 = prob_given_b
# group the rows by values in columns 'G' and 'C'
grouped = df.groupby(['G', 'C'])

# loop over the groups and calculate the conditional probability for column 'F'
for (g, c), group in grouped:
    counts = group['F'].value_counts() # count the occurrences of each unique value in column 'F' within the group
    total_count = counts.sum() # count the total number of values in column 'F' within the group
    prob_given_gc = counts / total_count # divide the counts by the total count to get the conditional probability
    if g == 0 and c == 1:
        prob_given_g0_c1 = prob_given_gc
    elif g == 1 and c == 0:
        prob_given_g1_c0 = prob_given_gc
    elif g==0 and c==0:
      prob_given_g0_c0 = prob_given_gc 
    elif g==1 and c==1:
      prob_given_g1_c1 = prob_given_gc 

# Defining the class called BayesianNetwork
class BayesianNetwork:
    
    # Function definition of the constructor
    def __init__(self):
        
        # Probability values taken from the table given
        self.P_Bt = prob_one_b
        self.P_Ct = prob_one_c
        self.P_Gt_given_Bt = prob_given_b1[1]
        self.P_Gt_given_Bf = prob_given_b0[1]
        self.P_Ft_given_Gt_Ct = prob_given_g1_c1[1]
        self.P_Ft_given_Gf_Ct = prob_given_g0_c1[1]
        self.P_Ft_given_Gt_Cf = prob_given_g1_c0[1]
        self.P_Ft_given_Gf_Cf = prob_given_g0_c0[1]
        
    def computeProbability(self, B, G, C, F):
        product = 1
        
        if not B:
            product = product * (1 - self.P_Bt)
        else:
            product = product * self.P_Bt
            
        if not C:
            product = product * (1 - self.P_Ct)
        else:
            product = product * self.P_Ct
            
        if B:   
            if G:
                product = product * self.P_Gt_given_Bt
            else:
                product = product * (1 - self.P_Gt_given_Bt)
        else:
            if G:
                product = product * self.P_Gt_given_Bf
            else:
                product = product * (1 - self.P_Gt_given_Bf)
        
        if G and C:
            if F:
                product = product * self.P_Ft_given_Gt_Ct
            else:
                product = product * (1 - self.P_Ft_given_Gt_Ct)
        elif G and not C:
            if F:
                product = product * self.P_Ft_given_Gt_Cf
            else:
                product = product * (1 - self.P_Ft_given_Gt_Cf)
        elif not G and C:
            if F:
                product = product * self.P_Ft_given_Gf_Ct
            else:
                product = product * (1 - self.P_Ft_given_Gf_Ct)
        else:
            if F:
                product = product * self.P_Ft_given_Gf_Cf
            else:
                product = product * (1 - self.P_Ft_given_Gf_Cf)
							
        return product
	
    def iterateProbability(self, flag):
        result = 0
        
        for B in [True, False]:
            for G in [True, False]:
                for C in [True, False]:
                    for F in [True, False]:
                        if (B and flag[0] != 0) or (not B and flag[0] != 1):
                            if (G and flag[1] != 0) or (not G and flag[1] != 1):
                                if (C and flag[2] != 0) or (not C and flag[2] != 1):
                                    if (F and flag[3] != 0) or (not F and flag[3] != 1):
                                        result = result + self.computeProbability(B, G, C, F)
        return result

def processip(flagAr,varId,truthVal):
	if varId == 'B':
		if truthVal:
			flagAr[0] = 1
		else:
			flagAr[0] = 0
	elif varId == 'G':
		if truthVal:
			flagAr[1] = 1
		else:
			flagAr[1] = 0
	elif varId == 'C':
		if truthVal:
			flagAr[2] = 1
		else:
			flagAr[2] = 0
	elif varId == 'F':
		if truthVal:
			flagAr[3] = 1
		else:
			flagAr[3] = 0
	else:
		print ('This code should not be reachable. Invalid Variable to be ignored: ', varId)
	return flagAr

def combineFlags(qFlag,eFlag):
	#combines flags of query and evidence variable to form flags for numerator part of condl prob calculation
	rFlag = [-1, -1, -1, -1]
	err = False
	for i in range(4):
		if eFlag[i] == -1:
			rFlag[i] = qFlag[i]
		else:
			if qFlag[i] == -1:
				rFlag[i] = eFlag[i]
			else:
				if eFlag[i] == qFlag[i]:
					rFlag[i] = qFlag[i]
				else:
					#Same variable in both query and evidence with differing truth values. Result should be 0.0
					err = True
	if not err:
		return rFlag
	else:
		return -1


def main():
    out= BayesianNetwork()
    b = BayesianNetwork()
    query = [-1, -1, -1, -1] #flags for query variables. contains +1 if var is true, 0 if var is false and -1 if var is not present
    evide = [-1, -1, -1, -1] #flags for evidence variables
    evFlag = False	
    if len(sys.argv) >=5 :
        for i in range(2,len(sys.argv)):
            if sys.argv[i] == 'given':
              evFlag = True
            else:
                if sys.argv[i][1] == 't':
                   if evFlag:
                        evide = processip(evide, sys.argv[i][0], True)
                   else:
                        query = processip(query, sys.argv[i][0], True)
                elif sys.argv[i][1] == 'f':
                   if evFlag:
                        evide = processip(evide, sys.argv[i][0], False)
                   else:
                        query = processip(query,sys.argv[i][0], False)
                else:
                    print ('This code should not be reachable. Ignoring invalid entry: ', sys.argv[i]) 
    else :
         evFlag = True
    if not evFlag:
        print (b.iterateProbability(query))
    else:
        numerator = combineFlags(query,evide)
    if numerator != -1:#check for error condition
        print (b.iterateProbability(numerator)/b.iterateProbability(evide))
    else:
        print (0.0)

if __name__ == "__main__":
    main()