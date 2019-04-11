#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from xlrd import open_workbook
from collections import Counter
import numpy as np
from datetime import datetime
import xlrd
import time
from operator import itemgetter
import pandas as pd

#...
book = open_workbook("Data\\YelpNYC\\Metadata (Sortedby_Reviewer_wise).xlsx")		# Change the path according to the file location
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
book1 = open_workbook("Data\\YelpNYC\\Metadata (Sortedby_Product_wise).xlsx")		# Change the path according to the file location
sheet1 = book1.sheet_by_index(0)
#print(sheet1.nrows)
rid1 = []
pid1 = []
rating1 = []
label1 = []
date1 = []
count1 = []
#...
for row in range(1, sheet1.nrows): #start from 1, to leave out row 0
	rid1.append(int(sheet1.cell(row, 0).value))
	pid1.append(int(sheet1.cell(row, 1).value))
	rating1.append(int(sheet1.cell(row, 2).value))
	label1.append(int(sheet1.cell(row, 3).value))
	date1.append(int(sheet1.cell(row, 4).value))
	count1.append(int(sheet1.cell(row, 5).value))
#print(len(rid1))

avg_rat = []
r_dev = []
rank = []	
tpid = []
sorted_dates = []
Difference_ETF = []
rrpt_20 = []
rrpb_20 = []
mnr = []
rpr = []
rnr = []
ard = []
rbst = []
frr = []
extr = []
exrr = []
mrd = []
wrd =[]
err = []
TRRR_20 = []
BRRR_20 = []

