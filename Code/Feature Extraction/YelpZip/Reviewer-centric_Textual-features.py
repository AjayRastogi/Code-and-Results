#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
from nltk import word_tokenize    
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import xlrd
import math
from xlrd import open_workbook
import numpy as np
from numpy.lib.stride_tricks import as_strided
import re
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('sentiwordnet')
from nltk import pos_tag
from nltk.corpus import stopwords
import nltk.tokenize.punkt
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
import time
from datetime import datetime
import pandas as pd

#...
book = open_workbook("Data\\YelpZip\\ReviewContent (Sortedby_Reviewer_wise).xlsx")			# Change the path according to the file location
sheet = book.sheet_by_index(0) 
#print(sheet.nrows)
rid = []
pid = []
date = []
text =[]
count = []
for row in range(1, sheet.nrows): #start from 1, to leave out row 0
	rid.append(int(sheet.cell(row, 0).value))
	pid.append(int(sheet.cell(row, 1).value))
	date.append(int(sheet.cell(row, 2).value))
	text.append(sheet.cell(row, 3).value)
	count.append(int(sheet.cell(row, 4).value))
#print(len(text))

MCS = []
ACS_TFIDF_BIGRAM = []
ARL=[]
AFPP=[]
ASPP=[]
AFTAPP=[]
ASAPP=[]
ASW = []
AOW = []
AInW = []
AImW = []

