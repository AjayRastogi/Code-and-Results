import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

cls = ['SVM','LR','MLP']
# Reading model objects as returned by model training phase ...............
# Reviewer-Centric Setting ................................................
AP_final = []
F1_final = []
ROC_final = []

for k in range(0,len(cls)):
	models_b = []
	models_t = []
	models_h = []

	for u in range(0,10):
			models_b.append(pickle.load(open('Data\\Results\\YelpZip\\Reviewer Behavioral\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))		# Change the path according to the file location
	for u in range(0,10):
			models_t.append(pickle.load(open('Data\\Results\\YelpZip\\Reviewer Textual\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))			# Change the path according to the file location
	for u in range(0,10):
			models_h.append(pickle.load(open('Data\\Results\\YelpZip\\Reviewer Hybrid\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))			# Change the path according to the file location
	ap=[]
	f1=[]
	roc=[]
	for m in models_h:
		ap.append(sum(m['test_ap'])/len(m['test_ap']))
		f1.append(sum(m['test_f1_macro'])/len(m['test_f1_macro']))
		roc.append(sum(m['test_roc_auc'])/len(m['test_roc_auc']))
	AP=[]
	ROC=[]
	F1=[]
	AP.append(sum(ap)/float(len(ap)))
	ROC.append(sum(roc)/float(len(roc)))
	F1.append(sum(f1)/float(len(f1)))
	
	ap=[]
	f1=[]
	roc=[]
	for m in models_b:
		ap.append(sum(m['test_ap'])/len(m['test_ap']))
		f1.append(sum(m['test_f1_macro'])/len(m['test_f1_macro']))
		roc.append(sum(m['test_roc_auc'])/len(m['test_roc_auc']))
	AP.append(sum(ap)/float(len(ap)))
	ROC.append(sum(roc)/float(len(roc)))
	F1.append(sum(f1)/float(len(f1)))
	
	ap=[]
	f1=[]
	roc=[]
	for m in models_t:
		ap.append(sum(m['test_ap'])/len(m['test_ap']))
		f1.append(sum(m['test_f1_macro'])/len(m['test_f1_macro']))
		roc.append(sum(m['test_roc_auc'])/len(m['test_roc_auc']))
	AP.append(sum(ap)/float(len(ap)))
	ROC.append(sum(roc)/float(len(roc)))
	F1.append(sum(f1)/float(len(f1)))
	
	AP_final.append(AP)
	F1_final.append(F1)
	ROC_final.append(ROC)

# Reading model objects as returned by model training phase ...............
# Review-Centric Setting ................................................
AP_final1 = []
F1_final1 = []
ROC_final1 = []

for k in range(0,len(cls)):
	models_b = []
	models_t = []
	models_h = []

	for u in range(0,21):
			models_b.append(pickle.load(open('Data\\Results\\YelpZip\\Review Behavioral\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))		# Change the path according to the file location
	for u in range(0,21):
			models_t.append(pickle.load(open('Data\\Results\\YelpZip\\Review Textual\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))			# Change the path according to the file location
	for u in range(0,21):
			models_h.append(pickle.load(open('Data\\Results\\YelpZip\\Review Hybrid\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))			# Change the path according to the file location
	ap=[]
	f1=[]
	roc=[]
	for m in models_h:
		ap.append(sum(m['test_ap'])/len(m['test_ap']))
		f1.append(sum(m['test_f1_macro'])/len(m['test_f1_macro']))
		roc.append(sum(m['test_roc_auc'])/len(m['test_roc_auc']))
	AP=[]
	ROC=[]
	F1=[]
	AP.append(sum(ap)/float(len(ap)))
	ROC.append(sum(roc)/float(len(roc)))
	F1.append(sum(f1)/float(len(f1)))
	
	ap=[]
	f1=[]
	roc=[]
	for m in models_b:
		ap.append(sum(m['test_ap'])/len(m['test_ap']))
		f1.append(sum(m['test_f1_macro'])/len(m['test_f1_macro']))
		roc.append(sum(m['test_roc_auc'])/len(m['test_roc_auc']))
	AP.append(sum(ap)/float(len(ap)))
	ROC.append(sum(roc)/float(len(roc)))
	F1.append(sum(f1)/float(len(f1)))
	
	ap=[]
	f1=[]
	roc=[]
	for m in models_t:
		ap.append(sum(m['test_ap'])/len(m['test_ap']))
		f1.append(sum(m['test_f1_macro'])/len(m['test_f1_macro']))
		roc.append(sum(m['test_roc_auc'])/len(m['test_roc_auc']))
	AP.append(sum(ap)/float(len(ap)))
	ROC.append(sum(roc)/float(len(roc)))
	F1.append(sum(f1)/float(len(f1)))
	
	AP_final1.append(AP)
	F1_final1.append(F1)
	ROC_final1.append(ROC)

# Reading model objects as returned by model training phase ...............
# Product-Centric Setting ................................................
AP_final2 = []
F1_final2 = []
ROC_final2 = []

for k in range(0,len(cls)):
	models_b = []
	models_t = []
	models_h = []

	for u in range(0,8):
			models_b.append(pickle.load(open('Data\\Results\\YelpZip\\Product Behavioral\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))		# Change the path according to the file location
	for u in range(0,8):
			models_t.append(pickle.load(open('Data\\Results\\YelpZip\\Product Textual\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))		# Change the path according to the file location
	for u in range(0,8):
			models_h.append(pickle.load(open('Data\\Results\\YelpZip\\Product Hybrid\\'+str(cls[k])+'\\Model_'+str(u+1)+'.sav', 'rb')))			# Change the path according to the file location
	ap=[]
	f1=[]
	roc=[]
	for m in models_h:
		ap.append(sum(m['test_ap'])/len(m['test_ap']))
		f1.append(sum(m['test_f1_macro'])/len(m['test_f1_macro']))
		roc.append(sum(m['test_roc_auc'])/len(m['test_roc_auc']))
	AP=[]
	ROC=[]
	F1=[]
	AP.append(sum(ap)/float(len(ap)))
	ROC.append(sum(roc)/float(len(roc)))
	F1.append(sum(f1)/float(len(f1)))
	
	ap=[]
	f1=[]
	roc=[]
	for m in models_b:
		ap.append(sum(m['test_ap'])/len(m['test_ap']))
		f1.append(sum(m['test_f1_macro'])/len(m['test_f1_macro']))
		roc.append(sum(m['test_roc_auc'])/len(m['test_roc_auc']))
	AP.append(sum(ap)/float(len(ap)))
	ROC.append(sum(roc)/float(len(roc)))
	F1.append(sum(f1)/float(len(f1)))
	
	ap=[]
	f1=[]
	roc=[]
	for m in models_t:
		ap.append(sum(m['test_ap'])/len(m['test_ap']))
		f1.append(sum(m['test_f1_macro'])/len(m['test_f1_macro']))
		roc.append(sum(m['test_roc_auc'])/len(m['test_roc_auc']))
	AP.append(sum(ap)/float(len(ap)))
	ROC.append(sum(roc)/float(len(roc)))
	F1.append(sum(f1)/float(len(f1)))
	
	AP_final2.append(AP)
	F1_final2.append(F1)
	ROC_final2.append(ROC)

# Plotting Bar Charts for AP, F1 and ROC-AUC ..............................
# Reviewer-Centric Setting ................................................
i = 331
x = np.arange(len(cls))
width = 0.2
plt.subplot(i)
data = np.array(AP_final)
plt.bar(x, data[:,0], width, color='b', label = 'Hybrid')
plt.bar(x+0.02+width, data[:,1], width, color='C1', label = 'Behavioral')
plt.bar(x+0.04+(2 * width), data[:,2], width, color='C7', label = 'Textual')
plt.ylabel('Avg. Precision')
plt.xlabel('(a)')
plt.xticks(x+width, cls)
plt.ylim([0.4,0.8])
plt.yticks(np.arange(0.4,1.0,step=0.2))
i=i+1

plt.subplot(i)
data = np.array(F1_final)
plt.bar(x, data[:,0], width, color='b', label = 'Hybrid')
plt.bar(x+0.02+width, data[:,1], width, color='C1', label = 'Behavioral')
plt.bar(x+0.04+(2 * width), data[:,2], width, color='C7', label = 'Textual')
plt.ylabel('F$1$–Score')
plt.xlabel('(a)')
plt.xticks(x+width, cls)
plt.ylim([0.4,0.8])
plt.yticks(np.arange(0.4,1.0,step=0.2))
i=i+1

plt.subplot(i)
data = np.array(ROC_final)
plt.bar(x, data[:,0], width, color='b', label = 'Hybrid')
plt.bar(x+0.02+width, data[:,1], width, color='C1', label = 'Behavioral')
plt.bar(x+0.04+(2 * width), data[:,2], width, color='C7', label = 'Textual')
plt.ylabel('ROC-AUC')
plt.xlabel('(a)')
plt.xticks(x+width, cls)
plt.ylim([0.4,0.8])
plt.yticks(np.arange(0.4,1.0,step=0.2))
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
i=i+1

# Review-Centric Setting ................................................
plt.subplot(i)
data = np.array(AP_final1)
plt.bar(x, data[:,0], width, color='b', label = 'Hybrid')
plt.bar(x+0.02+width, data[:,1], width, color='C1', label = 'Behavioral')
plt.bar(x+0.04+(2 * width), data[:,2], width, color='C7', label = 'Textual')
plt.ylabel('Avg. Precision')
plt.xlabel('(b)')
plt.xticks(x+width, cls)
plt.ylim([0.4,0.8])
plt.yticks(np.arange(0.4,1.0,step=0.2))
i=i+1

plt.subplot(i)
data = np.array(F1_final1)
plt.bar(x, data[:,0], width, color='b', label = 'Hybrid')
plt.bar(x+0.02+width, data[:,1], width, color='C1', label = 'Behavioral')
plt.bar(x+0.04+(2 * width), data[:,2], width, color='C7', label = 'Textual')
plt.ylabel('F$1$–Score')
plt.xlabel('(b)')
plt.xticks(x+width, cls)
plt.ylim([0.4,0.8])
plt.yticks(np.arange(0.4,1.0,step=0.2))
i=i+1

plt.subplot(i)
data = np.array(ROC_final1)
plt.bar(x, data[:,0], width, color='b', label = 'Hybrid')
plt.bar(x+0.02+width, data[:,1], width, color='C1', label = 'Behavioral')
plt.bar(x+0.04+(2 * width), data[:,2], width, color='C7', label = 'Textual')
plt.ylabel('ROC-AUC')
plt.xlabel('(b)')
plt.xticks(x+width, cls)
plt.ylim([0.4,0.8])
plt.yticks(np.arange(0.4,1.0,step=0.2))
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
i=i+1

# Product-Centric Setting ................................................
plt.subplot(i)
data = np.array(AP_final2)
plt.bar(x, data[:,0], width, color='b', label = 'Hybrid')
plt.bar(x+0.02+width, data[:,1], width, color='C1', label = 'Behavioral')
plt.bar(x+0.04+(2 * width), data[:,2], width, color='C7', label = 'Textual')
plt.ylabel('Avg. Precision')
plt.xlabel('(c)')
plt.xticks(x+width, cls)
plt.ylim([0.4,0.8])
plt.yticks(np.arange(0.4,1.0,step=0.2))
i=i+1

plt.subplot(i)
data = np.array(F1_final2)
plt.bar(x, data[:,0], width, color='b', label = 'Hybrid')
plt.bar(x+0.02+width, data[:,1], width, color='C1', label = 'Behavioral')
plt.bar(x+0.04+(2 * width), data[:,2], width, color='C7', label = 'Textual')
plt.ylabel('F$1$–Score')
plt.xlabel('(c)')
plt.xticks(x+width, cls)
plt.ylim([0.4,0.8])
plt.yticks(np.arange(0.4,1.0,step=0.2))
i=i+1

plt.subplot(i)
data = np.array(ROC_final2)
plt.bar(x, data[:,0], width, color='b', label = 'Hybrid')
plt.bar(x+0.02+width, data[:,1], width, color='C1', label = 'Behavioral')
plt.bar(x+0.04+(2 * width), data[:,2], width, color='C7', label = 'Textual')
plt.ylabel('ROC-AUC')
plt.xlabel('(c)')
plt.xticks(x+width, cls)
plt.ylim([0.4,0.8])
plt.yticks(np.arange(0.4,1.0,step=0.2))
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
i=i+1

plt.show()
