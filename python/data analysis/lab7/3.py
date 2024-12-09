import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, StackingClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier

df = pd.read_csv("creditcard.csv")
x = df[["V1","V2","V3","V4","V5","V6","V7","V8","V9","V10","V11","V12","V13","V14","V15","V16","V17","V18","V19","V20","V21","V22","V23","V24","V25","V26","V27","V28","Amount"]]
y = df["Class"]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, stratify=y)

clf = LGBMClassifier(objective="binary", n_estimators=10)
clf.fit(x_train, y_train)
y_pred = clf.predict(x_test)

print(f1_score(y_test, y_pred, average="macro"))
print(classification_report(y_test, y_pred, digits=6))
print(confusion_matrix(y_test, y_pred, labels=clf.classes_))
print("===========================")



estimators = [('Forest', RandomForestClassifier(bootstrap=False, criterion='gini', max_features='log2', n_estimators=50)),
              ('XGBoost', XGBClassifier()),
              ('Tree', DecisionTreeClassifier())]

clf = StackingClassifier(estimators=estimators)
clf.fit(x_train, y_train)
y_pred = clf.predict(x_test)

print(clf.final_estimator_)
print(f1_score(y_test, y_pred, average="macro"))
print(classification_report(y_test, y_pred, digits=6))
print(confusion_matrix(y_test, y_pred, labels=clf.classes_))



# 0.8543873103394717
#               precision    recall  f1-score   support
#
#            0   0.999264  0.998930  0.999097     14956
#            1   0.673469  0.750000  0.709677        44
#
#     accuracy                       0.998200     15000
#    macro avg   0.836367  0.874465  0.854387     15000
# weighted avg   0.998309  0.998200  0.998248     15000
#
# [[14940    16]
#  [   11    33]]
# ===========================
# LogisticRegression()
# 0.9388572667730821
#               precision    recall  f1-score   support
#
#            0   0.999465  0.999866  0.999666     14956
#            1   0.947368  0.818182  0.878049        44
#
#     accuracy                       0.999333     15000
#    macro avg   0.973417  0.909024  0.938857     15000
# weighted avg   0.999312  0.999333  0.999309     15000
#
# [[14954     2]
#  [    8    36]]