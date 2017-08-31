
# coding: utf-8

# In[1]:

#from __future__ import print_function
import os
import subprocess
import sys
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

def get_code(tree, feature_names, target_names,
             spacer_base="    "):
    """Produce psuedo-code for decision tree.

    Args
    ----
    tree -- scikit-leant DescisionTree.
    feature_names -- list of feature names.
    target_names -- list of target (class) names.
    spacer_base -- used for spacing code (default: "    ").

    Notes
    -----
    based on http://stackoverflow.com/a/30104792.
    """
    left      = tree.tree_.children_left
    right     = tree.tree_.children_right
    threshold = tree.tree_.threshold
    features  = [feature_names[i] for i in tree.tree_.feature]
    value = tree.tree_.value

    def recurse(left, right, threshold, features, node, depth):
        spacer = spacer_base * depth
        if (threshold[node] != -2):
            print(spacer + "if ( " + features[node] + " <= " + \
                  str(threshold[node]) + " ) {")
            if left[node] != -1:
                    recurse(left, right, threshold, features,
                            left[node], depth+1)
            print(spacer + "}\n" + spacer +"else {")
            if right[node] != -1:
                    recurse(left, right, threshold, features,
                            right[node], depth+1)
            print(spacer + "}")
        else:
            target = value[node]
            for i, v in zip(np.nonzero(target)[1],
                            target[np.nonzero(target)]):
                target_name = target_names[i]
                target_count = int(v)
                print(spacer + "return " + str(target_name) + \
                      " ( " + str(target_count) + " examples )")

    recurse(left, right, threshold, features, 0, 0)


def define_pjpf( row ):
	if row['FIRST_NAME'] == 'PJ':
		return 'PJ'
	else:
		return 'PF'

def visualize_tree(tree, feature_names, plusname):
	"""Create tree png using graphviz.

	Args
	----
	tree -- scikit-learn DecsisionTree.
	feature_names -- list of feature names.
	"""
	with open("dt-"+plusname+".dot", 'w') as f:
		export_graphviz(tree, out_file=f, feature_names=feature_names)

	command = ["dot", "-Tpng", "dt-"+plusname+".dot", "-o", "dt-"+plusname+".png"]
	try:
		subprocess.check_call(command)
	except:
		exit("Could not run dot, ie graphviz, to produce visualization")

def encode_target(df, target_column):
	"""Add column to df with integers for the target.
	
	Args
	----
	df -- pandas DataFrame.
	target_column -- column to map to int, producing
	                 new Target column.
	
	Returns
	-------
	df_mod -- modified DataFrame.
	targets -- list of target names.
	"""
	df_mod = df.copy()
	targets = df_mod[target_column].unique()
	map_to_int = {name: n for n, name in enumerate(targets)}
	df_mod["Target"] = df_mod[target_column].replace(map_to_int)

	return (df_mod, targets)

resultados = pd.read_csv("resultados.csv")
#print resultados.info()
#print resultados.groupby("TITLE").size().reset_index()



appr = resultados[resultados.RESULT == 'APPROVED']
defeat = resultados[resultados.RESULT == 'DEFEATED']


appr.head(15)

defeat.head(10)

pAllProp = pd.read_csv("all_prop.csv")
#print pAllProp.info()


resTotAllProp = pd.merge(left=resultados, right=pAllProp, left_on='ID_PROPOSITION', right_on='ID_PROPOSITION')
#print resTotAllProp.info()
#print resTotAllProp.head(15)

resTotAllProp.drop(['FILING_ID','TYPE','TITLE','SUBJECT', 'DESCRIPTION', 'COMMITTEE_ID', 'AMEND_ID', 'CITY', 'STATE', 'ZIPCODE', 'EMPLOYER', 'OCCUPATION', 'DATE'], axis=1, inplace=True)
#print resTotAllProp.info()
#print resTotAllProp.head(15)
"""
TYPE                  86786 non-null object
TITLE                 86786 non-null object
SUBJECT               86786 non-null object
DESCRIPTION           86786 non-null object
RESULT                86786 non-null object
ID_PROPOSITION        86786 non-null int64
FILING_ID             86786 non-null int64
COMMITTEE_ID          86786 non-null int64
COMMITTEE_NAME        86786 non-null object
COMMITTEE_POSITION    86786 non-null object
AMEND_ID              86786 non-null int64
FIRST_NAME            83652 non-null object
LAST_NAME             86786 non-null object
CITY                  86773 non-null object
STATE                 86766 non-null object
ZIPCODE               86770 non-null object
EMPLOYER              80993 non-null object
OCCUPATION            83576 non-null object
DATE                  86786 non-null object
AMOUNT                86786 non-null float64

pAllSumContrib = pAll.groupby(['COMMITTEE_POSITION', 'WHO'])[["AMOUNT"]].sum()
pAllMeanContrib = pAll.groupby(['COMMITTEE_POSITION', 'WHO'])[["AMOUNT"]].mean()
pAll.groupby(['COMMITTEE_POSITION', 'WHO','ID_PROPOSITION'])[["AMOUNT"]].sum().reset_index()
pAll.groupby(['COMMITTEE_POSITION', 'WHO','ID_PROPOSITION']).agg(['count']).reset_index()
"""

###TRANSFORMA E CRIA COLUNA WHO
resTotAllProp['FIRST_NAME'].fillna('PJ', inplace=True)
resTotAllProp['WHO'] = resTotAllProp.apply( lambda row: define_pjpf( row ), axis=1)
#print resTotAllProp.info()
#print resTotAllProp.head(15)