def MNR_RPR_RNR_ARD_WRD_RBST_FRR_EXRR_MRD_ERR_TRRR_BRRR():
	# MNR ...................................................
	temp_date = []
	# RPR_RNR ...............................................
	temp_rating = []
	# ARD ...................................................
	temp_rate = []
	i=0
	while (i < len(rid1)):
		j = count1[i] + i
		for k in range(i,j):
			temp_rate.append(rating1[k])
		avg = float(sum(temp_rate)) / len(temp_rate)
		for k in range(i,j):
			avg_rat.append(float(avg))
		temp_rate = []
		i = i + count1[i]
	rid1_ = np.array(rid1)
	new_avg_rat = map(itemgetter(0), sorted(zip(avg_rat, rid1_), key=itemgetter(1)))
	new_avg_rat1 = list(new_avg_rat)
	temp_rate = []
	# RBST ..................................................
	temp_date = []
	Difference = []
	tau = 76		# value of tau is estimated by recursive minimum entropy partitioning... 
	# WRD + FRR ..............................................
	# Sorting products according to dates.....................
	temp2 = []
	weight = []
	i = 0
	while (i < len(rid1)):
		j = count1[i] + i
		for k in range(i,j):
			temp2.append(xlrd.xldate_as_datetime(date1[k], book.datemode))
		s= sorted(temp2)
		sorted_dates.append(s)
		tpid.append(pid1[i])
		# WRD..................................................
		s1 = list(set(temp2))			# Getting unique dates in temp2
		s1= sorted(s1)					# Sorting dates in s1
		for k in range(i,j):
			for z in range(0, len(s1)):
				if (xlrd.xldate_as_datetime(date1[k], book.datemode)) == s1[z] :
					rank.append(z+1)
					weight.append(1/(math.pow(rank[k],1.5)))
					break
		temp2 = []
		i = i + count1[i]
	rid1_ = np.array(rid1)
	sorted_weight = map(itemgetter(0), sorted(zip(weight, rid1_), key=itemgetter(1)))
	sorted_weight1 = list(sorted_weight)
	temp_rdev = []
	temp_weight = []
	temp_date2 = []
	temp_pid = []
	# EXRR ......................................................
	# Calculating extreme ratings  (EXTR) First .................
	i=0
	while(i < len(rating)):
		if (rating[i] == 1) or (rating[i] == 5):
			extr.append(1)
		else:
			extr.append(0)
		i = i + 1	
	# Calculating extreme rating ratio (EXRR) ...................
	temp_rate1 = []	
	# ERR .......................................................
	# Calculating early time frame (ETF) First ..................
	temp_date1 = []
	i=0
	while (i < len(pid1)):
		j = count1[i] + i
		for k in range(i,j):
			temp_date1.append(date1[k])   
		first = min(temp_date1)
		for k in range(i,j):
			diff = date1[k] - first
			Difference_ETF.append(diff)
		temp_date1 =[]
		i = i + count1[i]
	rid1_ = np.array(rid1)
	new_difference_ETF = map(itemgetter(0), sorted(zip(Difference_ETF, rid1_), key=itemgetter(1)))
	new_difference_ETF1 = list(new_difference_ETF)
	ETF = []
	delta = 210 		# 210 days = 7 months. For more details, refer to Rayana & Akoglu (2015) ...
	beta = 0.0047		# value of beta is estimated by recursive minimal entropy partitioning...
	for i in range(len(new_difference_ETF1)):
		if new_difference_ETF1[i] > delta:
			etf = 0						
		else:
			etf = float(1-(float(new_difference_ETF1[i])/delta))			
		if etf <= beta:
			ETF.append(0)							# No, it's not an early review...
		else:
			ETF.append(1)							# Yes, it's an early review...
	temp_rate2 = []
	# TRRR_BRRR ...................................................
	temp_rank = []
	i=0
	while (i < len(rank)):
		j = i + count1[i]
		for k in range(i,j):
			temp_rank.append(rank[k])
		le = len(set(temp_rank))
		per20 = math.ceil((20*le) / float(100))
		for k in (temp_rank):
			if (k<=per20):
				rrpt_20.append(1)
			else:
				rrpt_20.append(0)
			if (k>(le-per20)):
				rrpb_20.append(1)
			else:
				rrpb_20.append(0)
		temp_rank =[]
		i = i + count1[i]	
	rid1_ = np.array(rid1)
	new_rrpt_20 = map(itemgetter(0), sorted(zip(rrpt_20, rid1_), key=itemgetter(1)))
	new_rrpt_20_1 = list(new_rrpt_20)
	new_rrpb_20 = map(itemgetter(0), sorted(zip(rrpb_20, rid1_), key=itemgetter(1)))
	new_rrpb_20_1 = list(new_rrpb_20)
	temp_top20s = []
	temp_bottom20s = []
	
	i=0
	while (i < len(rid)):
		#print(i)
		j = count[i] + i
		for k in range(i,j):
			temp_date.append(date[k])
			temp_rating.append(rating[k])
			rd = abs(rating[k]-new_avg_rat1[k])/ float(4)
			r_dev.append(float(rd))
			temp_rate.append(float(rd))
			temp_rdev.append(r_dev[k])
			temp_weight.append(sorted_weight1[k])
			temp_date2.append(xlrd.xldate_as_datetime(date[k], book.datemode))
			temp_pid.append(int(pid[k]))
			temp_rate1.append(extr[k])
			temp_rate2.append(ETF[k])
			temp_top20s.append(new_rrpt_20_1[k])
			temp_bottom20s.append(new_rrpb_20_1[k])
		# MNR .............	..........
		g = Counter(temp_date)
		max_value = max(g.values())
		mnr.append(int(max_value))
		# RPR_RNR ....................
		star4 = temp_rating.count(4)
		star5 = temp_rating.count(5)
		star1 = temp_rating.count(1)
		star2 = temp_rating.count(2)
		total_pos = float(star4 + star5)/count[i]
		total_neg = float(star1 + star2)/count[i]
		rpr.append(float(total_pos))
		rnr.append(float(total_neg))
		# ARD ...........................
		avg_rd = float(sum(temp_rate)) / len(temp_rate)
		ard.append(float(avg_rd))
		# WRD ...........................
		erd = sum(temp_rdev[g] * temp_weight[g] for g in range(len(temp_rdev))) / sum(temp_weight)	
		wrd.append(float(erd))
		# RBST ..........................
		first = min(temp_date)
		last = max(temp_date)
		diff = last - first
		Difference.append(diff)
		if (diff > tau):
			rbst.append(0)
		else:
			bst = float(1 - (float(diff)/tau))
			rbst.append(float(bst))
		# FRR .............................
		fcount = 0	
		for l in range(0, len(temp_pid)):
			m1 = temp_pid[l]
			m = tpid.index(m1)
			if temp_date2[l] == sorted_dates[m][0]:
				fcount = fcount + 1
		first = float(fcount)/len(temp_pid)	
		frr.append(float(first))
		# EXRR ............................
		ecount = temp_rate1.count(1)
		extrr = float(ecount)/len(temp_rate1)
		exrr.append(float(extrr))
		# MRD .............................
		max_rd = max(temp_rate)
		mrd.append(float(max_rd))
		# ERR .............................
		ecount = temp_rate2.count(1)
		erratio = float(ecount)/len(temp_rate2)
		err.append(float(erratio))
		# TRRR_BRRR .......................
		count_top20s = temp_top20s.count(1)
		count_bottom20s = temp_bottom20s.count(1)
		TRRR_20 = float(count_top20s)/len(temp_top20s)
		BRRR_20 = float(count_bottom20s)/len(temp_bottom20s)
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
		temp_top20s = []
		temp_bottom20s = []
		
		i = i + count[i]	
	#print(len(rpr), len(rnr), len(mnr), len(ard), len(wrd), len(rbst),len(frr), len(exrr), len(mrd), len(err),len(TRRR_20), len(BRRR_20))

start_time = time.clock()
print("Start Time : ", start_time , str(datetime.now()))
print("Script Running ...")
MNR_RPR_RNR_ARD_WRD_RBST_FRR_EXRR_MRD_ERR_TRRR_BRRR()
print("Running time of this script is : ", time.clock() - start_time, "seconds", str(datetime.now()))

# Saving Features ..................................................................

df=pd.DataFrame(list(zip(mnr,rpr,rnr,ard,wrd,rbst,frr,exrr,mrd,err,TRRR_20,BRRR_20)))
df.columns = ['MNR(u)',	'RPR(u)',	'RNR(u)',	'ARD(u)',	'WRD(u)',	'RBST (u)',	'FRR(u)',	'EXRR(u)',	'MRD(u)',	'ERR(u)',	'TRRR(u)',	'BRRR(u)']
df.to_excel("Data\\YelpNYC\\Resulting Features\\Reviewer_Centric_Behavioral_Features.xlsx", index = False)		# Change the path according to the file location
