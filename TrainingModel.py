import matplotlib

import pandas as pd
import numpy as np
#matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.metrics import average_precision_score, confusion_matrix
from xgboost.sklearn import XGBClassifier
from xgboost import plot_importance, to_graphviz
import xgboost as xgb
import warnings
#from graphviz import Source
import pickle


warnings.filterwarnings("ignore", category=DeprecationWarning)

df = pd.read_csv('filtered_data.csv')
df = df.rename(columns={'oldbalanceOrg':'oldBalanceOrig', 'newbalanceOrig':'newBalanceOrig', \
                        'oldbalanceDest':'oldBalanceDest', 'newbalanceDest':'newBalanceDest'})
print(df.head())
print(df.isnull().values.any())

######## DATA  CLEANING ##############

X = df.loc[(df.type == 'TRANSFER') | (df.type == 'CASH_OUT')]

randomState = 5
np.random.seed(randomState)



#X = X.loc[np.random.choice(X.index, 100000, replace = False)]

Y = X['isFraud']
del X['isFraud']

# Eliminate columns shown to be irrelevant for analysis in the EDA
X = X.drop(['isFlaggedFraud'], axis = 1)

# Binary-encoding of labelled data in 'type'
X.loc[X.type == 'TRANSFER', 'type'] = 0
X.loc[X.type == 'CASH_OUT', 'type'] = 1
X.type = X.type.astype(int) # convert dtype('O') to dtype(int)

Xfraud = X.loc[Y == 1]
XnonFraud = X.loc[Y == 0]


######### Data-Cleaning for ML #########

# if oldDestBalance == 0 && newDestBalance == 0 Replace it with -1 for ML
X.loc[(X.oldBalanceDest == 0) & (X.newBalanceDest == 0) & (X.amount != 0), \
      ['oldBalanceDest', 'newBalanceDest']] = - 1

# if oldOrigBalance == 0 && newOrigBalance == 0 Replace it with null for ML
X.loc[(X.oldBalanceOrig == 0) & (X.newBalanceOrig == 0) & (X.amount != 0), \
      ['oldBalanceOrig', 'newBalanceOrig']] = np.nan

######### Feature-engineering #########

X['errorBalanceOrig'] = X.newBalanceOrig + X.amount - X.oldBalanceOrig
X['errorBalanceDest'] = X.oldBalanceDest + X.amount - X.newBalanceDest
## Removing charcter from des and orig name and encode it as int ##
X.loc[X.nameOrig.str.contains('C'),'nameOrig'] = X.nameOrig.str.replace('C','')
X.loc[X.nameDest.str.contains('C'),'nameDest'] = X.nameDest.str.replace('C','')
X.nameOrig = X.nameOrig.astype(int)
X.nameDest = X.nameDest.astype(int)
## Adding Average transaction to each client ##
X['AvgAmountOfTransaction'] = 0
AfterNameDestList = []
afterDestSet = {}
for index, row in X.iterrows():
    AfterNameDestList.append(row['nameDest'])

afterDestSet = set(AfterNameDestList)
for name in afterDestSet:
   X.loc[X['nameDest'] == name, 'AvgAmountOfTransaction'] = X.loc[X.nameDest == name].amount.mean()



######## Machine Learning ###########
trainX, testX, trainY, testY = train_test_split(X, Y, test_size = 0.3, \
                                                random_state = randomState)
# Long computation in this cell (~1.8 minutes)
weights = (Y == 0).sum() / (1.0 * (Y == 1).sum())
clf = XGBClassifier(max_depth = 3, scale_pos_weight = weights, \
                n_jobs = 4)
clf.fit(trainX, trainY)
predict = clf.predict(testX)
print('Predict', predict)

######## SAVE THE MODEL  ###########
'''fileName = 'SMI_MODEL.sav'
pickle.dump(clf, open(fileName,'wb'))'''


######## LOAD THE MODEL  ###########

'''loaded_model = pickle.load(open('SMI_MODEL.sav', 'rb'))
predict = loaded_model.predict(testX)'''

''''### Save testing data into one frame ####
df_testing = pd.DataFrame(testX)
df_testing['isFruad'] = testY

dfFraudTesting = df_testing.loc[(df.isFraud == 1)]

### Printing Suspicious Transactions in the testing dataset  ####
print('Suspicious Transactions in testing data set:')
print(dfFraudTesting)

### Saving testing dataset ###
df_testing.to_csv('testingData.csv', encoding='utf-8', index=False)


### Merge prediction column to the rest of the columns and save it in one data frame####
dt_result = pd.DataFrame(testX)
dt_result['isFruad_result']=predict
dt_result.to_csv('predictionResult.csv', encoding='utf-8', index=False)



suspiciousTransactions = dt_result.loc[(dt_result.isFruad_result == 1)]
suspiciousTransactions.to_csv('suspiciousTransactions.csv', encoding='utf-8', index=False)

### Printing Suspicious Transactions that the model flagged it as fraud  ####

print('Suspicious Transactions the model predicted:')
print(suspiciousTransactions)

### Visulazution ###

fig = plt.figure(figsize=(14, 9))
ax = fig.add_subplot(111)

colours = plt.cm.Set1(np.linspace(0, 1, 9))

ax = plot_importance(clf, height=1, color=colours, grid=False, \
                     show_values=False, importance_type='cover', ax=ax);
for axis in ['top', 'bottom', 'left', 'right']:
    ax.spines[axis].set_linewidth(2)

ax.set_xlabel('importance score', size=16);
ax.set_ylabel('features', size=16);
ax.set_yticklabels(ax.get_yticklabels(), size=12);
ax.set_title('Ordering of features by importance to the model learnt', size=20);
plt.show()

cm = confusion_matrix(testY,predict)



plt.clf()
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Wistia)
classNames = ['Negative','Positive']
plt.title('Confusion Matrix - Test Data')
plt.ylabel('True label')
plt.xlabel('Predicted label')
tick_marks = np.arange(len(classNames))
plt.xticks(tick_marks, classNames, rotation=45)
plt.yticks(tick_marks, classNames)
s = [['TN','FP'], ['FN', 'TP']]
for i in range(2):
    for j in range(2):
        plt.text(j,i, str(s[i][j])+" = "+str(cm[i][j]))
plt.show()


def plotStrip(x, y, hue, figsize=(14, 9)):
    fig = plt.figure(figsize=figsize)
    colours = plt.cm.tab10(np.linspace(0, 1, 9))
    with sns.axes_style('ticks'):
        ax = sns.stripplot(x, y, \
                           hue=hue, jitter=0.4, marker='.', \
                           size=4, palette=colours)
        ax.set_xlabel('')
        ax.set_xticklabels(['genuine', 'fraudulent'], size=16)
        for axis in ['top', 'bottom', 'left', 'right']:
            ax.spines[axis].set_linewidth(2)

        handles, labels = ax.get_legend_handles_labels()
        plt.legend(handles, ['Transfer', 'Cash out'], bbox_to_anchor=(1, 1), \
                   loc=2, borderaxespad=0, fontsize=16);
    return ax



xgb.plot_tree(clf,num_trees=3)
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(150, 100)
fig.savefig('tree.png') '''