def MCS_unigram_ACS_TFIDF_bigram_ARL_AFPP_ASPP_AFTAPP_ASAPP_ASW_AOW_AImW_AInW():
	stemmer1 = SnowballStemmer("english")
	regex = re.compile('[%s]' % re.escape(string.punctuation))
	RL = []
	F_P = []
	S_P = []
	T_P = []     
	RFP_wrt_SP = []
	RSP_wrt_FP = []
	RFPTP_wrt_SP = []
	RSP_wrt_FPTP = []
	OBJ = []
	SUB = []
	tag = ['PRP', 'PRP$', 'WP', 'WP$',':','.','\'\'','CC', 'CD', 'DT', 'EX', 'FW', 'IN','LS','MD','POS', 'TO', 'UH', 'PDT', 'SYM', 'RP']
	noun = ['NN', 'NNS', 'NNP', 'NNPS']
	adj = ['JJ', 'JJR', 'JJS']
	verb = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
	adverb = ['RB', 'RBR', 'RBS', 'WRB']   
	RSW = []
	ROW = []
	N_A = []
	V_A = []  
	RInW = []
	RImW = []
	temp_rtext = []

	i=0
	while (i < len(rid)):
		#print(i)
		j = count[i] + i
		for k in range(i,j):
			pre_text = re.sub(r'[^\x00-\x7F]+',' ', text[k])				#replacing non-ascii characters with a space
			rl = len(pre_text.split())
			RL.append(rl)
			pre_text = re.sub('[^a-zA-Z0-9-_ \']', ' ', pre_text)
			pre_text = pre_text.replace(' i ', ' I ')
			pre_text = pre_text.replace('i ', 'I ')
			pre_text = pre_text.replace(' i\'', ' I\'')
			temp_rtext.append(" ".join(stemmer1.stem(word) for word in pre_text.split(" ")))
			for word, pos in pos_tag(word_tokenize(pre_text)):
				# RFPP, RSPP, RFTAPP, RSAPP ............................
				if (pos in ['PRP', 'PRP$']) and (word.lower() in ['i','me','my','mine','we','our','us','ours','myself','ourselves']):
					F_P.append(word.lower())
				elif (pos in ['PRP', 'PRP$']) and (word.lower() in ['you','your','yours','yourself','yourselves']):
					S_P.append(word.lower())
				elif (pos in ['PRP', 'PRP$']) and (word.lower() in ['he','she','it','his','her','him','its','hisself','herself','himself','itself','hers','they','their','them','theirs','themself','themselves']):
					T_P.append(word.lower())
				# RSW, ROW ..............................................
				if not pos in tag:
					if pos in noun:
						wn_tag = wn.NOUN
					elif pos in adj:
						wn_tag = wn.ADJ
					elif pos in verb:
						wn_tag = wn.VERB
					elif pos in adverb:
						wn_tag = wn.ADV
					else:
						wn_tag = 'None'
					if wn_tag == 'None' :
						synset = list(swn.senti_synsets(word))
						if len(list(synset)) != 0:
							syn_score = synset[0]
							if float(syn_score.obj_score()) > float(0.5):
								OBJ.append(word)
							elif float(float(syn_score.pos_score()) + float(syn_score.neg_score())) > float(0.5):
								SUB.append(word)
					else:
						synset = list(swn.senti_synsets(word, wn_tag))
						if len(list(synset)) != 0:
							syn_score = synset[0]
							if float(syn_score.obj_score()) > float(0.5):
								OBJ.append(word)
							elif float(float(syn_score.pos_score()) + float(syn_score.neg_score())) > float(0.5):
								SUB.append(word)
				# RInW and RImW ...........................................
				if pos in ['NN', 'NNS', 'NNPS','NNP', 'JJ', 'JJR']:
					N_A.append(word)
				elif pos in ['VB', 'VBZ','VBG', 'VBP', 'VBD', 'VBN','RB','RBR', 'WRB', 'RBS']:
					V_A.append(word)       
			# RFPP, RSPP, RFTAPP, RSAPP ...................................
			total_F_S = len(F_P) + len(S_P)
			total_pp = len(F_P) + len(S_P) + len(T_P)
			if total_F_S >0:
				RFP_wrt_SP.append(float(float(len(F_P))/total_F_S))
				RSP_wrt_FP.append(float(float(len(S_P))/total_F_S))
			else:
				RFP_wrt_SP.append(0.0)
				RSP_wrt_FP.append(0.0)
			if total_pp >0:
				RFPTP_wrt_SP.append(float(float(len(F_P)+len(T_P))/total_pp))
				RSP_wrt_FPTP.append(float(float(len(S_P))/total_pp))
			else:
				RFPTP_wrt_SP.append(0.0)
				RSP_wrt_FPTP.append(0.0)
			F_P = []
			S_P = []
			T_P = []
			# RSW and ROW ................................................
			if (len(OBJ) + len(SUB)) > 0:
				RSW.append(float(float(len(SUB))/(len(OBJ) + len(SUB))))
				ROW.append(float(float(len(OBJ))/(len(OBJ) + len(SUB))))
			else:
				RSW.append(0.0)
				ROW.append(0.0)
			SUB = []
			OBJ = []
			# RInW and RImW ..............................................
			RInW = []
			RImW = []
			if len(N_A) + len(V_A) > 0:
				RInW.append(float(float(len(N_A))/(len(N_A) + len(V_A))))
				RImW.append(float(float(len(V_A))/(len(N_A) + len(V_A))))
			else:
				RInW.append(0.0)
				RImW.append(0.0)
			N_A = []
			V_A = []
		# MCS and ACS using Uni-grams and Bi grams TFIDF Vectors, respectively..............
		if (len(temp_rtext)>1):
			try:
				vectorizer = CountVectorizer(stop_words = "english")
				freq_term_matrix = vectorizer.fit_transform(temp_rtext)
				m = freq_term_matrix.shape[0]
				s1= cosine_similarity(freq_term_matrix[0:m], freq_term_matrix)
				n = s1.shape[0]
				mcs = np.max(as_strided(s1, (n-1,n+1), (s1.itemsize*(n+1), s1.itemsize))[:,1:])
				MCS.append(float(mcs))
			except (ValueError) as e:
				MCS.append(0.0)
			try:
				vectorizer1 = CountVectorizer(stop_words = "english", ngram_range = (2,2))
				freq_term_matrix_bigram = vectorizer1.fit_transform(temp_rtext)
				tfidf_transformer = TfidfTransformer()
				tfidf_bigrams_matrix = tfidf_transformer.fit_transform(freq_term_matrix_bigram)
				m1 = tfidf_bigrams_matrix.shape[0]
				s2= cosine_similarity(tfidf_bigrams_matrix[0:m1], tfidf_bigrams_matrix)
				b1 = np.triu(s2, k=1)
				b2 = b1.shape[0]
				acs_tfidf_bigram = float(sum(sum(b1))) / (b2*(b2-1)/2)
				ACS_TFIDF_BIGRAM.append(float(acs_tfidf_bigram))
			except (ValueError) as e:
				ACS_TFIDF_BIGRAM.append(0.0)
		else:
			MCS.append(-1.0)
			ACS_TFIDF_BIGRAM.append(-1.0)
		# ARL ................................................................
		ARL.append(float(sum(RL)/float(len(RL))))	
		# AFPP ASPP, AFTAPP and ASAPP ........................................
		AFPP.append(float(float(sum(RFP_wrt_SP))/len(RFP_wrt_SP)))
		ASPP.append(float(float(sum(RSP_wrt_FP))/len(RSP_wrt_FP)))
		AFTAPP.append(float(float(sum(RFPTP_wrt_SP))/len(RFPTP_wrt_SP)))
		ASAPP.append(float(float(sum(RSP_wrt_FPTP))/len(RSP_wrt_FPTP)))
		# ASW and AOW ........................................................
		ASW.append(float(float(sum(RSW))/len(RSW)))
		AOW.append(float(float(sum(ROW))/len(ROW)))
		# AInW and AImW ......................................................
		AInW.append(float(float(sum(RInW))/len(RInW)))
		AImW.append(float(float(sum(RImW))/len(RImW)))

		temp_rtext = []
		RL = []
		RFP_wrt_SP = []
		RSP_wrt_FP = []
		RFPTP_wrt_SP = []
		RSP_wrt_FPTP = []
		RSW = []
		ROW = []
		RInW = []
		RImW = []
		
		i = i + count[i]
	#print(len(MCS), len(ACS_TFIDF_BIGRAM), len(ARL), len(AFPP),len(ASPP),len(AFTAPP),len(ASAPP), len(ASW),len(AOW),len(AInW),len(AImW))

start_time = time.clock()
print("Start Time : ", start_time , str(datetime.now()))
print("Script Running ...")
MCS_unigram_ACS_TFIDF_bigram_ARL_AFPP_ASPP_AFTAPP_ASAPP_ASW_AOW_AImW_AInW()
print("Running time of this script is : ", time.clock() - start_time, "seconds", str(datetime.now()))

# Saving Features .............................................................

df=pd.DataFrame(list(zip(MCS,ACS_TFIDF_BIGRAM,ARL,AFPP,ASPP,AFTAPP,ASAPP,ASW,AOW,AInW,AImW)))
df.columns = ['MCS_unigram(u)','ACS_bigram_tfidf(u)','ARL(u)','AFPP(u)','ASPP(u)','AFTAPP(u)','ASAPP(u)','ASW(u)','AOW(u)','AInW(u)','AImW(u)']
df.to_excel("Data\\YelpZip\\Resulting Features\\Reviewer_Centric_Textual_Features.xlsx", index = False)			# Change the path according to the file location
