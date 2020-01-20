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
fpr_revr_b = []
fpr_revr_t = []
tpr_revr_b = []
tpr_revr_t = []
for k in range(0, len(cls)):
	models_revr_b = []
	models_revr_t = []
	for u in range(0,10):
		models_revr_b.append(pickle.load(open('Data\\Results\\YelpZip\\Reviewer Behavioral\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))	# Change the path according to the file location
	for u in range(0,10):
		models_revr_t.append(pickle.load(open('Data\\Results\\YelpZip\\Reviewer Textual\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))		# Change the path according to the file location

	ROC_B = []
	ROC_T = []
	for m in models_revr_b:
		ROC_B.append(sum(m['test_roc_auc'])/float(len(m['test_roc_auc'])))
	for m in models_revr_t:
		ROC_T.append(sum(m['test_roc_auc'])/float(len(m['test_roc_auc'])))

	diff = []
	r = sum(ROC_B)/len(ROC_B)				# Average roc-auc score for behavioral features over all 5-folds and models
	for i in models_revr_b:
		for j in i['test_roc_auc']:
			diff.append(abs(r-j))
	col1 = np.argmin(diff) + 1				# Picking up that fold which returns same roc-auc score as average roc-auc score

	diff1 = []
	r = sum(ROC_T)/len(ROC_T)				# Average roc-auc score for textual features over all 5-folds and models
	for i in models_revr_t:
		for j in i['test_roc_auc']:
			diff1.append(abs(r-j))
	col2 = np.argmin(diff1) + 1				# Picking up that fold which returns same roc-auc score as average roc-auc score

	# Reading FPR and TPR values ..............................................
	fpr_revr_b.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Reviewer Behavioral\\'+str(cls[k])+'\\FPR_TPR_Threshold_Reviewer_Behavioral.xlsx', sheetname=0, header= None, parse_cols =[col1,col1])))		# Change the path according to the file location
	tpr_revr_b.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Reviewer Behavioral\\'+str(cls[k])+'\\FPR_TPR_Threshold_Reviewer_Behavioral.xlsx', sheetname=1, header= None, parse_cols =[col1,col1])))		# Change the path according to the file location
	fpr_revr_t.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Reviewer Textual\\'+str(cls[k])+'\\FPR_TPR_Threshold_Reviewer_Textual.xlsx', sheetname=0, header= None, parse_cols =[col2,col2])))			# Change the path according to the file location
	tpr_revr_t.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Reviewer Textual\\'+str(cls[k])+'\\FPR_TPR_Threshold_Reviewer_Textual.xlsx', sheetname=1, header= None, parse_cols =[col2,col2])))			# Change the path according to the file location

# Reading model objects as returned by model training phase ...............
# Review-Centric Setting ..................................................
fpr_rev_b = []
fpr_rev_t = []
tpr_rev_b = []
tpr_rev_t = []
for k in range(0, len(cls)):
	models_rev_b = []
	models_rev_t = []
	for u in range(0,21):
		models_rev_b.append(pickle.load(open('Data\\Results\\YelpZip\\Review Behavioral\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))	# Change the path according to the file location
	for u in range(0,21):
		models_rev_t.append(pickle.load(open('Data\\Results\\YelpZip\\Review Textual\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))		# Change the path according to the file location

	ROC_B = []
	ROC_T = []
	for m in models_rev_b:
		ROC_B.append(sum(m['test_roc_auc'])/float(len(m['test_roc_auc'])))
	for m in models_rev_t:
		ROC_T.append(sum(m['test_roc_auc'])/float(len(m['test_roc_auc'])))

	diff = []
	r = sum(ROC_B)/len(ROC_B)				# Average roc-auc score for behavioral features over all 5-folds and models
	for i in models_rev_b:
		for j in i['test_roc_auc']:
			diff.append(abs(r-j))
	col1 = np.argmin(diff) + 1				# Picking up that fold which returns same roc-auc score as average roc-auc score

	diff1 = []
	r = sum(ROC_T)/len(ROC_T)				# Average roc-auc score for textual features over all 5-folds and models
	for i in models_rev_t:
		for j in i['test_roc_auc']:
			diff1.append(abs(r-j))
	col2 = np.argmin(diff1) + 1				# Picking up that fold which returns same roc-auc score as average roc-auc score

	# Reading FPR and TPR values ..............................................
	fpr_rev_b.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Review Behavioral\\'+str(cls[k])+'\\FPR_TPR_Threshold_Review_Behavioral.xlsx', sheetname=0, header= None, parse_cols =[col1,col1])))		# Change the path according to the file location
	tpr_rev_b.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Review Behavioral\\'+str(cls[k])+'\\FPR_TPR_Threshold_Review_Behavioral.xlsx', sheetname=1, header= None, parse_cols =[col1,col1])))		# Change the path according to the file location
	fpr_rev_t.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Review Textual\\'+str(cls[k])+'\\FPR_TPR_Threshold_Review_Textual.xlsx', sheetname=0, header= None, parse_cols =[col2,col2])))				# Change the path according to the file location
	tpr_rev_t.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Review Textual\\'+str(cls[k])+'\\FPR_TPR_Threshold_Review_Textual.xlsx', sheetname=1, header= None, parse_cols =[col2,col2])))				# Change the path according to the file location

# Reading model objects as returned by model training phase ...............
# Product-Centric Setting ................................................
fpr_prod_b = []
fpr_prod_t = []
tpr_prod_b = []
tpr_prod_t = []
for k in range(0, len(cls)):
	models_prod_b = []
	models_prod_t = []
	for u in range(0,2):
		models_prod_b.append(pickle.load(open('Data\\Results\\YelpZip\\Product Behavioral\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))	# Change the path according to the file location
	for u in range(0,2):
		models_prod_t.append(pickle.load(open('Data\\Results\\YelpZip\\Product Textual\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))		# Change the path according to the file location

	ROC_B = []
	ROC_T = []
	for m in models_prod_b:
		ROC_B.append(sum(m['test_roc_auc'])/float(len(m['test_roc_auc'])))
	for m in models_prod_t:
		ROC_T.append(sum(m['test_roc_auc'])/float(len(m['test_roc_auc'])))

	diff = []
	r = sum(ROC_B)/len(ROC_B)				# Average roc-auc score for behavioral features over all 5-folds and models
	for i in models_prod_b:
		for j in i['test_roc_auc']:
			diff.append(abs(r-j))
	col1 = np.argmin(diff) + 1				# Picking up that fold which returns same roc-auc score as average roc-auc score

	diff1 = []
	r = sum(ROC_T)/len(ROC_T)				# Average roc-auc score for textual features over all 5-folds and models
	for i in models_prod_t:
		for j in i['test_roc_auc']:
			diff1.append(abs(r-j))
	col2 = np.argmin(diff1) + 1				# Picking up that fold which returns same roc-auc score as average roc-auc score

	# Reading FPR and TPR values ..............................................
	fpr_prod_b.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Product Behavioral\\'+str(cls[k])+'\\FPR_TPR_Threshold_Product_Behavioral.xlsx', sheetname=0, header= None, parse_cols =[col1,col1])))		# Change the path according to the file location
	tpr_prod_b.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Product Behavioral\\'+str(cls[k])+'\\FPR_TPR_Threshold_Product_Behavioral.xlsx', sheetname=1, header= None, parse_cols =[col1,col1])))		# Change the path according to the file location
	fpr_prod_t.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Product Textual\\'+str(cls[k])+'\\FPR_TPR_Threshold_Product_Textual.xlsx', sheetname=0, header= None, parse_cols =[col2,col2])))				# Change the path according to the file location
	tpr_prod_t.append(np.array(pd.read_excel('Data\\Results\\YelpZip\\Product Textual\\'+str(cls[k])+'\\FPR_TPR_Threshold_Product_Textual.xlsx', sheetname=1, header= None, parse_cols =[col2,col2])))				# Change the path according to the file location

	
# Plotting ROC Curves .....................................................
# Reviewer-Centric Setting ................................................
i = 331
for k in range(0, len(cls)):
	plt.subplot(i)
	plt.title('ROC for Reviewer-centric Setting',fontsize=10)
	roc_auc_b = auc(fpr_revr_b[k],tpr_revr_b[k])
	roc_auc_t = auc(fpr_revr_t[k],tpr_revr_t[k])
	plt.plot(fpr_revr_b[k], tpr_revr_b[k], 'c',linewidth=0.8,label='Behavioral (AUC = %0.2f)'% roc_auc_b)
	plt.plot(fpr_revr_t[k], tpr_revr_t[k], 'r',linewidth=0.8,label='Textual (AUC = %0.2f)'% roc_auc_t)
	plt.legend(loc='lower right',prop={'size':8})
	plt.plot([0,1],[0,1],'--',color = 'lightgray', linewidth=0.8)
	plt.xlim([0.0,1.0])
	plt.ylim([0.0,1.0])
	plt.ylabel('True Positive Rate',fontsize=8)
	plt.xlabel('(a) False Positive Rate',fontsize=8)
	props = dict(boxstyle='round', facecolor='white', alpha=0.3)
	plt.text(0.05, 0.9, cls[k], fontsize=8,verticalalignment='top', bbox=props)
	i=i+1

# Review-Centric Setting ................................................
for k in range(0, len(cls)):
	plt.subplot(i)
	plt.title('ROC for Review-centric Setting',fontsize=10)
	roc_auc_b = auc(fpr_rev_b[k],tpr_rev_b[k])
	roc_auc_t = auc(fpr_rev_t[k],tpr_rev_t[k])
	plt.plot(fpr_rev_b[k], tpr_rev_b[k], 'c',linewidth=0.8,label='Behavioral (AUC = %0.2f)'% roc_auc_b)
	plt.plot(fpr_rev_t[k], tpr_rev_t[k], 'r',linewidth=0.8,label='Textual (AUC = %0.2f)'% roc_auc_t)
	plt.legend(loc='lower right',prop={'size':8})
	plt.plot([0,1],[0,1],'--',color = 'lightgray', linewidth=0.8)
	plt.xlim([0.0,1.0])
	plt.ylim([0.0,1.0])
	plt.ylabel('True Positive Rate',fontsize=8)
	plt.xlabel('(b) False Positive Rate',fontsize=8)
	props = dict(boxstyle='round', facecolor='white', alpha=0.3)
	plt.text(0.05, 0.9, cls[k], fontsize=8,verticalalignment='top', bbox=props)
	i=i+1

# Product-Centric Setting ................................................
for k in range(0, len(cls)):
	plt.subplot(i)
	plt.title('ROC for Product-centric Setting',fontsize=10)
	roc_auc_b = auc(fpr_prod_b[k],tpr_prod_b[k])
	roc_auc_t = auc(fpr_prod_t[k],tpr_prod_t[k])
	plt.plot(fpr_prod_b[k], tpr_prod_b[k], 'c',linewidth=0.8,label='Behavioral (AUC = %0.2f)'% roc_auc_b)
	plt.plot(fpr_prod_t[k], tpr_prod_t[k], 'r',linewidth=0.8,label='Textual (AUC = %0.2f)'% roc_auc_t)
	plt.legend(loc='lower right',prop={'size':8})
	plt.plot([0,1],[0,1],'--',color = 'lightgray', linewidth=0.8)
	plt.xlim([0.0,1.0])
	plt.ylim([0.0,1.0])
	plt.ylabel('True Positive Rate',fontsize=8)
	plt.xlabel('(c) False Positive Rate',fontsize=8)
	props = dict(boxstyle='round', facecolor='white', alpha=0.3)
	plt.text(0.05, 0.9, cls[k], fontsize=8,verticalalignment='top', bbox=props)
	i=i+1
plt.show()

