import re
import random
import pymorphy2

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.text as text
import matplotlib.cm as cm

#import seaborn as sns; sns.set()

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, StackingClassifier
from xgboost import XGBClassifier

from sklearn.model_selection import GridSearchCV
import itertools

import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Embedding, LSTM, GRU

# pd.options.display.width = 0
# pd.set_option('display.max_rows', 100)
# pd.set_option('display.max_columns', 11)

df = pd.read_csv("mails.csv", sep='\t')

cls_dic = {1:'Условия подачи',
           2:'Проходной и допустимый балл',
           3:'Достижения',
           4:'Общежития',
           5:'Вступительные испытания',
           6:'Перевод',
           7:'Аспирантура',
           8:'Регистрация',
           }
# hlt_dic = {1:'ONLINE приёмная',
#            2:'Очная приемная',
#            3:'Приёмная аспирантуры'
#            }

# df['cls_name'] = df['class'].map(lambda x: cls_dic[x])
# df['hlt_name'] = df.TYPE_HOTLINE.map(lambda x: hlt_dic[x])
# print(df)

# df["text"] = df["CONTENT"].map(lambda txt: txt.split())

def del_punct(word):
    return re.sub(r"\W", " ", word)

def filter_words(word):
    return word not in [
        "здравствуйте",
    ]

def morphan(word, morph):
    word = del_punct(word).strip()
    p = morph.parse(word)[0]

    word_new = word
    if (not 'Surn' in p.tag) and (not 'Name' in p.tag) and (not 'Patr' in p.tag) and ('NOUN' in p.tag):
        #существительное не ФИО
        word_new = p.normal_form
    elif 'Surn' in p.tag:
        word_new = 'ФАМИЛИЯ'
    elif 'Name' in p.tag:
        word_new = 'ИМЯ'
    elif 'Patr' in p.tag:
        word_new = 'ОТЧЕСТВО'


    elif ('INFN' in p.tag) or ('VERB' in p.tag): #глагол
        word_new = p.normal_form

    elif ('ADJF' in p.tag) or ('ADJS' in p.tag) or ('COMP' in p.tag): #прилагательное
        word_new = p.normal_form


    elif ('PRTF' in p.tag) or ('PRTS' in p.tag) or ('GRND' in p.tag): #причастие, похоже на глагол
        word_new = p.normal_form

    elif ('ADVB' in p.tag) or ('NPRO' in p.tag) or ('PRED' in p.tag) or ('PREP' in p.tag) or ('CONJ' in p.tag) or ('PRCL' in p.tag) or ('INTJ' in p.tag):
        word_new = ""

    elif ('NUMR' in p.tag) or ('NUMB' in p.tag) or ('intg' in p.tag): # числительные NUMB,intg
        word_new = ''

    else:
        word_new = word
    return word_new

def normtext(txt, morph):
    return str(' '.join(filter(filter_words, [morphan(x, morph) for x in txt.split()])))


def pymorphy2_311_hotfix():
    from inspect import getfullargspec
    from pymorphy2.units.base import BaseAnalyzerUnit

    def _get_param_names_311(klass):
        if klass.__init__ is object.__init__:
            return []
        args = getfullargspec(klass.__init__).args
        return sorted(args[1:])

    setattr(BaseAnalyzerUnit, '_get_param_names', _get_param_names_311)

pymorphy2_311_hotfix()
morph = pymorphy2.MorphAnalyzer()

df['text'] = df["CONTENT"].map(lambda x: normtext(x, morph))

print(df['text'])
with open("test.txt", "w", encoding="utf-8") as file:
    file.write(df["text"].to_csv())


def classifier(X_train, y_train, C=10.):
    '''
    Возвращает обученный классификатор и векторизатор.
    '''

    tfv = TfidfVectorizer()
    X_train = tfv.fit_transform(X_train)

    clf = LogisticRegression(C=C)
    # clf = DecisionTreeClassifier()
    # clf = RandomForestClassifier()
    # clf = BaggingClassifier(DecisionTreeClassifier())
    # estimators = [  ('Forest', RandomForestClassifier()),
    #                 # ('XGBoost', XGBClassifier()),
    #                 ('Tree', DecisionTreeClassifier())]
    # estimators = [  ('Tree', DecisionTreeClassifier()),
    #                 ('Forest', RandomForestClassifier())]
    # clf = StackingClassifier(estimators=estimators)

    clf = clf.fit(X_train, y_train)

    return tfv, clf

def predictor(text, clf, tfv):
    '''
    text - классифицируемый текс
    clf - обученный классификатор
    tfv - обученный векторизатор

    '''
    X_test = tfv.transform([text])

    pred = clf.predict(X_test)

    return pred[0]

