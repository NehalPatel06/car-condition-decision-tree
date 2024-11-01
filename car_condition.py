# -*- coding: utf-8 -*-
"""Lab_4_Code_UPD_V2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mxENsQpGuVViCyG5OJwK2pp53KMFRbo-
"""

# Read your train data and test data in two different variables
import pandas as pd

trainData = pd.read_csv('trainData.csv')
trainData

trainData.dtypes

testData = pd.read_csv('testData.csv')
trainData

"""For the rest of this lab session, we use sci-kit learn library. sci-kit learn is a simple and efficient tool for predictive data analysis. Install the library using the following command (**Note**: scikit-learn is already installed on Colab, and you don't need to install it again):

```pip install -U scikit-learn```

The *sklearn.tree* module includes decision tree-based models for classification. Decision Trees (DTs) are supervised learning method. The goal is to create a model that predicts the value of a target variable by learning simple decision rules inferred from the data features.

---

Decision tree that is part of scikit-learn only accepts numerical values. Thus, we have to convert non-numerical values to numerical values. We start by the target class. Note that for the traget class, the order of attriutes is not important. Thus, we use `LabelEncoder`
"""

# Note that we store the converted target_class attribute in a new column called "target_class_val"
# this is because you can compare and see the old attribute and the new attribute at the same time

from sklearn.preprocessing import LabelEncoder

le_target = LabelEncoder()
le_target.fit(trainData['target_class'])
trainData['target_class_val'] = le_target.transform(trainData['target_class'])
testData['target_class_val'] = le_target.transform(testData['target_class'])

# note that the new attribute (column) is added at the end of the dataframe
trainData

testData

# check the mapping values of target_class
print('unique values of target_class', trainData.target_class.unique())
print('mapping of unacc value is ', trainData[trainData['target_class']=='unacc'].iloc[0]['target_class_val'])
print('mapping of acc value is ', trainData[trainData['target_class']=='acc'].iloc[0]['target_class_val'])
print('mapping of good value is ', trainData[trainData['target_class']=='good'].iloc[0]['target_class_val'])
print('mapping of vgood value is ', trainData[trainData['target_class']=='vgood'].iloc[0]['target_class_val'])

# number of instances of each target values (there are other ways of doing this, this is one easy way)
print('number of unacc instances is ', len(trainData[trainData['target_class']=='unacc']))
print('number of acc instances is ', len(trainData[trainData['target_class']=='acc']))
print('number of good instances is ', len(trainData[trainData['target_class']=='good']))
print('number of vgood instances is ', len(trainData[trainData['target_class']=='vgood']))

"""We now move to convert the remaining attributes to numerical. However, since the remaining attributes will be used to create the decision tree (i.e., they are not target attributes), and they are Ordinal Attributes, their order is important. Thus, we have to use `OrdinalEncoder` for conversion. The same as the target attribute, we will store these in new columns. First, we will find unique values of each attributes. We then use them to map non-numeric values to numeric values."""

print("unique values of buying", trainData.buying.unique())
print("unique values of maint", trainData.maint.unique())
print("unique values of doors", trainData.doors.unique())
print("unique values of persons", trainData.persons.unique())
print("unique values of lug_boot", trainData.lug_boot.unique())
print("unique values of safety", trainData.safety.unique())

"""We need to install `category_encoders` package (it's not installed on Colab by default)"""

pip install category_encoders

from category_encoders import OrdinalEncoder

buying_mapping = [{'col': 'buying', 'mapping': {'vhigh': 3, 'high': 2, 'med': 1, 'low': 0}}]
oe_buying = OrdinalEncoder(mapping=buying_mapping)
oe_buying.fit(trainData['buying'])
trainData['buying_val'] = oe_buying.transform(trainData['buying'])
testData['buying_val'] = oe_buying.transform(testData['buying'])

maint_mapping = [{'col': 'maint', 'mapping': {'vhigh': 3, 'high': 2, 'med': 1, 'low': 0}}]
oe_maint = OrdinalEncoder(mapping=maint_mapping)
oe_maint.fit(trainData['maint'])
trainData['maint_val'] = oe_maint.transform(trainData['maint'])
testData['maint_val'] = oe_maint.transform(testData['maint'])

# we may want to consider using one hot encoding for doors attribute (will be covered in a future lecture/lab)
doors_mapping = [{'col': 'doors', 'mapping': {'5more': 3, '4': 2, '3': 1, '2': 0}}]
oe_doors = OrdinalEncoder(mapping=doors_mapping)
oe_doors.fit(trainData['doors'])
trainData['doors_val'] = oe_doors.transform(trainData['doors'])
testData['doors_val'] = oe_doors.transform(testData['doors'])

# we may want to consider using one hot encoding for persons attribute (will be covered in a future lecture/lab)
persons_mapping = [{'col': 'persons', 'mapping': {'more': 2, '4': 1, '2': 0}}]
oe_persons = OrdinalEncoder(mapping=persons_mapping)
oe_persons.fit(trainData['persons'])
trainData['persons_val'] = oe_persons.transform(trainData['persons'])
testData['persons_val'] = oe_persons.transform(testData['persons'])

