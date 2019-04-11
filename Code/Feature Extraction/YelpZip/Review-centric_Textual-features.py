#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
from nltk import word_tokenize       
from xlrd import open_workbook
import re
import io
from nltk import pos_tag
from nltk.corpus import stopwords
import nltk.tokenize.punkt
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
import time
from datetime import datetime
import pandas as pd

#...
book = open_workbook("Data\\YelpZip\\ReviewContent (Sortedby_Product_wise).xlsx")		# Change the path according to the file location
sheet = book.sheet_by_index(0)
#print(sheet.nrows)
rid = []
pid = []
date = []
text = []
count = []

#...
for row in range(1, sheet.nrows): #start from 1, to leave out row 0
	rid.append(int(sheet.cell(row, 0).value))
	pid.append(int(sheet.cell(row, 1).value))
	date.append(int(sheet.cell(row, 2).value))
	text.append(sheet.cell(row, 3).value)
	count.append(int(sheet.cell(row, 4).value))
#print(len(text))

RFPP = []
RSPP = []
RFTAPP = []
RSAPP = []
RSW = []
ROW = []
RInW = []
RImW = []
RPW = []
RNW = []

def RFPP_RSPP_RFTAPP_RSAPP_RSW_ROW_RInW_RImW_RPW_RNW():
	F_P = []
	S_P = []
	T_P = []
	OBJ = []
	SUB = []
	tag = ['PRP', 'PRP$', 'WP', 'WP$',':','.','\'\'','CC', 'CD', 'DT', 'EX', 'FW', 'IN','LS','MD','POS', 'TO', 'UH', 'PDT', 'SYM', 'RP']
	noun = ['NN', 'NNS', 'NNP', 'NNPS']
	adj = ['JJ', 'JJR', 'JJS']
	verb = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
	adverb = ['RB', 'RBR', 'RBS', 'WRB']
	N_A = []
	V_A = []
	positive_words = []
	negative_words = []
	word_features = []
	aDict = dict(zip('abcdefghijklmnopqrstuvwxyz', range(0, 26)))
	pos_index = dict([(35,203),(204,280),(281,422),(423,496),(497,700),(701,814),(815,902),(903,973),(974,1071),(1072,1088),(1089,1097),(1098,1163),(1164,1228),(1229,1250),(1251,1283),(1284,1437),(1438,1443),(1444,1587),(1588,1809),(1810,1888),(1889,1937),(1938,1962),(1963,2034),(2033,2038),(2035,2036),(2037,2040)])
	neg_index = dict([(37,266),(267,534),(535,844),(845,1463),(1464,1593),(1594,1853),(1854,1959),(1960,2136),(2137,2623),(2624,2658),(2659,2671),(2672,2813),(2814,3028),(3029,3089),(3090,3234),(3235,3450),(3451,3465),(3466,3677),(3678,4219),(4220,4385),(4386,4638),(4639,4703),(4704,4809),(4809,4810),(4810,4810),(4811,4817)])
	positive_f = io.open("Data\\opinion-lexicon-English\\positive-words.txt", 'r',encoding  =  'utf-8', errors = 'ignore')		# Change the path according to the file location
	positive_lines = positive_f.readlines()
	negative_f = io.open("Data\\opinion-lexicon-English\\negative-words.txt", 'r', encoding  = 'utf-8', errors = 'ignore')		# Change the path according to the file location
	negative_lines = negative_f.readlines()
	
	for i in range(0, len(text)):
		#print(i)
		pre_text = re.sub(r'[^\x00-\x7F]+',' ', text[i])			#replacing non-ascii characters with a space
		pre_text = re.sub('[^a-zA-Z0-9-_ \' ]', ' ', pre_text)
		pre_text = pre_text.replace(' i ', ' I ')
		pre_text = pre_text.replace('i ', 'I ')
		pre_text = pre_text.replace(' i\'', ' I\'')
		temp_words = []
		for word, pos in pos_tag(word_tokenize(pre_text)):
			flag = False
			# RFPP, RSPP, RFTAPP, RSAPP .............................
			if (pos == 'PRP' or pos == 'PRP$') and (word.lower() in ['i','me','my','mine','we','our','us','ours','myself','ourselves']):
				F_P.append(word.lower())
			elif (pos == 'PRP' or pos == 'PRP$') and (word.lower() in ['you','your','yours','yourself','yourselves']):
				S_P.append(word.lower())
			elif (pos == 'PRP' or pos == 'PRP$') and (word.lower() in ['he','she','it','his','her','him','its','hisself','herself','himself','itself','hers','they','their','them','theirs','themself','themselves']):
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
					synset = swn.senti_synsets(word)
					if len(list(synset)) != 0:
						synset = swn.senti_synsets(word)
						syn_score = list(synset)[0]
						if float(syn_score.obj_score()) > float(0.5):
							OBJ.append(word)
						elif float(float(syn_score.pos_score()) + float(syn_score.neg_score())) > float(0.5):
							SUB.append(word)
					else:
						temp_words.append(word)
				else:
					synset = swn.senti_synsets(word, wn_tag)
					if len(list(synset)) != 0:
						synset = swn.senti_synsets(word, wn_tag)
						syn_score = list(synset)[0]
						if float(syn_score.obj_score()) > float(0.5):
							OBJ.append(word)
						elif float(float(syn_score.pos_score()) + float(syn_score.neg_score())) > float(0.5):
							SUB.append(word)
					else:
						temp_words.append(word)
			# RInW and RImW .........................................
			if pos in ['NN', 'NNS', 'NNPS','NNP', 'JJ', 'JJR']:
				N_A.append(word)
			elif pos in ['VB', 'VBZ','VBG', 'VBP', 'VBD', 'VBN','RB','RBR', 'WRB', 'RBS']:
				V_A.append(word)   
			# RPW and RNW ...........................................
			if pos in ['JJ', 'JJR', 'JJS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'RB', 'RBR', 'RBS', 'NN', 'NNS', 'NNP', 'NNPS']:
				ll = ["'","-","_","0","1","2","3","4","5","6","7","8","9"]
				if word[0] in ll:
					continue
				first = aDict[word[0].lower()]
				start = sorted(pos_index)[first]
				end = pos_index[start]
				for j in range(start, end+1):
					if word == (positive_lines[j].replace("\n", '')):
						positive_words.append(word)
						flag = True
						break
				if flag is False:
					start = sorted(neg_index)[first]
					end = neg_index[start]
					for j in range(start, end+1):
						if word == (negative_lines[j].replace("\n", '')):
							negative_words.append(word)
							break 
		# RFPP, RSPP, RFTAPP, RSAPP .................................
		total_F_S = len(F_P) + len(S_P)
		total_pp = len(F_P) + len(S_P) + len(T_P)
		if total_F_S >0:
			RFPP.append(float(float(len(F_P))/total_F_S))
			RSPP.append(float(float(len(S_P))/total_F_S))
		else:
			RFPP.append(0.0)
			RSPP.append(0.0)
		if total_pp >0:
			RFTAPP.append(float(float(len(F_P)+len(T_P))/total_pp))
			RSAPP.append(float(float(len(S_P))/total_pp))
		else:
			RFTAPP.append(0.0)
			RSAPP.append(0.0)
		F_P = []
		S_P = []
		T_P = []
		# RSW and ROW ...............................................
		if (len(OBJ) + len(SUB)) > 0:
			RSW.append(float(float(len(SUB))/(len(OBJ) + len(SUB))))
			ROW.append(float(float(len(OBJ))/(len(OBJ) + len(SUB))))
		else:
			RSW.append(0.0)
			ROW.append(0.0)
		SUB = []
		OBJ = []
		# RInW and RImW ..............................................
		if len(N_A) + len(V_A) > 0:
			RInW.append(float(float(len(N_A))/(len(N_A) + len(V_A))))
			RImW.append(float(float(len(V_A))/(len(N_A) + len(V_A))))
		else:
			RInW.append(0.0)
			RImW.append(0.0)
		N_A = []
		V_A = []
		# RPW and RNW ...............................................
		if (len(positive_words) + len(negative_words)) > 0:
			RPW.append(float(float(len(positive_words))/(len(positive_words) + len(negative_words))))
			RNW.append(float(float(len(negative_words))/(len(positive_words) + len(negative_words))))
		else:
			RPW.append(0.0)
			RNW.append(0.0)
		positive_words = []
		negative_words = []
		
	#print(len(RFPP), len(RSPP), len(RFTAPP), len(RSAPP), len(RSW), len(ROW), len(RInW),len(RImW), len(RPW), len(RNW))
		
start_time = time.clock()
print("Start Time : ", start_time , str(datetime.now()))
print("Script Running ...")
RFPP_RSPP_RFTAPP_RSAPP_RSW_ROW_RInW_RImW_RPW_RNW()
print("Running time of this script is : ", time.clock() - start_time, "seconds", str(datetime.now()))

# Saving Features .............................................................

df=pd.DataFrame(list(zip(RFPP,RSPP,RFTAPP,RSAPP,RSW,ROW,RInW,RImW,RPW,RNW)))
df.columns = ['RFPP(r)','RSPP(r)','RFTAPP(r)','RSAPP(r)','RSW(r)','ROW(r)','RInW(r)','RImW(r)','RPW(r)','RNW(r)']
df.to_excel("Data\\YelpZip\\Resulting Features\\Review_Centric_Textual_Features.xlsx", index = False)			# Change the path according to the file location