def try_to_determine(text):
    words = text.split()
    for word in words:
        if word in ["аспирантура", "аспирант", "кандидат"]:
            return 7
        if word in ["зарегистрироваться"]:
            return 8
        # if word in ["общежитие"]: # Почему-то вопросы по общежитию иногда относится к условиям подачи. И ещё 4 раз к регистрации.
        #     return 4              # Хах, забавно, указав условие выше, общежития скакнули сразу до 1.00
    
    return 0

X_train, X_test, y_train, y_test = train_test_split(df.text, df['class'], random_state=42, test_size=0.3)
tfv, clf = classifier(X_train, y_train, C=10)
# tfv, clf = classifier(X_train, y_train, C=100)

class_save = []
pred = []
for nom, txt in enumerate(X_test.values):
    det_class = try_to_determine(txt)
    if det_class != 0:
        pred.append(det_class)
    else:
        pred.append(predictor(txt, clf, tfv))

y_test_list = y_test.tolist()
pred_list = pred

mtrs = classification_report([cls_dic[x] for x in y_test_list], [cls_dic[x] for x in pred_list])
print(mtrs)





X_train_1, X_vt_1, y_train_1, y_vt_1 = train_test_split(df.text, df['class'], random_state=42, test_size=0.2)
X_valid_1, X_test_1, y_valid_1, y_test_1 = train_test_split(X_vt_1, y_vt_1, test_size=0.5, random_state=42)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train_1)

textSequences = tokenizer.texts_to_sequences(X_train_1)

max_words = 0
for desc in df.text.tolist():
    words = len(desc.split())
    if words > max_words:
        max_words = words
print('Максимальное количество слов в самом длинном письме: {} слов'.format(max_words))

total_unique_words = len(tokenizer.word_counts)
print('Всего уникальных слов в словаре: {}'.format(total_unique_words))

maxSequenceLength = max_words

vocab_size = 10000
tokenizer = Tokenizer(num_words=vocab_size)
tokenizer.fit_on_texts(df.text)

X_train = tokenizer.texts_to_sequences(X_train_1)
X_valid = tokenizer.texts_to_sequences(X_valid_1)
X_test = tokenizer.texts_to_sequences(X_test_1)

X_train = sequence.pad_sequences(X_train, maxlen=maxSequenceLength)
X_valid = sequence.pad_sequences(X_valid, maxlen=maxSequenceLength)
X_test = sequence.pad_sequences(X_test, maxlen=maxSequenceLength)

print('Размерность X_train:', X_train.shape)
print('Размерность X_valid:', X_valid.shape)
print('Размерность X_test:', X_test.shape)

# Преобразуем категории в матрицу двоичных чисел (для использования categorical_crossentropy)

num_classes = df['class'].unique().shape[0]+1

y_train = keras.utils.to_categorical(y_train_1, num_classes)
y_valid = keras.utils.to_categorical(y_valid_1, num_classes)
y_test = keras.utils.to_categorical(y_test_1, num_classes)
print('y_train shape:', y_train.shape)
print('y_valid shape:', y_valid.shape)
print('y_test shape:', y_test.shape)

print(u'Собираем модель...')
model = Sequential()
# model.add(Embedding(10000, maxSequenceLength))
model.add(Embedding(1500, maxSequenceLength))
# model.add(Embedding(100000, maxSequenceLength))

# model.add(LSTM(32, dropout=0.3, recurrent_dropout=0.3))
# model.add(LSTM(32, dropout=0.1, recurrent_dropout=0.1))
# model.add(LSTM(32, dropout=0.0, recurrent_dropout=0.0))
model.add(LSTM(32, dropout=0.2, recurrent_dropout=0.2))
# model.add(GRU(32, dropout=0.2, recurrent_dropout=0.2))

# model.add(Dense(num_classes, activation='sigmoid'))
# model.add(Dense(num_classes, activation='silu'))
# model.add(Dense(num_classes, activation='exponential'))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss='categorical_crossentropy',
# model.compile(loss='poisson',
# model.compile(loss='categorical_focal_crossentropy',
              optimizer='adam',
            #   optimizer='adamw',
            #   optimizer='nadam',
              metrics=['accuracy'])

print(model.summary())

batch_size = 32
epochs = 25

print(u'Тренируем модель...')
history = model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          validation_data=(X_valid, y_valid))

predictions = model.predict(X_test).argmax(axis=1)
y2 = np.array(y_test_1.to_list())
pred2 = np.array(predictions)

print(classification_report([cls_dic[x] for x in y2], [cls_dic[x] for x in pred2]))