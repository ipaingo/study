import re
import random
import pymorphy3

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, StackingClassifier
from xgboost import XGBClassifier


import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Embedding, LSTM, GRU

# pd.options.display.width = 0
# pd.set_option('display.max_rows', 100)
# pd.set_option('display.max_columns', 11)

df = pd.read_excel("mails.xlsx")

cls_dic = {1:'Условия подачи',
           2:'Проходной и допустимый балл',
           3:'Достижения',
           4:'Общежития',
           5:'Вступительные испытания',
           6:'Перевод',
           7:'Аспирантура',
           8:'Регистрация',
           }

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