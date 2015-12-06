import re
import random
import sys
import getopt
import time

WORDNUM_DEFAULT=300
NUM_TEXT_DEFAULT=10
FILENAME_DEFAULT="frank10.txt"
OUTPUT_FILENAME_DEFAULT="resultado_"+str(time.time())+".txt"


HELP_MESSAGE='markov.py -i <inputfile>  -w <wordnum> -n <textnum>'

###### HELPER FUNCTIONS #######################


def wordcount(string):
	content_0=string.lower()
	content_1 = re.sub('\s+', ' ', content_0)
	content_2 = re.sub('[^A-Za-z ]+', '', content_1)
	words = content_2.split()
	return words

def generate_text(seed,word_count,transition_matrix,wordbag):
	text=[]
	for i in range(0,word_count):		
		if i==0:
			word=next_state(seed,transition_matrix,wordbag)
			text=text+[seed]+[" "]
		else: 
			word=next_state(current_state,transition_matrix,wordbag)
		current_state=word
		text=text+[word]+["  "]
	return "".join(text)
	
def generate_seed(wordbag):
	zero_state_index=random.randint(0,len(wordbag)-1)
	j=0
	for word in wordbag:
		zero_state=word
		j+=1
		if zero_state_index==j:
			break;
	return zero_state
	
		
def next_state(current_state,transition_matrix,wordbag):
	value=random.randint(0,1)
	prob_vector={}
	cum_prob_vector={}
	for x1,x2 in transition_matrix:
		if current_state==x1:
			prob_vector[x2]=transition_matrix[(x1,x2)]
	cum_sum=0.0
	if len(prob_vector)==0:
		return generate_seed(wordbag)
	
	##### THIS CAN BE IMPROVED ##########################
	
	for x in prob_vector:
		cum_prob_vector[x]=cum_sum
		cum_sum+=prob_vector[x]
	
	for x in cum_prob_vector:
		cum_prob_vector[x]=cum_prob_vector[x]/cum_sum
	
	for x in cum_prob_vector:
		if cum_prob_vector[x]>=value:
			return x
	return x

	
def main(argv):
	
	###### PROGRAM INGRESS ###################
	FILENAME = FILENAME_DEFAULT
	WORDNUM = WORDNUM_DEFAULT
	NUM_TEXT= NUM_TEXT_DEFAULT
	OUTPUT_FILENAME= OUTPUT_FILENAME_DEFAULT 
	
	try:
		opts, args = getopt.getopt(argv,"hi:w:n:o:",["ifile=","wordnum=","textnum=","ofile="])
	except getopt.GetoptError:
		print HELP_MESSAGE
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print HELP_MESSAGE
			sys.exit()
		elif opt in ("-i", "--ifile"):
			FILENAME = arg
		elif opt in ("-w", "--wordnum"):
			WORDNUM= int(arg)
		elif opt in ("-n", "--textnum"):
			NUM_TEXT= int(arg)
		elif opt in ("-o", "--ofile"):
			OUTPUT_FILENAME= arg
	
	##### MAIN BODY OF PROGRAM ################
	dictionary=open(FILENAME,'r')
	wordbag={}
	sum_vector={}
	transition_matrix={}
	for line in dictionary:
		words=wordcount(line)
		for word in words:
			if word not in wordbag:
				wordbag[word]=1
				sum_vector[word]=1
			else:
				sum_vector[word]+=1
	dictionary.close()
	dictionary=open(FILENAME,'r')
	for line in dictionary:
		words=wordcount(line)
		for i in range(0,len(words)-1):
			transition=(words[i],words[i+1])
			if transition not in transition_matrix:
				transition_matrix[transition]=1
			else:
				transition_matrix[transition]+=1
	dictionary.close()

	for x1,x2 in transition_matrix:
		if x1 in wordbag:
			transition_matrix[(x1,x2)]=float(transition_matrix[(x1,x2)])/float(sum_vector[x1])

	######## OUTPUT OF THE PROGRAM #######################
	ofile=open(OUTPUT_FILENAME,"w")
	for i in range(0,NUM_TEXT):
		ofile.write(generate_text(generate_seed(wordbag),WORDNUM,transition_matrix,wordbag))
		ofile.write('\n')
		
	ofile.close()
			
	
if __name__=="__main__":
	main(sys.argv[1:])
	
	