# we may want to consider using one hot encoding for lug attribute (will be covered in a future lecture/lab)
lug_boot_mapping = [{'col': 'lug_boot', 'mapping': {'big': 2, 'med': 1, 'small': 0}}]
oe_lug_boot = OrdinalEncoder(mapping=lug_boot_mapping)
oe_lug_boot.fit(trainData['lug_boot'])
trainData['lug_boot_val'] = oe_lug_boot.transform(trainData['lug_boot'])
testData['lug_boot_val'] = oe_lug_boot.transform(testData['lug_boot'])

safety_mapping = [{'col': 'safety', 'mapping': {'high': 2, 'med': 1, 'low': 0}}]
oe_safety = OrdinalEncoder(mapping=safety_mapping)
oe_safety.fit(trainData['safety'])
trainData['safety_val'] = oe_safety.transform(trainData['safety'])
testData['safety_val'] = oe_safety.transform(testData['safety'])

# manually compare the new attribute with the old one and confirm that the encoding kept the order
trainData

testData

# Now, import a decision tree and fit it on the train data
from sklearn import tree

"""------------ Tree1 ------------"""

# First, we only use *buying* attribute to predict the target class
# Rremember we encodeed buying to buying_val and target_class to target_class_val (so they're both numeric)

tree1 = tree.DecisionTreeClassifier()
tree1 = tree1.fit(trainData[['buying_val']], trainData['target_class_val'])

"""Now we plot the tree uinsg:

`tree.plot_tree(tree1)`

Note that in other environments, such as PyCharm, you may need to use the following two commands after the above command to show the tree (but it's not necessary in Colab):

`import matplotlib.pyplot as plt`

`plt.show()`
"""

# now we plot the tree
tree.plot_tree(tree1)

# another visualization that shows class label (note that we can's use target_class_val as this method doesn't accept int values). 
# But since we have a one to one mappting between target_class and target_class_val, we get the same result.
import graphviz 
dot_data1 = tree.export_graphviz(tree1, out_file=None, 
                    feature_names=['buying_val'],  
                    class_names=trainData.target_class.unique(),
                    filled=True, rounded=True,  
                    special_characters=True)
graph1 = graphviz.Source(dot_data1)  
graph1 
# as you can see in the graph, all instances are essentially predicted as 'vgood'

# show tree in a textual format
text_representation1 = tree.export_text(tree1)
print(text_representation1)

# predict the values of test data using the first tree
predicted_1 = tree1.predict(testData[['buying_val']])

# compare the predicted labels with the actual ones
from sklearn.metrics import classification_report

print(classification_report(testData[['target_class_val']], predicted_1))

"""------------ Tree 2 ------------"""

# now we build the second tree using three attributes: persons, lug_boot and safety
tree2 = tree.DecisionTreeClassifier()
tree2 = tree2.fit(trainData[['persons_val', 'lug_boot_val', 'safety_val']], trainData['target_class_val'])

# plot the tree
tree.plot_tree(tree2)

dot_data2 = tree.export_graphviz(tree2, out_file=None, 
                    feature_names=['persons_val', 'lug_boot_val', 'safety_val'],  
                    class_names=trainData.target_class.unique(),
                    filled=True, rounded=True,  
                    special_characters=True)
graph2 = graphviz.Source(dot_data2)  
graph2 
# as you can see in the second graph, we now have preditions for 'vgood' and 'unacc'

# show tree in a textual format
text_representation2 = tree.export_text(tree2)
print(text_representation2)

# check the performance of the second tree on test data
predicted_2 = tree2.predict(testData[['persons_val', 'lug_boot_val', 'safety_val']])

print(classification_report(testData[['target_class_val']], predicted_2))
# we gain a small improvement in accuracy comparing to the first tree

"""------------ Tree 3 ------------"""

# building the thrid tree using all six attributes
tree3 = tree.DecisionTreeClassifier()
tree3 = tree3.fit(trainData[['buying_val', 'maint_val', 'doors_val', 'persons_val', 'lug_boot_val', 'safety_val']], trainData['target_class_val'])

# plot the tree (it takes a few seconds as this is a larger tree comparing to the first one and second one)
tree.plot_tree(tree3)

dot_data3 = tree.export_graphviz(tree3, out_file=None, 
                    feature_names=['buying_val', 'maint_val', 'doors_val', 'persons_val', 'lug_boot_val', 'safety_val'],  
                    class_names=trainData.target_class.unique(),  
                    filled=True, rounded=True,  
                    special_characters=True)  
graph3 = graphviz.Source(dot_data3)  
graph3 
# with the third graph, all four labels are in leaf nodes now

text_representation3 = tree.export_text(tree3)
print(text_representation3)

# check the performance of the third tree on test data
predicted_3 = tree3.predict(testData[['buying_val', 'maint_val', 'doors_val', 'persons_val', 'lug_boot_val', 'safety_val']])
print(classification_report(testData[['target_class_val']], predicted_3))
# we gain significant improvement comparing to the first and second trees