resTotAllProp.drop(['FIRST_NAME','LAST_NAME','COMMITTEE_NAME'], axis=1, inplace=True)

print resTotAllProp.info()
print resTotAllProp.head(15)

#pAllSumContrib = resTotAllProp.groupby(['COMMITTEE_POSITION', 'WHO'])[["AMOUNT"]].sum()
#pAllMeanContrib = resTotAllProp.groupby(['COMMITTEE_POSITION', 'WHO'])[["AMOUNT"]].mean()
AllSum = resTotAllProp.groupby(['COMMITTEE_POSITION', 'WHO', 'RESULT'])[["AMOUNT"]].sum().reset_index()
AllQntd = resTotAllProp.groupby(['COMMITTEE_POSITION', 'WHO', 'RESULT']).agg(['count']).reset_index()
ByPropAllSum = resTotAllProp.groupby(['COMMITTEE_POSITION', 'WHO', 'RESULT','ID_PROPOSITION'])[["AMOUNT"]].sum().reset_index()
ByPropAllQntd = resTotAllProp.groupby(['COMMITTEE_POSITION', 'WHO', 'RESULT','ID_PROPOSITION']).agg(['count']).reset_index()
#AllQntdMean = resTotAllProp.groupby(['COMMITTEE_POSITION', 'WHO', 'RESULT']).agg(['count']).mean().reset_index()

#print pAllSumContrib
#print pAllMeanContrib

print AllSum
print AllQntd
#print ByPropAllSum
#print ByPropAllQntd
"""
Nao recomendado
BinresTotAllProp = pd.merge(left=ByPropAllSum, right=ByPropAllQntd, left_on=['ID_PROPOSITION','COMMITTEE_POSITION', 'WHO' ], right_on=['ID_PROPOSITION', 'COMMITTEE_POSITION', 'WHO' ] )
print BinresTotAllProp
"""


#ByPropAllSum.to_csv('SumAll.csv')
#ByPropAllQntd.to_csv('QntdAll.csv')
# this will output a file.

pdSumAll = pd.read_csv("SumAll.csv")
pdQntdAll = pd.read_csv("QntdAll.csv")
pdSumAll.drop(pdSumAll.columns[[0]], axis=1, inplace=True )
pdQntdAll.drop(pdQntdAll.columns[[0]], axis=1, inplace=True )
BinresTotAllProp = pd.merge(left=pdSumAll, right=pdQntdAll, left_on=['ID_PROPOSITION','COMMITTEE_POSITION', 'WHO', 'RESULT' ], right_on=['ID_PROPOSITION', 'COMMITTEE_POSITION', 'WHO', 'RESULT' ] )

#BinresTotAllProp = BinresTotAllProp[['COMMITTEE_POSITION','WHO','ID_PROPOSITION','AMOUNT','QNTD', 'RESULT']]
BinresTotAllProp = BinresTotAllProp[['COMMITTEE_POSITION','WHO','AMOUNT','QNTD', 'RESULT']]
print BinresTotAllProp


"""
PREPARaCAO DA ARVORE
"""
enc = LabelEncoder()
label_encoder_CP = enc.fit(BinresTotAllProp.iloc[:, 0])
print "Categorical classes:", label_encoder_CP.classes_
integer_classes_CP = label_encoder_CP.transform(label_encoder_CP.classes_)
print "Integer classes:", integer_classes_CP
t_CP = label_encoder_CP.transform(BinresTotAllProp.iloc[:, 0])
BinresTotAllProp.iloc[:, 0] = t_CP

label_encoder_WHO = enc.fit(BinresTotAllProp.iloc[:, 1])
print "Categorical classes:", label_encoder_WHO.classes_
integer_classes_WHO = label_encoder_WHO.transform(label_encoder_WHO.classes_)
print "Integer classes:", integer_classes_WHO
t_WHO = label_encoder_WHO.transform(BinresTotAllProp.iloc[:, 1])
BinresTotAllProp.iloc[:, 1] = t_WHO


label_encoder_RESULT = enc.fit(BinresTotAllProp.iloc[:, 4])
print "Categorical classes:", label_encoder_RESULT.classes_
integer_classes_RESULT = label_encoder_RESULT.transform(label_encoder_RESULT.classes_)
print "Integer classes:", integer_classes_RESULT
t_RESULT = label_encoder_RESULT.transform(BinresTotAllProp.iloc[:, 4])
BinresTotAllProp.iloc[:, 4] = t_RESULT


print BinresTotAllProp.info()
print BinresTotAllProp.head(3)


features = BinresTotAllProp.columns.difference( ['RESULT'] )
X = BinresTotAllProp[features].values
y = BinresTotAllProp['RESULT'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

dt = DecisionTreeClassifier(random_state=1, criterion='gini', max_depth=5)
dt.fit(X_train, y_train)
y_predict = dt.predict(X_test)

""" PRECISAO com criterio do indice gini """
print "PRECISAO"
print accuracy_score(y_test, y_predict) * 100
print "MATRIX DE CONFUSAO"
print pd.DataFrame( confusion_matrix(y_test, y_predict), columns=['0','1'], index=['0', '1'] )
print ""
print(classification_report(y_test, y_predict))

with open("tree-final20170826.dot", 'w') as f:
	export_graphviz(dt, out_file=f, feature_names=features)
command = ["dot", "-Tpng", "tree-final20170826.dot", "-o", "tree-final20170826.png"]
try:
	subprocess.check_call(command)
except:
	exit("Could not run dot, ie graphviz, to produce visualization")


get_code(dt, ['AMOUNT','COMMITTEE_POSITION','QNTD','WHO'], X)


