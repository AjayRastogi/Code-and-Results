#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import auc
import pickle
import math
import warnings

warnings.filterwarnings("ignore")
print("Please wait, Plotting ...")

cls = ['SVM','LR','MLP']
# Reading model objects as returned by model training phase ...............
# Reviewer-Centric Setting ................................................
precision_revr_b = []
precision_revr_t = []
recall_revr_b = []
recall_revr_t = []
for k in range(0, len(cls)):
	models_revr_b = []
	models_revr_t = []
	for u in range(0,10):
		models_revr_b.append(pickle.load(open('Data\\Results\\YelpZip\\Reviewer Behavioral\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))	# Change the path according to the file location
	for u in range(0,10):
		models_revr_t.append(pickle.load(open('Data\\Results\\YelpZip\\Reviewer Textual\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))		# Change the path according to the file location
	
	AP_B = []
	AP_T = []
	for m in models_revr_b:
		AP_B.append(sum(m['test_ap'])/float(len(m['test_ap'])))
	for m in models_revr_t:
		AP_T.append(sum(m['test_ap'])/float(len(m['test_ap'])))

	diff = []
	r = sum(AP_B)/len(AP_B)				# Average AP score for behavioral features over all 5-folds and models
	for i in models_revr_b:
		for j in i['test_ap']:
			diff.append(abs(r-j))
	col1 = np.argmin(diff) + 1			# Picking up that fold which returns same AP score as average AP score

	diff1 = []
	r = sum(AP_T)/len(AP_T)				# Average AP score for textual features over all 5-folds and models
	for i in models_revr_t:
		for j in i['test_ap']:
			diff1.append(abs(r-j))
	col2 = np.argmin(diff1) + 1			# Picking up that fold which returns same AP score as average AP score

	# Reading precision and recall values ..............................................
	precision_revr_b.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Reviewer Behavioral\\'+str(cls[k])+'\\Pre_Recall_Threshold_Reviewer_Behavioral.xlsx', sheetname=0, header= None, parse_cols =[col1,col1])))		# Change the path according to the file location
	recall_revr_b.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Reviewer Behavioral\\'+str(cls[k])+'\\Pre_Recall_Threshold_Reviewer_Behavioral.xlsx', sheetname=1, header= None, parse_cols =[col1,col1])))		# Change the path according to the file location
	precision_revr_t.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Reviewer Textual\\'+str(cls[k])+'\\Pre_Recall_Threshold_Reviewer_Textual.xlsx', sheetname=0, header= None, parse_cols =[col2,col2])))			# Change the path according to the file location
	recall_revr_t.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Reviewer Textual\\'+str(cls[k])+'\\Pre_Recall_Threshold_Reviewer_Textual.xlsx', sheetname=1, header= None, parse_cols =[col2,col2])))				# Change the path according to the file location

# Reading model objects as returned by model training phase ...............
# Review-Centric Setting ..................................................
precision_rev_b = []
precision_rev_t = []
recall_rev_b = []
recall_rev_t = []
for k in range(0, len(cls)):
	models_rev_b = []
	models_rev_t = []
	for u in range(0,21):
		models_rev_b.append(pickle.load(open('Data\\Results\\YelpZip\\Review Behavioral\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))	# Change the path according to the file location
	for u in range(0,21):
		models_rev_t.append(pickle.load(open('Data\\Results\\YelpZip\\Review Textual\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))		# Change the path according to the file location
	
	AP_B = []
	AP_T = []
	for m in models_rev_b:
		AP_B.append(sum(m['test_ap'])/float(len(m['test_ap'])))
	for m in models_rev_t:
		AP_T.append(sum(m['test_ap'])/float(len(m['test_ap'])))

	diff = []
	r = sum(AP_B)/len(AP_B)				# Average AP score for behavioral features over all 5-folds and models
	for i in models_rev_b:
		for j in i['test_ap']:
			diff.append(abs(r-j))
	col1 = np.argmin(diff) + 1			# Picking up that fold which returns same AP score as average AP score

	diff1 = []
	r = sum(AP_T)/len(AP_T)				# Average AP score for textual features over all 5-folds and models
	for i in models_rev_t:
		for j in i['test_ap']:
			diff1.append(abs(r-j))
	col2 = np.argmin(diff1) + 1			# Picking up that fold which returns same AP score as average AP score

	# Reading precision and recall values ..............................................
	precision_rev_b.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Review Behavioral\\'+str(cls[k])+'\\Pre_Recall_Threshold_Review_Behavioral.xlsx', sheetname=0, header= None, parse_cols =[col1,col1])))		# Change the path according to the file location
	recall_rev_b.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Review Behavioral\\'+str(cls[k])+'\\Pre_Recall_Threshold_Review_Behavioral.xlsx', sheetname=1, header= None, parse_cols =[col1,col1])))			# Change the path according to the file location
	precision_rev_t.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Review Textual\\'+str(cls[k])+'\\Pre_Recall_Threshold_Review_Textual.xlsx', sheetname=0, header= None, parse_cols =[col2,col2])))			# Change the path according to the file location
	recall_rev_t.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Review Textual\\'+str(cls[k])+'\\Pre_Recall_Threshold_Review_Textual.xlsx', sheetname=1, header= None, parse_cols =[col2,col2])))				# Change the path according to the file location

# Reading model objects as returned by model training phase ...............
# Product-Centric Setting ..................................................
precision_prod_b = []
precision_prod_t = []
recall_prod_b = []
recall_prod_t = []
for k in range(0, len(cls)):
	models_prod_b = []
	models_prod_t = []
	for u in range(0,2):
		models_prod_b.append(pickle.load(open('Data\\Results\\YelpZip\\Product Behavioral\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))	# Change the path according to the file location
	for u in range(0,2):
		models_prod_t.append(pickle.load(open('Data\\Results\\YelpZip\\Product Textual\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))		# Change the path according to the file location
	
	AP_B = []
	AP_T = []
	for m in models_prod_b:
		AP_B.append(sum(m['test_ap'])/float(len(m['test_ap'])))
	for m in models_prod_t:
		AP_T.append(sum(m['test_ap'])/float(len(m['test_ap'])))

	diff = []
	r = sum(AP_B)/len(AP_B)				# Average AP score for behavioral features over all 5-folds and models
	for i in models_prod_b:
		for j in i['test_ap']:
			diff.append(abs(r-j))
	col1 = np.argmin(diff) + 1			# Picking up that fold which returns same AP score as average AP score

	diff1 = []
	r = sum(AP_T)/len(AP_T)				# Average AP score for textual features over all 5-folds and models
	for i in models_prod_t:
		for j in i['test_ap']:
			diff1.append(abs(r-j))
	col2 = np.argmin(diff1) + 1			# Picking up that fold which returns same AP score as average AP score

	# Reading precision and recall values ..............................................
	precision_prod_b.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Product Behavioral\\'+str(cls[k])+'\\Pre_Recall_Threshold_Product_Behavioral.xlsx', sheetname=0, header= None, parse_cols =[col1,col1])))		# Change the path according to the file location
	recall_prod_b.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Product Behavioral\\'+str(cls[k])+'\\Pre_Recall_Threshold_Product_Behavioral.xlsx', sheetname=1, header= None, parse_cols =[col1,col1])))			# Change the path according to the file location
	precision_prod_t.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Product Textual\\'+str(cls[k])+'\\Pre_Recall_Threshold_Product_Textual.xlsx', sheetname=0, header= None, parse_cols =[col2,col2])))				# Change the path according to the file location
	recall_prod_t.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Product Textual\\'+str(cls[k])+'\\Pre_Recall_Threshold_Product_Textual.xlsx', sheetname=1, header= None, parse_cols =[col2,col2])))				# Change the path according to the file location
	
# Plotting PR Curves .....................................................
# Reviewer-Centric Setting ................................................
i = 331
for k in range(0, len(cls)):
	plt.subplot(i)
	plt.title('PR for Reviewer-centric Setting',fontsize=10)
	pr_auc_b = auc(recall_revr_b[k],precision_revr_b[k])
	pr_auc_t = auc(recall_revr_t[k],precision_revr_t[k])
	plt.plot(recall_revr_b[k], precision_revr_b[k], 'c',linewidth=0.8,label='Behavioral (AUC = %0.2f)'% pr_auc_b)
	plt.plot(recall_revr_t[k], precision_revr_t[k], 'r',linewidth=0.8,label='Textual (AUC = %0.2f)'% pr_auc_t)
	plt.legend(loc='lower right',prop={'size':8})
	plt.xlim([0.0,1.0])
	plt.ylim([0.0,1.0])
	plt.ylabel('Precision',fontsize=8)
	plt.xlabel('(a) Recall',fontsize=8)
	props = dict(boxstyle='round', facecolor='white', alpha=0.3)
	plt.text(0.8, 0.9, cls[k], fontsize=8,verticalalignment='top', bbox=props)
	i=i+1

# Review-Centric Setting ................................................
for k in range(0, len(cls)):
	plt.subplot(i)
	plt.title('PR for Review-centric Setting',fontsize=10)
	pr_auc_b = auc(recall_rev_b[k],precision_rev_b[k])
	pr_auc_t = auc(recall_rev_t[k],precision_rev_t[k])
	plt.plot(recall_rev_b[k], precision_rev_b[k], 'c',linewidth=0.8,label='Behavioral (AUC = %0.2f)'% pr_auc_b)
	plt.plot(recall_rev_t[k], precision_rev_t[k], 'r',linewidth=0.8,label='Textual (AUC = %0.2f)'% pr_auc_t)
	plt.legend(loc='lower right',prop={'size':8})
	plt.xlim([0.0,1.0])
	plt.ylim([0.0,1.0])
	plt.ylabel('Precision',fontsize=8)
	plt.xlabel('(b) Recall',fontsize=8)
	props = dict(boxstyle='round', facecolor='white', alpha=0.3)
	plt.text(0.8, 0.9, cls[k], fontsize=8,verticalalignment='top', bbox=props)
	i=i+1

# Product-Centric Setting ................................................
for k in range(0, len(cls)):
	plt.subplot(i)
	plt.title('PR for Product-centric Setting',fontsize=10)
	pr_auc_b = auc(recall_prod_b[k],precision_prod_b[k])
	pr_auc_t = auc(recall_prod_t[k],precision_prod_t[k])
	plt.plot(recall_prod_b[k], precision_prod_b[k], 'c',linewidth=0.8,label='Behavioral (AUC = %0.2f)'% pr_auc_b)
	plt.plot(recall_prod_t[k], precision_prod_t[k], 'r',linewidth=0.8,label='Textual (AUC = %0.2f)'% pr_auc_t)
	plt.legend(loc='lower right',prop={'size':8})
	plt.xlim([0.0,1.0])
	plt.ylim([0.0,1.0])
	plt.ylabel('Precision',fontsize=8)
	plt.xlabel('(c) Recall',fontsize=8)
	props = dict(boxstyle='round', facecolor='white', alpha=0.3)
	plt.text(0.8, 0.9, cls[k], fontsize=8,verticalalignment='top', bbox=props)
	i=i+1
plt.show()
