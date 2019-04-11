#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from xlrd import open_workbook
import xlsxwriter
import counter
import numpy as np
from datetime import datetime
from datetime import date
import xlrd
import math
import operator
import time
from operator import itemgetter

#...
book = open_workbook("Data\\YelpNYC\\Metadata (Sortedby_Product_wise).xlsx")		# Change the path according to the file location
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

avg_rat = []
r_dev = []
rank = []	
tpid = []
sorted_dates = []
Difference_ETF = []
mnr = []
rpr = []
rnr = []
ard = []
pbst = []
extr = []
exrr = []
mrd = []
wrd =[]
err = []
TRRR_20 = []
BRRR_20 = []

def Product_MNR_RPR_RNR_ARD_WRD_PBST_EXRR_MRD_ERR_TRRR_BRRR():
	# MNR ........................................................
	temp_date = []
	# RPR_RNR ....................................................
	temp_rating = []
	# ARD ........................................................
	temp_rate = []
	i=0
	while (i < len(pid)):
		j = count[i] + i
		for k in range(i,j):
			temp_rate.append(rating[k])
		avg = float(sum(temp_rate)) / len(temp_rate)
		for k in range(i,j):
			avg_rat.append(float(avg))
		temp_rate = []
		i = i + count[i]
	temp_rate = []
	# PBST .......................................................
	temp_date = []
	Difference = []
	tau = 76			# value of tau is estimated by recursive minimum entropy partitioning... 
	# WRD ........................................................
	# Sorting products according to dates.........................
	temp2 = []
	weight = []
	i = 0
	while (i < len(pid)):
		j = count[i] + i
		for k in range(i,j):
			temp2.append(xlrd.xldate_as_datetime(date[k], book.datemode))
		s= sorted(temp2)
		sorted_dates.append(s)
		tpid.append(pid[i])
		# WRD ....................................................
		s1 = list(set(temp2))			# Getting unique dates in temp2
		s1= sorted(s1)					# Sorting dates in s1
		for k in range(i,j):
			for z in range(0, len(s1)):
				if (xlrd.xldate_as_datetime(date[k], book.datemode)) == s1[z] :
					rank.append(z+1)
					weight.append(1/(math.pow(rank[k],1.5)))
					break
		temp2 = []
		i = i + count[i]
	temp_rdev = []
	temp_weight = []
	# EXRR ......................................................
	# Calculating extreme ratings (EXTR) First  .................
	i=0
	while(i < len(rating)):
		if (rating[i] == 1) or (rating[i] == 5):
			extr.append(1)
		else:
			extr.append(0)
		i = i + 1	
	# Calculating extreme rating ratio (EXRR) ...................
	temp_rate1 = []
	# MRD .......................................................
	temp_rate = []
	# ERR .......................................................
	# Calculating early time frame (ETF) First ..................
	temp_date = []
	i=0
	while (i < len(pid)):
		j = count[i] + i
		for k in range(i,j):
			temp_date.append(date[k])   
		first = min(temp_date)
		for k in range(i,j):
			diff = date[k] - first
			Difference_ETF.append(diff)
		temp_date =[]
		i = i + count[i]
	# Calculating early review ratio (ERR) .......................
	early_review = []
	delta = 210 		# 210 days = 7 months. For more details, refer to Rayana & Akoglu (2015) ...
	for i in range(len(Difference_ETF)):
		if Difference_ETF[i] > delta:
			early_review.append(0)		# No, it's not an early review...
		else:
			early_review.append(1)		# Yes, it's an early review...
	temp_rate2 = []
	# TRRR_BRRR ...................................................
	temp_top20 = []
	temp_bottom20 = []
	
	i=0
	while (i < len(pid)):
		#print(i)
		j = count[i] + i
		for k in range(i,j):
			temp_date.append(date[k])
			temp_rating.append(rating[k])
			rd = abs(rating[k]-avg_rat[k])/ float(4)
			r_dev.append(float(rd))
			temp_rate.append(float(rd))
			temp_rdev.append(r_dev[k])
			temp_weight.append(weight[k])
			temp_rate1.append(extr[k])
			temp_rate2.append(early_review[k])
		# MNR .............	........................................
		g = counter.Counter(temp_date)
		max_value = max(g.values())
		mnr.append(int(max_value))
		# RPR_RNR ..................................................
		star4 = temp_rating.count(4)
		star5 = temp_rating.count(5)
		star1 = temp_rating.count(1)
		star2 = temp_rating.count(2)
		total_pos = float(star4 + star5)/count[i]
		total_neg = float(star1 + star2)/count[i]
		rpr.append(float(total_pos))
		rnr.append(float(total_neg))
		# ARD .......................................................
		avg_rd = float(sum(temp_rate)) / len(temp_rate)
		ard.append(float(avg_rd))
		# WRD .......................................................
		erd = sum(temp_rdev[g] * temp_weight[g] for g in range(len(temp_rdev))) / sum(temp_weight)	
		wrd.append(float(erd))
		# PBST ......................................................
		first = min(temp_date)
		last = max(temp_date)
		diff = last - first
		Difference.append(diff)
		if (diff > tau):
			pbst.append(0)
		else:
			bst = float(1 - (float(diff)/tau))
			pbst.append(float(bst))
		# EXRR ......................................................
		ecount = temp_rate1.count(1)
		extrr = float(ecount)/len(temp_rate1)
		exrr.append(float(extrr))
		# MRD .......................................................
		max_rd = max(temp_rate)
		mrd.append(float(max_rd))
		# ERR .......................................................
		ecount = temp_rate2.count(1)
		erratio = float(ecount)/len(temp_rate2)
		err.append(float(erratio))
		# TRRR_BRRR .................................................
		per20 = math.ceil((20*diff) / float(100))
		counts_top20s = first + per20
		counts_bottom20s = last - per20
		for k in range(i,j):
			if (date[k] <= counts_top20s):
				temp_top20.append(date[k])
			if (date[k] >= counts_bottom20s):
				temp_bottom20.append(date[k])
		TRRR_20 = float(len(temp_top20))/len(temp_date)
		BRRR_20 = float(len(temp_bottom20))/len(temp_date)
		TRRR_20.append(float(TRRR_20))
		BRRR_20.append(float(BRRR_20))
		
		temp_rating = []
		temp_date =[]
		temp_rate =[]
		temp_rdev =[]
		temp_weight = []
		temp_date2 = []
		temp_pid = []
		temp_rate1 =[]
		temp_rate2 =[]
		temp_top20 = []
		temp_bottom20 = []
		
		i = i + count[i]	
	#print(len(rpr), len(rnr), len(mnr), len(ard), len(wrd), len(pbst), len(exrr), len(mrd), len(err),len(TRRR_20), len(BRRR_20))

start_time = time.clock()
print("Start Time : ", start_time , str(datetime.now()))
print("Script Running ...")
Product_MNR_RPR_RNR_ARD_WRD_PBST_EXRR_MRD_ERR_TRRR_BRRR()
print ("Running time of this script is : ", time.clock() - start_time, "seconds", str(datetime.now()))


# Saving Features ..................................................................

df=pd.DataFrame(list(zip(mnr,rpr,rnr,ard,wrd,pbst,exrr,mrd,err,TRRR_20,BRRR_20)))
df.columns = ['MNR(p)',	'RPR(p)',	'RNR(p)',	'ARD(p)',	'WRD(p)',	'PBST (p)',	'EXRR(p)',	'MRD(p)',	'ERR(p)',	'TRRR(p)',	'BRRR(p)']
df.to_excel("Data\\YelpNYC\\Resulting Features\\Product_Centric_Behavioral_Features.xlsx", index = False)		# Change the path according to the file location
