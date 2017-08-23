
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

#
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
resultados.info()

resultados.groupby("TITLE").size().reset_index()


# In[9]:


appr = resultados[resultados.RESULT == 'APPROVED']


# In[10]:


defeat = resultados[resultados.RESULT == 'DEFEATED']


# In[11]:


appr.head(15)


# In[12]:


defeat.head(10)


# In[13]:


propTIT51 = resultados[resultados.TITLE == 'PROPOSITION 051 - SCHOOL BONDS. FUNDING FOR K-12 SCHOOL AND COMMUNITY COLLEGE FACILITIES. INITIATIVE STATUTORY AMENDMENT.']


# In[14]:


propTIT51.head()


# In[15]:


propTIT52 = resultados[resultados.TITLE == 'PROPOSITION 052 - STATE FEES ON HOSPITALS. FEDERAL MEDI-CAL MATCHING FUNDS. INITIATIVE STATUTORY AND CONSTITUTIONAL AMENDMENT.']


# In[16]:


propTIT52.head()


# In[17]:


propTIT53 = resultados[resultados.TITLE == 'PROPOSITION 053 - REVENUE BONDS. STATEWIDE VOTER APPROVAL. INITIATIVE CONSTITUTIONAL AMENDMENT.']


# In[18]:


propTIT53.head()


# In[19]:


propTIT64 = resultados[resultados.TITLE == 'PROPOSITION 064- MARIJUANA LEGALIZATION. INITIATIVE STATUTE.']


# In[20]:


propTIT64.head()


# In[21]:


resultados.groupby("SUBJECT").size().reset_index()


# In[22]:


p51 = pd.read_csv("prop_51_contributions.csv")


# In[23]:


p52 = pd.read_csv("prop_52_contributions.csv")


# In[24]:


p53 = pd.read_csv("prop_53_contributions.csv")


# In[25]:


p54 = pd.read_csv("prop_54_contributions.csv")


# In[26]:


p55 = pd.read_csv("prop_55_contributions.csv")


# In[27]:


p56 = pd.read_csv("prop_56_contributions.csv")


# In[28]:


p57 = pd.read_csv("prop_57_contributions.csv")


# In[29]:


p58 = pd.read_csv("prop_58_contributions.csv")


# In[30]:


p59 = pd.read_csv("prop_59_contributions.csv")


# In[31]:


p60 = pd.read_csv("prop_60_contributions.csv")


# In[32]:


p61 = pd.read_csv("prop_61_contributions.csv")


# In[33]:


p62 = pd.read_csv("prop_62_contributions.csv")


# In[34]:


p63 = pd.read_csv("prop_63_contributions.csv")


# In[35]:


p64 = pd.read_csv("prop_64_contributions.csv")


# In[36]:


p65 = pd.read_csv("prop_65_contributions.csv")


# In[37]:


p66 = pd.read_csv("prop_66_contributions.csv")


# In[38]:


p67 = pd.read_csv("prop_67_contributions.csv")


# In[39]:


p51.info()


# In[40]:


p51.COMMITTEE_NAME.value_counts().reset_index()


# In[41]:


p51COMMITTEE_NAME = p51.COMMITTEE_NAME.value_counts()


# In[42]:


p51COMMITTEE_NAME.reset_index()


# In[43]:


p51AMOUNT = p51.groupby("COMMITTEE_NAME").sum()


# In[44]:


p51AMOUNT.reset_index()


# In[ ]:





# In[59]:


#########################################
"""Proposition 51"""
#########################################
resTot51 = pd.merge(left=resultados, right=p51, left_on='ID_PROPOSITION', right_on='ID_PROPOSITION')
resTot51.drop(['FILING_ID','COMMITTEE_ID','AMEND_ID', 'TYPE','CITY', 'STATE', 'ZIPCODE', 'OCCUPATION', 'DATE', 'EMPLOYER', 'DESCRIPTION', 'TITLE', 'COMMITTEE_NAME' ], axis=1, inplace=True)
#print resTot51.count()
cp51 = resTot51.copy()
#print cp51
TOTALcp51 = cp51.AMOUNT.sum()
cp51['PERC'] = cp51['AMOUNT'] / TOTALcp51
#print TOTALcp51
#print cp51
colunas = list(cp51.columns.values)
#print colunas
cp51 = cp51[ ['FIRST_NAME', 'LAST_NAME','SUBJECT', 'RESULT', 'ID_PROPOSITION', 'COMMITTEE_POSITION', 'AMOUNT', 'PERC'] ]
cp51['FIRST_NAME'].fillna('PJ', inplace=True)
cp51['WHO'] = cp51.apply( lambda row: define_pjpf( row ), axis=1)
cp51 = cp51[ ['RESULT', 'AMOUNT', 'PERC', 'COMMITTEE_POSITION', 'ID_PROPOSITION', 'WHO' ] ]
#print cp51

