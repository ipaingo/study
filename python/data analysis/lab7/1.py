import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier

df = pd.read_csv("creditcard.csv")
x = df[["V1","V2","V3","V4","V5","V6","V7","V8","V9","V10","V11","V12","V13","V14","V15","V16","V17","V18","V19","V20","V21","V22","V23","V24","V25","V26","V27","V28","Amount"]]
y = df["Class"]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, stratify=y)

clf = DecisionTreeClassifier().fit(x_train, y_train)
y_pred = clf.predict(x_test)
f1_dec_tree = f1_score(y_test, y_pred, average="macro")
# print(f1_score(y_test, y_pred, average="macro"))
# print(classification_report(y_test, y_pred, digits=6))

clf = BaggingClassifier(DecisionTreeClassifier())
clf.fit(x_train, y_train)
y_pred = clf.predict(x_test)
f1_bagg_tree = f1_score(y_test, y_pred, average="macro")
# print(f1_score(y_test, y_pred, average="macro"))
# print(classification_report(y_test, y_pred, digits=6))

clf = RandomForestClassifier().fit(x_train, y_train)
y_pred = clf.predict(x_test)
f1_rand_forest = f1_score(y_test, y_pred, average="macro")
# print(f1_score(y_test, y_pred, average="macro"))
# print(classification_report(y_test, y_pred, digits=6))

print(f"Дерево решений: {f1_dec_tree}\nБэггинг дерева решений: {f1_bagg_tree}\nСлучайный лес: {f1_rand_forest}\n")