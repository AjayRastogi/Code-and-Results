import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel('Data\\Results\\YelpZip\\Computation Time.xlsx')			# Change the path according to the file location
df1 = pd.read_excel('Data\\Results\\YelpNYC\\Computation Time.xlsx')		# Change the path according to the file location
Behavioral_yelpzip = np.array(df['Behavioral'])
Textual_yelpzip = np.array(df['Textual'])
Behavioral_yelpnyc = np.array(df1['Behavioral'])
Textual_yelpnyc = np.array(df1['Textual'])

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = float(rect.get_height())
        plt.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%0.3f' % float(height),
                ha='center', va='bottom')

# Plotting bar charts for computation time.................................
# YelpZip Dataset .........................................................
i = 121
cat = list(df.index)
x = np.arange(len(cat))
width = 0.2
plt.subplot(i)
plt.title('YelpZip',fontsize=10)
rects1 = plt.bar(x, Behavioral_yelpzip, width, color='b', label = 'Behavioral')
rects2 = plt.bar(x+0.02+width, Textual_yelpzip, width, color='C1', label = 'Textual')
plt.ylabel('Time\n(in seconds)\n(x 1000)')
plt.xlabel('(a)')
plt.grid(which='major', axis = 'y',linestyle='-', linewidth='0.5', color='lightgray')
plt.ylim([0,28])
plt.yticks(np.arange(0,29,step=4))
plt.xticks(x+width-0.08, cat)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=2)
autolabel(rects1)
autolabel(rects2)
i=i+1

# YelpNYC Dataset .........................................................
plt.subplot(i)
plt.title('YelpNYC',fontsize=10)
rects3 = plt.bar(x, Behavioral_yelpnyc, width, color='b', label = 'Behavioral')
rects4 = plt.bar(x+0.02+width, Textual_yelpnyc, width, color='C1', label = 'Textual')
plt.ylabel('Time\n(in seconds)\n(x 1000)')
plt.xlabel('(b)')
plt.grid(which='major', axis = 'y',linestyle='-', linewidth='0.5', color='lightgray')
plt.ylim([0,8])
plt.yticks(np.arange(0,9,step=2))
plt.xticks(x+width-0.08, cat)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=2)
autolabel(rects3)
autolabel(rects4)

plt.show()