DictCOMMITTEE_POSITION = {'SUPPORT': True, 'OPPOSE': False}
cp51['B_COMMITTEE_POSITION'] = cp51['COMMITTEE_POSITION'].map( DictCOMMITTEE_POSITION )
cp51.drop(['COMMITTEE_POSITION'], axis=1, inplace=True)

DictRESULT = {'APPROVED': True, 'DEFEATED': False}
cp51['B_RESULT'] = cp51['RESULT'].map( DictRESULT )
cp51.drop(['RESULT'], axis=1, inplace=True)
#print cp51.head()

#cp51 = cp51[ ['B_RESULT', 'AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'WHO' ] ]
cp51 = cp51[ ['AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'WHO' ] ]
print "Linhas: %d, Colunas: %d" % (len(cp51), len(cp51.columns))
print cp51['WHO'].value_counts()
print cp51['B_COMMITTEE_POSITION'].value_counts()
### SOMA VALORES AMOUNT COM GROUP BY B_COMMITTEE_POSITION
cp51['B_CONTRIBAboveMean'] = cp51['AMOUNT'] > cp51['AMOUNT'].mean()
cp51 = cp51[ ['AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'B_CONTRIBAboveMean', 'WHO' ] ]
print cp51.head()

features = cp51.columns.difference( ['WHO'] )
X = cp51[features].values
y = cp51['WHO'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

dt = DecisionTreeClassifier(random_state=1986, criterion='gini', max_depth=6)
dt.fit(X_train, y_train)
y_predict = dt.predict(X_test)

""" ACURACIA """
print accuracy_score(y_test, y_predict)

""" MATRIZ DE CONFUSAO """
print pd.DataFrame( confusion_matrix(y_test, y_predict), columns=['Predicted Not Survival','Predicted Survival'], index=['True Nor Survival', 'True Survival'] )
with open("tree-51.dot", 'w') as f:
	export_graphviz(dt, out_file=f, feature_names=features)
command = ["dot", "-Tpng", "tree-51.dot", "-o", "tree-51.png"]
try:
	subprocess.check_call(command)
except:
	exit("Could not run dot, ie graphviz, to produce visualization")



#########################################
"""Proposition 52
#########################################
resTot52 = pd.merge(left=resultados, right=p52, left_on='ID_PROPOSITION', right_on='ID_PROPOSITION')
resTot52.drop(['FILING_ID','COMMITTEE_ID','AMEND_ID', 'TYPE','CITY', 'STATE', 'ZIPCODE', 'OCCUPATION', 'DATE', 'EMPLOYER', 'DESCRIPTION', 'TITLE', 'COMMITTEE_NAME' ], axis=1, inplace=True)
#print resTot52.count()
cp52 = resTot52.copy()
#print cp52
TOTALcp52 = cp52.AMOUNT.sum()
cp52['PERC'] = cp52['AMOUNT'] / TOTALcp52
#print TOTALcp52
#print cp52
colunas = list(cp52.columns.values)
#print colunas
cp52 = cp52[ ['FIRST_NAME', 'LAST_NAME','SUBJECT', 'RESULT', 'ID_PROPOSITION', 'COMMITTEE_POSITION', 'AMOUNT', 'PERC'] ]
cp52['FIRST_NAME'].fillna('PJ', inplace=True)
cp52['WHO'] = cp52.apply( lambda row: define_pjpf( row ), axis=1)
cp52 = cp52[ ['RESULT', 'AMOUNT', 'PERC', 'COMMITTEE_POSITION', 'ID_PROPOSITION', 'WHO' ] ]
#print cp52

DictCOMMITTEE_POSITION = {'SUPPORT': True, 'OPPOSE': False}
cp52['B_COMMITTEE_POSITION'] = cp52['COMMITTEE_POSITION'].map( DictCOMMITTEE_POSITION )
cp52.drop(['COMMITTEE_POSITION'], axis=1, inplace=True)

DictRESULT = {'APPROVED': True, 'DEFEATED': False}
cp52['B_RESULT'] = cp52['RESULT'].map( DictRESULT )
cp52.drop(['RESULT'], axis=1, inplace=True)
#print cp52.head()

#cp52 = cp52[ ['B_RESULT', 'AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'WHO' ] ]
cp52 = cp52[ ['AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'WHO' ] ]
print "Linhas: %d, Colunas: %d" % (len(cp52), len(cp52.columns))
print cp52['WHO'].value_counts()
print cp52['B_COMMITTEE_POSITION'].value_counts()
### SOMA VALORES AMOUNT COM GROUP BY B_COMMITTEE_POSITION
cp52['B_CONTRIBAboveMean'] = cp52['AMOUNT'] > cp52['AMOUNT'].mean()
cp52 = cp52[ ['AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'B_CONTRIBAboveMean', 'WHO' ] ]
print cp52.head()
features = cp52.columns.difference( ['WHO'] )
X = cp52[features].values
y = cp52['WHO'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

dt = DecisionTreeClassifier(random_state=1986, criterion='gini', max_depth=6)
dt.fit(X_train, y_train)
y_predict = dt.predict(X_test)

ACURACIA 
print accuracy_score(y_test, y_predict)

MATRIZ DE CONFUSAO
print pd.DataFrame( confusion_matrix(y_test, y_predict), columns=['Predicted Not Survival','Predicted Survival'], index=['True Nor Survival', 'True Survival'] )
with open("tree-52.dot", 'w') as f:
        export_graphviz(dt, out_file=f, feature_names=features)
command = ["dot", "-Tpng", "tree-52.dot", "-o", "tree-52.png"]
try:
	subprocess.check_call(command)
except:
	exit("Could not run dot, ie graphviz, to produce visualization")
"""

#########################################
"""Proposition 58"""
#########################################
resTot58 = pd.merge(left=resultados, right=p58, left_on='ID_PROPOSITION', right_on='ID_PROPOSITION')
resTot58.drop(['FILING_ID','COMMITTEE_ID','AMEND_ID', 'TYPE','CITY', 'STATE', 'ZIPCODE', 'OCCUPATION', 'DATE', 'EMPLOYER', 'DESCRIPTION', 'TITLE', 'COMMITTEE_NAME' ], axis=1, inplace=True)
#print resTot58.count()
cp58 = resTot58.copy()
#print cp58
TOTALcp58 = cp58.AMOUNT.sum()
cp58['PERC'] = cp58['AMOUNT'] / TOTALcp58
#print TOTALcp58
#print cp58
colunas = list(cp58.columns.values)
#print colunas
cp58 = cp58[ ['FIRST_NAME', 'LAST_NAME','SUBJECT', 'RESULT', 'ID_PROPOSITION', 'COMMITTEE_POSITION', 'AMOUNT', 'PERC'] ]
cp58['FIRST_NAME'].fillna('PJ', inplace=True)
cp58['WHO'] = cp58.apply( lambda row: define_pjpf( row ), axis=1)
cp58 = cp58[ ['RESULT', 'AMOUNT', 'PERC', 'COMMITTEE_POSITION', 'ID_PROPOSITION', 'WHO' ] ]
#print cp58

DictCOMMITTEE_POSITION = {'SUPPORT': True, 'OPPOSE': False}
cp58['B_COMMITTEE_POSITION'] = cp58['COMMITTEE_POSITION'].map( DictCOMMITTEE_POSITION )
cp58.drop(['COMMITTEE_POSITION'], axis=1, inplace=True)

DictRESULT = {'APPROVED': True, 'DEFEATED': False}
cp58['B_RESULT'] = cp58['RESULT'].map( DictRESULT )
cp58.drop(['RESULT'], axis=1, inplace=True)
#print cp58.head()

#cp58 = cp58[ ['B_RESULT', 'AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'WHO' ] ]
cp58 = cp58[ ['AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'WHO' ] ]
print "Linhas: %d, Colunas: %d" % (len(cp58), len(cp58.columns))
print cp58['WHO'].value_counts()
print cp58['B_COMMITTEE_POSITION'].value_counts()
### SOMA VALORES AMOUNT COM GROUP BY B_COMMITTEE_POSITION
cp58['B_CONTRIBAboveMean'] = cp58['AMOUNT'] > cp58['AMOUNT'].mean()
cp58 = cp58[ ['AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'B_CONTRIBAboveMean', 'WHO' ] ]
print cp58.head()
features = cp58.columns.difference( ['WHO'] )
X = cp58[features].values
y = cp58['WHO'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

dt = DecisionTreeClassifier(random_state=1986, criterion='gini', max_depth=6)
dt.fit(X_train, y_train)
y_predict = dt.predict(X_test)

""" ACURACIA """
print accuracy_score(y_test, y_predict)

""" MATRIZ DE CONFUSAO """
print pd.DataFrame( confusion_matrix(y_test, y_predict), columns=['Predicted Not Survival','Predicted Survival'], index=['True Nor Survival', 'True Survival'] )
with open("tree-58.dot", 'w') as f:
        export_graphviz(dt, out_file=f, feature_names=features)
command = ["dot", "-Tpng", "tree-58.dot", "-o", "tree-58.png"]
try:
	subprocess.check_call(command)
except:
	exit("Could not run dot, ie graphviz, to produce visualization")


#########################################
"""Proposition 60"""
#########################################
resTot60 = pd.merge(left=resultados, right=p60, left_on='ID_PROPOSITION', right_on='ID_PROPOSITION')
resTot60.drop(['FILING_ID','COMMITTEE_ID','AMEND_ID', 'TYPE','CITY', 'STATE', 'ZIPCODE', 'OCCUPATION', 'DATE', 'EMPLOYER', 'DESCRIPTION', 'TITLE', 'COMMITTEE_NAME' ], axis=1, inplace=True)
#print resTot60.count()
cp60 = resTot60.copy()
#print cp60
TOTALcp60 = cp60.AMOUNT.sum()
cp60['PERC'] = cp60['AMOUNT'] / TOTALcp60
#print TOTALcp60
#print cp60
colunas = list(cp60.columns.values)
#print colunas
cp60 = cp60[ ['FIRST_NAME', 'LAST_NAME','SUBJECT', 'RESULT', 'ID_PROPOSITION', 'COMMITTEE_POSITION', 'AMOUNT', 'PERC'] ]
cp60['FIRST_NAME'].fillna('PJ', inplace=True)
cp60['WHO'] = cp60.apply( lambda row: define_pjpf( row ), axis=1)
cp60 = cp60[ ['RESULT', 'AMOUNT', 'PERC', 'COMMITTEE_POSITION', 'ID_PROPOSITION', 'WHO' ] ]
#print cp60

DictCOMMITTEE_POSITION = {'SUPPORT': True, 'OPPOSE': False}
cp60['B_COMMITTEE_POSITION'] = cp60['COMMITTEE_POSITION'].map( DictCOMMITTEE_POSITION )
cp60.drop(['COMMITTEE_POSITION'], axis=1, inplace=True)

DictRESULT = {'APPROVED': True, 'DEFEATED': False}
cp60['B_RESULT'] = cp60['RESULT'].map( DictRESULT )
cp60.drop(['RESULT'], axis=1, inplace=True)
#print cp60.head()

#cp60 = cp60[ ['B_RESULT', 'AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'WHO' ] ]
cp60 = cp60[ ['AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'WHO' ] ]
print "Linhas: %d, Colunas: %d" % (len(cp60), len(cp60.columns))
print cp60['WHO'].value_counts()
print cp60['B_COMMITTEE_POSITION'].value_counts()
### SOMA VALORES AMOUNT COM GROUP BY B_COMMITTEE_POSITION
cp60['B_CONTRIBAboveMean'] = cp60['AMOUNT'] > cp60['AMOUNT'].mean()
cp60 = cp60[ ['AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'B_CONTRIBAboveMean', 'WHO' ] ]
print cp60.head()
features = cp60.columns.difference( ['WHO'] )
X = cp60[features].values
y = cp60['WHO'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

dt = DecisionTreeClassifier(random_state=1986, criterion='gini', max_depth=6)
dt.fit(X_train, y_train)
y_predict = dt.predict(X_test)

""" ACURACIA """
print accuracy_score(y_test, y_predict)

""" MATRIZ DE CONFUSAO """
print pd.DataFrame( confusion_matrix(y_test, y_predict), columns=['Predicted Not Survival','Predicted Survival'], index=['True Nor Survival', 'True Survival'] )
with open("tree-60.dot", 'w') as f:
        export_graphviz(dt, out_file=f, feature_names=features)
command = ["dot", "-Tpng", "tree-60.dot", "-o", "tree-60.png"]
try:
	subprocess.check_call(command)
except:
	exit("Could not run dot, ie graphviz, to produce visualization")



#########################################
"""Proposition 61"""
#########################################
resTot61 = pd.merge(left=resultados, right=p61, left_on='ID_PROPOSITION', right_on='ID_PROPOSITION')
resTot61.drop(['FILING_ID','COMMITTEE_ID','AMEND_ID', 'TYPE','CITY', 'STATE', 'ZIPCODE', 'OCCUPATION', 'DATE', 'EMPLOYER', 'DESCRIPTION', 'TITLE', 'COMMITTEE_NAME' ], axis=1, inplace=True)
#print resTot61.count()
cp61 = resTot61.copy()
#print cp61
TOTALcp61 = cp61.AMOUNT.sum()
cp61['PERC'] = cp61['AMOUNT'] / TOTALcp61
#print TOTALcp61
#print cp61
colunas = list(cp61.columns.values)
#print colunas
cp61 = cp61[ ['FIRST_NAME', 'LAST_NAME','SUBJECT', 'RESULT', 'ID_PROPOSITION', 'COMMITTEE_POSITION', 'AMOUNT', 'PERC'] ]
cp61['FIRST_NAME'].fillna('PJ', inplace=True)
cp61['WHO'] = cp61.apply( lambda row: define_pjpf( row ), axis=1)
cp61 = cp61[ ['RESULT', 'AMOUNT', 'PERC', 'COMMITTEE_POSITION', 'ID_PROPOSITION', 'WHO' ] ]
#print cp61

DictCOMMITTEE_POSITION = {'SUPPORT': True, 'OPPOSE': False}
cp61['B_COMMITTEE_POSITION'] = cp61['COMMITTEE_POSITION'].map( DictCOMMITTEE_POSITION )
cp61.drop(['COMMITTEE_POSITION'], axis=1, inplace=True)

DictRESULT = {'APPROVED': True, 'DEFEATED': False}
cp61['B_RESULT'] = cp61['RESULT'].map( DictRESULT )
cp61.drop(['RESULT'], axis=1, inplace=True)
#print cp61.head()

#cp61 = cp61[ ['B_RESULT', 'AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'WHO' ] ]
cp61 = cp61[ ['AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'WHO' ] ]
print "Linhas: %d, Colunas: %d" % (len(cp61), len(cp61.columns))
print cp61['WHO'].value_counts()
print cp61['B_COMMITTEE_POSITION'].value_counts()
### SOMA VALORES AMOUNT COM GROUP BY B_COMMITTEE_POSITION
cp61['B_CONTRIBAboveMean'] = cp61['AMOUNT'] > cp61['AMOUNT'].mean()
cp61 = cp61[ ['AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'B_CONTRIBAboveMean', 'WHO' ] ]
print cp61.head()
features = cp61.columns.difference( ['WHO'] )
X = cp61[features].values
y = cp61['WHO'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

dt = DecisionTreeClassifier(random_state=1986, criterion='gini', max_depth=6)
dt.fit(X_train, y_train)
y_predict = dt.predict(X_test)

""" ACURACIA """
print accuracy_score(y_test, y_predict)

""" MATRIZ DE CONFUSAO """
print pd.DataFrame( confusion_matrix(y_test, y_predict), columns=['Predicted Not Survival','Predicted Survival'], index=['True Nor Survival', 'True Survival'] )
with open("tree-61.dot", 'w') as f:
        export_graphviz(dt, out_file=f, feature_names=features)
command = ["dot", "-Tpng", "tree-61.dot", "-o", "tree-61.png"]
try:
	subprocess.check_call(command)
except:
	exit("Could not run dot, ie graphviz, to produce visualization")

#########################################
"""Proposition 62"""
#########################################
resTot62 = pd.merge(left=resultados, right=p62, left_on='ID_PROPOSITION', right_on='ID_PROPOSITION')
resTot62.drop(['FILING_ID','COMMITTEE_ID','AMEND_ID', 'TYPE','CITY', 'STATE', 'ZIPCODE', 'OCCUPATION', 'DATE', 'EMPLOYER', 'DESCRIPTION', 'TITLE', 'COMMITTEE_NAME' ], axis=1, inplace=True)
#print resTot62.count()
cp62 = resTot62.copy()
#print cp62
TOTALcp62 = cp62.AMOUNT.sum()
cp62['PERC'] = cp62['AMOUNT'] / TOTALcp62
#print TOTALcp62
#print cp62
colunas = list(cp62.columns.values)
#print colunas
cp62 = cp62[ ['FIRST_NAME', 'LAST_NAME','SUBJECT', 'RESULT', 'ID_PROPOSITION', 'COMMITTEE_POSITION', 'AMOUNT', 'PERC'] ]
cp62['FIRST_NAME'].fillna('PJ', inplace=True)
cp62['WHO'] = cp62.apply( lambda row: define_pjpf( row ), axis=1)
cp62 = cp62[ ['RESULT', 'AMOUNT', 'PERC', 'COMMITTEE_POSITION', 'ID_PROPOSITION', 'WHO' ] ]
#print cp62

DictCOMMITTEE_POSITION = {'SUPPORT': True, 'OPPOSE': False}
cp62['B_COMMITTEE_POSITION'] = cp62['COMMITTEE_POSITION'].map( DictCOMMITTEE_POSITION )
cp62.drop(['COMMITTEE_POSITION'], axis=1, inplace=True)

DictRESULT = {'APPROVED': True, 'DEFEATED': False}
cp62['B_RESULT'] = cp62['RESULT'].map( DictRESULT )
cp62.drop(['RESULT'], axis=1, inplace=True)
#print cp62.head()

#cp62 = cp62[ ['B_RESULT', 'AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'WHO' ] ]
cp62 = cp62[ ['AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'WHO' ] ]
print "Linhas: %d, Colunas: %d" % (len(cp62), len(cp62.columns))
print cp62['WHO'].value_counts()
print cp62['B_COMMITTEE_POSITION'].value_counts()
### SOMA VALORES AMOUNT COM GROUP BY B_COMMITTEE_POSITION
cp62['B_CONTRIBAboveMean'] = cp62['AMOUNT'] > cp62['AMOUNT'].mean()
cp62 = cp62[ ['AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'B_CONTRIBAboveMean', 'WHO' ] ]
print cp62.head()
features = cp62.columns.difference( ['WHO'] )
X = cp62[features].values
y = cp62['WHO'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

dt = DecisionTreeClassifier(random_state=1986, criterion='gini', max_depth=6)
dt.fit(X_train, y_train)
y_predict = dt.predict(X_test)

""" ACURACIA """
print accuracy_score(y_test, y_predict)

""" MATRIZ DE CONFUSAO """
print pd.DataFrame( confusion_matrix(y_test, y_predict), columns=['Predicted Not Survival','Predicted Survival'], index=['True Nor Survival', 'True Survival'] )
with open("tree-62.dot", 'w') as f:
        export_graphviz(dt, out_file=f, feature_names=features)
command = ["dot", "-Tpng", "tree-62.dot", "-o", "tree-62.png"]
try:
	subprocess.check_call(command)
except:
	exit("Could not run dot, ie graphviz, to produce visualization")



#########################################
"""Proposition 64"""
#########################################
resTot64 = pd.merge(left=resultados, right=p64, left_on='ID_PROPOSITION', right_on='ID_PROPOSITION')
resTot64.drop(['FILING_ID','COMMITTEE_ID','AMEND_ID', 'TYPE','CITY', 'STATE', 'ZIPCODE', 'OCCUPATION', 'DATE', 'EMPLOYER', 'DESCRIPTION', 'TITLE', 'COMMITTEE_NAME' ], axis=1, inplace=True)
#print resTot64.count()
cp64 = resTot64.copy()
#print cp64
TOTALcp64 = cp64.AMOUNT.sum()
cp64['PERC'] = cp64['AMOUNT'] / TOTALcp64
#print TOTALcp64
#print cp64
colunas = list(cp64.columns.values)
#print colunas
cp64 = cp64[ ['FIRST_NAME', 'LAST_NAME','SUBJECT', 'RESULT', 'ID_PROPOSITION', 'COMMITTEE_POSITION', 'AMOUNT', 'PERC'] ]
cp64['FIRST_NAME'].fillna('PJ', inplace=True)
cp64['WHO'] = cp64.apply( lambda row: define_pjpf( row ), axis=1)
cp64 = cp64[ ['RESULT', 'AMOUNT', 'PERC', 'COMMITTEE_POSITION', 'ID_PROPOSITION', 'WHO' ] ]
#print cp64

DictCOMMITTEE_POSITION = {'SUPPORT': True, 'OPPOSE': False}
cp64['B_COMMITTEE_POSITION'] = cp64['COMMITTEE_POSITION'].map( DictCOMMITTEE_POSITION )
cp64.drop(['COMMITTEE_POSITION'], axis=1, inplace=True)

DictRESULT = {'APPROVED': True, 'DEFEATED': False}
cp64['B_RESULT'] = cp64['RESULT'].map( DictRESULT )
cp64.drop(['RESULT'], axis=1, inplace=True)
#print cp64.head()

#cp64 = cp64[ ['B_RESULT', 'AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'WHO' ] ]
cp64 = cp64[ ['AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'WHO' ] ]
print "Linhas: %d, Colunas: %d" % (len(cp64), len(cp64.columns))
print cp64['WHO'].value_counts()
print cp64['B_COMMITTEE_POSITION'].value_counts()
### SOMA VALORES AMOUNT COM GROUP BY B_COMMITTEE_POSITION
cp64['B_CONTRIBAboveMean'] = cp64['AMOUNT'] > cp64['AMOUNT'].mean()
cp64 = cp64[ ['AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'B_CONTRIBAboveMean', 'WHO' ] ]
print cp64.head()
features = cp64.columns.difference( ['WHO'] )
X = cp64[features].values
y = cp64['WHO'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

dt = DecisionTreeClassifier(random_state=1986, criterion='gini', max_depth=6)
dt.fit(X_train, y_train)
y_predict = dt.predict(X_test)

""" ACURACIA """
print accuracy_score(y_test, y_predict)

""" MATRIZ DE CONFUSAO """
print pd.DataFrame( confusion_matrix(y_test, y_predict), columns=['Predicted Not Survival','Predicted Survival'], index=['True Nor Survival', 'True Survival'] )
with open("tree-64.dot", 'w') as f:
        export_graphviz(dt, out_file=f, feature_names=features)
command = ["dot", "-Tpng", "tree-64.dot", "-o", "tree-64.png"]
try:
	subprocess.check_call(command)
except:
	exit("Could not run dot, ie graphviz, to produce visualization")


#########################################
"""Proposition 66"""
#########################################
resTot66 = pd.merge(left=resultados, right=p66, left_on='ID_PROPOSITION', right_on='ID_PROPOSITION')
resTot66.drop(['FILING_ID','COMMITTEE_ID','AMEND_ID', 'TYPE','CITY', 'STATE', 'ZIPCODE', 'OCCUPATION', 'DATE', 'EMPLOYER', 'DESCRIPTION', 'TITLE', 'COMMITTEE_NAME' ], axis=1, inplace=True)
#print resTot66.count()
cp66 = resTot66.copy()
#print cp66
TOTALcp66 = cp66.AMOUNT.sum()
cp66['PERC'] = cp66['AMOUNT'] / TOTALcp66
#print TOTALcp66
#print cp66
colunas = list(cp66.columns.values)
#print colunas
cp66 = cp66[ ['FIRST_NAME', 'LAST_NAME','SUBJECT', 'RESULT', 'ID_PROPOSITION', 'COMMITTEE_POSITION', 'AMOUNT', 'PERC'] ]
cp66['FIRST_NAME'].fillna('PJ', inplace=True)
cp66['WHO'] = cp66.apply( lambda row: define_pjpf( row ), axis=1)
cp66 = cp66[ ['RESULT', 'AMOUNT', 'PERC', 'COMMITTEE_POSITION', 'ID_PROPOSITION', 'WHO' ] ]
#print cp66

DictCOMMITTEE_POSITION = {'SUPPORT': True, 'OPPOSE': False}
cp66['B_COMMITTEE_POSITION'] = cp66['COMMITTEE_POSITION'].map( DictCOMMITTEE_POSITION )
cp66.drop(['COMMITTEE_POSITION'], axis=1, inplace=True)

DictRESULT = {'APPROVED': True, 'DEFEATED': False}
cp66['B_RESULT'] = cp66['RESULT'].map( DictRESULT )
cp66.drop(['RESULT'], axis=1, inplace=True)
#print cp66.head()

#cp66 = cp66[ ['B_RESULT', 'AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'WHO' ] ]
cp66 = cp66[ ['AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'WHO' ] ]
print "Linhas: %d, Colunas: %d" % (len(cp66), len(cp66.columns))
print cp66['WHO'].value_counts()
print cp66['B_COMMITTEE_POSITION'].value_counts()
### SOMA VALORES AMOUNT COM GROUP BY B_COMMITTEE_POSITION
cp66['B_CONTRIBAboveMean'] = cp66['AMOUNT'] > cp66['AMOUNT'].mean()
cp66 = cp66[ ['AMOUNT', 'PERC', 'B_COMMITTEE_POSITION', 'B_CONTRIBAboveMean', 'WHO' ] ]
print cp66.head()
features = cp66.columns.difference( ['WHO'] )
X = cp66[features].values
y = cp66['WHO'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

dt = DecisionTreeClassifier(random_state=1986, criterion='gini', max_depth=6)
dt.fit(X_train, y_train)
y_predict = dt.predict(X_test)

""" ACURACIA """
print accuracy_score(y_test, y_predict)

""" MATRIZ DE CONFUSAO """
print pd.DataFrame( confusion_matrix(y_test, y_predict), columns=['Predicted Not Survival','Predicted Survival'], index=['True Nor Survival', 'True Survival'] )
with open("tree-66.dot", 'w') as f:
        export_graphviz(dt, out_file=f, feature_names=features)
command = ["dot", "-Tpng", "tree-66.dot", "-o", "tree-66.png"]
try:
	subprocess.check_call(command)
except:
	exit("Could not run dot, ie graphviz, to produce visualization")




sys.exit(0)


# In[61]:


resTot52 = pd.merge(left=resultados, right=p52, left_on='ID_PROPOSITION', right_on='ID_PROPOSITION')


# In[62]:


resTot52.count()


# In[63]:


resTot51.append(resTot52)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[47]:


resTot.count()


# In[48]:


resTot.head()


# In[ ]:





# In[ ]:





# In[41]:





# In[51]:


result51 = p51AMOUNT.join(p51COMMITTEE_NAME, how='outer')


# In[52]:


result51.reset_index()


# In[53]:


result51.drop(['FILING_ID','COMMITTEE_ID','AMEND_ID','ID_PROPOSITION'], axis=1, inplace=True)


# In[54]:


result51.reset_index()


# In[61]:


result51.columns = ['TOTAL','TOTAL_COMMITTEE']


# In[ ]:





# In[ ]:





# In[57]:


result51.reset_index()


# In[58]:


result51 = result51.join(propTIT51, how='outer')


# In[59]:


result51.reset_index()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[70]:


p52.COMMITTEE_NAME.value_counts().reset_index()


# In[71]:


p53.COMMITTEE_NAME.value_counts().reset_index()


# In[72]:


p64.COMMITTEE_NAME.value_counts().reset_index()


# In[73]:


p51.groupby("COMMITTEE_NAME").sum().reset_index()


# In[74]:


p52.groupby("COMMITTEE_NAME").sum().reset_index()


# In[75]:


p53.groupby("COMMITTEE_NAME").sum().reset_index()


# In[76]:


p64.groupby("COMMITTEE_NAME").sum().reset_index()


# In[77]:


p51.drop(['FILING_ID','COMMITTEE_ID','AMEND_ID'], axis=1, inplace=True)


# In[78]:


p51.groupby("COMMITTEE_NAME").sum().plot.barh()


# In[79]:


p52.drop(['FILING_ID','COMMITTEE_ID','AMEND_ID','FIRST_NAME','EMPLOYER','OCCUPATION'], axis=1, inplace=True)


# In[80]:


p52.groupby("COMMITTEE_NAME").sum().plot.barh()


# In[81]:


p53.drop(['FILING_ID','COMMITTEE_ID','AMEND_ID','ZIPCODE'], axis=1, inplace=True)


# In[82]:


p53.groupby("COMMITTEE_NAME").sum().plot.barh()


# In[83]:


p64.drop(['FILING_ID','COMMITTEE_ID','AMEND_ID'], axis=1, inplace=True)


# In[84]:


p64.groupby("COMMITTEE_NAME").sum().plot.bar()


# In[85]:


top_supporters51 = p51.groupby(
    ["FIRST_NAME", "LAST_NAME"]
).sum().reset_index().sort_values("AMOUNT", ascending=False).head(10)


# In[86]:


top_supporters51.head(10)


# In[87]:


top_supporters52 = p52.groupby(
    ["LAST_NAME"]
).sum().reset_index().sort_values("AMOUNT", ascending=False).head(10)


# In[88]:


top_supporters52.head(10)


# In[89]:


top_supporters53 = p53.groupby(
    ["FIRST_NAME", "LAST_NAME"]
).sum().reset_index().sort_values("AMOUNT", ascending=False).head(10)


# In[90]:


top_supporters53.head(10)


# In[91]:


top_supporters64 = p64.groupby(
    ["FIRST_NAME", "LAST_NAME"]
).sum().reset_index().sort_values("AMOUNT", ascending=False).head(10)


# In[92]:


top_supporters64.head(10)


# In[93]:


p51.plot.hist()


# In[ ]:





# In[ ]:





# In[94]:


p52.plot.hist()


# In[95]:


p53.plot.hist()


# In[96]:


p64.plot.hist()


