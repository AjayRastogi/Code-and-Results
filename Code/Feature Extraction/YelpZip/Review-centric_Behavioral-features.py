#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
import math
from xlrd import open_workbook
import re
import numpy as np
from datetime import datetime
import time
import string
import pandas as pd 

book = open_workbook("Data\\YelpZip\\Metadata (Sortedby_Product_wise).xlsx")		# Change the path according to the file location
sheet = book.sheet_by_index(0) 
#print(sheet.nrows)
rid = []
pid = []
rating = []
label = []
date = []
count = []
for row in range(1, sheet.nrows): #start from 1, to leave out row 0
	rid.append(int(sheet.cell(row, 0).value))
	pid.append(int(sheet.cell(row, 1).value))
	rating.append(int(sheet.cell(row, 2).value))
	label.append(int(sheet.cell(row, 3).value))
	date.append(int(sheet.cell(row, 4).value))
	count.append(int(sheet.cell(row, 5).value))
#print(len(rid))

#...
book1 = open_workbook("Data\\YelpZip\\ReviewContent (Sortedby_Product_wise).xlsx")		# Change the path according to the file location
sheet1 = book1.sheet_by_index(0) 
#print(sheet1.nrows)
rtext = []
for row in range(1, sheet1.nrows): #start from 1, to leave out row 0
	rtext.append(sheet1.cell(row, 3).value)
#print(len(rtext))

#...
regex = re.compile('[%s]' % re.escape(string.punctuation))	
RD = []
ERD = []
ETF = []
EXT = []
TRR = []
BRR = []
RANK = []
RL = []

def RD_EXT_ETF_TRR_BRR_ERD_Rank_RL():
	temp_rate = []
	temp_date = []
	delta = 210			# 210 days = 7 months. For more details, refer to Rayana & Akoglu (2015) ...
	beta = 0.0047		# value of beta is estimated by recursive minimal entropy partitioning...
	temp_rank = []
	rank1 = []
	weight = []
	
	i=0
	while (i < len(rid)):
		#print(i)
		j = count[i] + i
		for k in range(i,j):
			temp_rate.append(rating[k])
			temp_date.append(date[k])
			temp_date.append(xlrd.xldate_as_datetime(date[k], book.datemode))
			# RL 
			pre_text = re.sub(r'[^\x00-\x7F]+',' ', rtext[k])
			RL.append(len(pre_text.split()))
		avg_rate = float(sum(temp_rate)) / len(temp_rate)
		first = min(temp_date)
		s = list(set(temp_date))
		s= sorted(s)
		for k in range(i,j):
			# RD
			rdev = abs(rating[k] - avg_rate)/float(4)
			RD.append(float(rdev))
			# EXT
			if (rating[k] == 1) or (rating[k] == 5):
				EXT.append(1)
			else:
				EXT.append(0)
			# ETF
			diff = date[k] - first
			if (diff > delta):
				etf = 0
			else:
				etf = float(1 -  (float(diff)/delta))
			if (etf <= beta):
				ETF.append(0)
			else:
				ETF.append(1)
			# TRR and BRR
			# Calculating Rank First ...................................
			for z in range(0, len(s)):
				if (xlrd.xldate_as_datetime(date[k], book.datemode)) == s[z] :
					temp_rank.append(z+1)
					rank1.append(z+1)
					weight.append(1/(math.pow(rank1[k],1.5)))
					break
			# ERD
			erd = RD[k] * weight[k]
			ERD.append(float(erd))
		# Calculating TRR and BRR Now ...................................
		le = len(set(temp_rank))
		per20 = math.ceil((20*le) / float(100))
		for k1 in (temp_rank):
			if (k1<=per20):
				TRR.append(1)
			else:
				TRR.append(0)
			if (k1>(le-per20)):
				BRR.append(1)
			else:
				BRR.append(0)
		# Normalized Rank by min-max normalization ......................
		mn = min(temp_rank)
		mx = max(temp_rank)
		if (mn == mx):
			RANK.append(1)
		else:
			for k2 in range(0, len(temp_rank)):
				rank = (temp_rank[k2] - mn) / float((mx-mn))
				RANK.append(rank)
		temp_rate = []
		temp_date = []
		temp_rank = []
		i = i + count[i]
	#print(len(RD), len(EXT), len(ETF), len(TRR), len(BRR), len(ERD), len(RL), len(RANK))
	
start_time = time.clock()
print("Start Time : ", start_time , str(datetime.now()))
print("Script Running ...")
RD_EXT_ETF_TRR_BRR_ERD_Rank_RL()
print("Running time of this script is : ", time.clock() - start_time, "seconds", str(datetime.now()))	


df=pd.DataFrame(list(zip(RD,EXT,ETF,TRR,BRR,ERD,RL,RANK)))				
df.columns = ['RD(r)','EXT(r)','ETF(r)','TRR(r)','BRR(r)','ERD(r)','RL(r)','Rank(r)']
df.to_excel("Data\\YelpZip\\Resulting Features\\Review_Centric_Behavioral_Features.xlsx", index = False)			# Change the path according to the file location
