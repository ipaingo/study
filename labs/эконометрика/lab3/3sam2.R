setwd("C:/Users/regst/Desktop/учёба/Эконометрика/lab3") # установить рабочую папку
T<-read.table("reg.txt", header=TRUE) # прочитать данные из файла и записать в таблицу T

#A1-A2
T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию F1
regA2A1<-lm(formula=T$A2 ~T$A1) # построить регрессию
summary(regA2A1) # вывод информации о построенной регрессии
format(coef(regA2A1), digits =12) # вывод коэффициентов регрессии с точностью 12 знаков
plot(x=T$A1, y=T$A2) # нарисовать диаграмму рассеяния
abline(regA2A1, col="red") # нарисовать линию регрессии
mean(regA2A1$residuals)

plot(regA2A1$residuals, main="График остатков", xlab="Номер наблюдения",
     ylab="Остатки")
abline(h=0)
#install.packages("forecast")
library("forecast") # подключить библиотеку forecast
accuracy(regA2A1) # вывод оценок качества регрессии, в том числе MAPE
T<-T[1,] # оставить только одну строку в таблице Т
T$A1<- 1350 # записать значение 1350 в переменную A1
format(predict(regA2A1, newdata=T, interval="confidence", level=0.9), digits=10) # вывод точечного и интервального прогнозов
P<-predict(regA2A1, newdata=T, interval="confidence", level=0.9) # записать прогноз в переменную P
T<-read.table("reg.txt", header=TRUE) # снова прочитать данные из файла
T<-T[order(T$A1),]
plot(x=T$A1, y=T$A2) # нарисовать диаграмму рассеяния
abline(regA2A1) # нарисовать линию регрессии
points(x=1350, y=P[1], col="red") # нарисовать точечный прогноз
lines(x=c(1350,1350,1350), y=P, col="red") # нарисовать интервальный прогноз

#A1-A3
T<-read.table("reg.txt", header=TRUE) # прочитать данные из файла и записать в таблицу T
T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию F1
regA3A1<-lm(formula=T$A3 ~T$A1) # построить регрессию
summary(regA3A1) # вывод информации о построенной регрессии
format(coef(regA3A1), digits =12) # вывод коэффициентов регрессии с точностью 13 знаков
plot(x=T$A1, y=T$A3) # нарисовать диаграмму рассеяния
abline(regA3A1, col="red") # нарисовать линию регрессии
mean(regA3A1$residuals)
plot(regA3A1$residuals, main="График остатков", xlab="Номер наблюдения",
     ylab="Остатки")
abline(h=0)
#install.packages("forecast")
library("forecast") # подключить библиотеку forecast
accuracy(regA3A1) # вывод оценок качества регрессии, в том числе MAPE
T<-T[1,] # оставить только одну строку в таблице Т
T$A1<- 1350 # записать значение 1350 в переменную A1
format(predict(regA3A1, newdata=T, interval="confidence", level=0.9), digits=10) # вывод точечного и интервального прогнозов
P<-predict(regA3A1, newdata=T, interval="confidence", level=0.9) # записать прогноз в переменную P
T<-read.table("reg.txt", header=TRUE) # снова прочитать данные из файла
T<-T[order(T$A1),]
plot(x=T$A1, y=T$A3) # нарисовать диаграмму рассеяния
abline(regA3A1) # нарисовать линию регрессии
points(x=1350, y=P[1], col="red") # нарисовать точечный прогноз
lines(x=c(1350,1350,1350), y=P, col="red") # нарисовать интервальный прогноз

#A1-A4
T<-read.table("reg.txt", header=TRUE) # прочитать данные из файла и записать в таблицу T
T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию F1
regA4A1<-lm(formula=T$A4 ~T$A1) # построить регрессию
summary(regA4A1) # вывод информации о построенной регрессии
format(coef(regA4A1), digits =12) # вывод коэффициентов регрессии с точностью 14 знаков
plot(x=T$A1, y=T$A4) # нарисовать диаграмму рассеяния
abline(regA4A1, col="red") # нарисовать линию регрессии
mean(regA4A1$residuals)
plot(regA4A1$residuals, main="График остатков", xlab="Номер наблюдения",
     ylab="Остатки")
abline(h=0)
#install.packages("forecast")
library("forecast") # подключить библиотеку forecast
accuracy(regA4A1) # вывод оценок качества регрессии, в том числе MAPE
T<-T[1,] # оставить только одну строку в таблице Т
T$A1<- 1350 # записать значение 1350 в переменную A1
format(predict(regA4A1, newdata=T, interval="confidence", level=0.9), digits=10) # вывод точечного и интервального прогнозов
P<-predict(regA4A1, newdata=T, interval="confidence", level=0.9) # записать прогноз в переменную P
T<-read.table("reg.txt", header=TRUE) # снова прочитать данные из файла
T<-T[order(T$A1),]
plot(x=T$A1, y=T$A4) # нарисовать диаграмму рассеяния
abline(regA4A1) # нарисовать линию регрессии
points(x=1350, y=P[1], col="red") # нарисовать точечный прогноз
lines(x=c(1350,1350,1350), y=P, col="red") # нарисовать интервальный прогноз

#A1-A5
T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию F1
regA5A1<-lm(formula=T$A5 ~T$A1) # построить регрессию
summary(regA5A1) # вывод информации о построенной регрессии
format(coef(regA5A1), digits =12) # вывод коэффициентов регрессии с точностью 12 знаков
plot(x=T$A1, y=T$A5) # нарисовать диаграмму рассеяния
abline(regA5A1, col="red") # нарисовать линию регрессии
mean(regA5A1$residuals)
plot(regA5A1$residuals, main="График остатков", xlab="Номер наблюдения",
     ylab="Остатки")
abline(h=0)
#install.packages("forecast")
library("forecast") # подключить библиотеку forecast
accuracy(regA5A1) # вывод оценок качества регрессии, в том числе MAPE
T<-T[1,] # оставить только одну строку в таблице Т
T$A1<- 1350 # записать значение 1350 в переменную A1
format(predict(regA5A1, newdata=T, interval="confidence", level=0.9), digits=10) # вывод точечного и интервального прогнозов
P<-predict(regA5A1, newdata=T, interval="confidence", level=0.9) # записать прогноз в переменную P
T<-read.table("reg.txt", header=TRUE) # снова прочитать данные из файла
T<-T[order(T$A1),]
plot(x=T$A1, y=T$A5) # нарисовать диаграмму рассеяния
abline(regA5A1) # нарисовать линию регрессии
points(x=1350, y=P[1], col="red") # нарисовать точечный прогноз
lines(x=c(1350,1350,1350), y=P, col="red") # нарисовать интервальный прогноз



#A1-A6
T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию F1
regA6A1<-lm(formula=T$A6 ~T$A1) # построить регрессию
summary(regA6A1) # вывод информации о построенной регрессии
format(coef(regA6A1), digits =12) # вывод коэффициентов регрессии с точностью 12 знаков
plot(x=T$A1, y=T$A6) # нарисовать диаграмму рассеяния
abline(regA6A1, col="red") # нарисовать линию регрессии
mean(regA6A1$residuals)
plot(regA6A1$residuals, main="График остатков", xlab="Номер наблюдения",
     ylab="Остатки")
abline(h=0)
#install.packages("forecast")
library("forecast") # подключить библиотеку forecast
accuracy(regA6A1) # вывод оценок качества регрессии, в том числе MAPE
T<-T[1,] # оставить только одну строку в таблице Т
T$A1<- 1350 # записать значение 1350 в переменную A1
format(predict(regA6A1, newdata=T, interval="confidence", level=0.9), digits=10) # вывод точечного и интервального прогнозов
P<-predict(regA6A1, newdata=T, interval="confidence", level=0.9) # записать прогноз в переменную P
T<-read.table("reg.txt", header=TRUE) # снова прочитать данные из файла
T<-T[order(T$A1),]
plot(x=T$A1, y=T$A6) # нарисовать диаграмму рассеяния
abline(regA6A1) # нарисовать линию регрессии
points(x=1350, y=P[1], col="red") # нарисовать точечный прогноз
lines(x=c(1350,1350,1350), y=P, col="red") # нарисовать интервальный прогноз

#A1-A7
T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию F1
regA7A1<-lm(formula=T$A7 ~T$A1) # построить регрессию
summary(regA7A1) # вывод информации о построенной регрессии
format(coef(regA7A1), digits =12) # вывод коэффициентов регрессии с точностью 12 знаков
plot(x=T$A1, y=T$A7) # нарисовать диаграмму рассеяния
abline(regA7A1, col="red") # нарисовать линию регрессии
mean(regA7A1$residuals)
plot(regA7A1$residuals, main="График остатков", xlab="Номер наблюдения",
     ylab="Остатки")
abline(h=0)
#install.packages("forecast")
library("forecast") # подключить библиотеку forecast
accuracy(regA7A1) # вывод оценок качества регрессии, в том числе MAPE
T<-T[1,] # оставить только одну строку в таблице Т
T$A1<- 1350 # записать значение 1350 в переменную A1
format(predict(regA7A1, newdata=T, interval="confidence", level=0.9), digits=10) # вывод точечного и интервального прогнозов
P<-predict(regA7A1, newdata=T, interval="confidence", level=0.9) # записать прогноз в переменную P
T<-read.table("reg.txt", header=TRUE) # снова прочитать данные из файла
T<-T[order(T$A1),]
plot(x=T$A1, y=T$A7) # нарисовать диаграмму рассеяния
abline(regA7A1) # нарисовать линию регрессии
points(x=1350, y=P[1], col="red") # нарисовать точечный прогноз
lines(x=c(1350,1350,1350), y=P, col="red") # нарисовать интервальный прогноз

#A1-A8
T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию F1
regA8A1<-lm(formula=T$A8 ~T$A1) # построить регрессию
summary(regA8A1) # вывод информации о построенной регрессии
format(coef(regA8A1), digits =12) # вывод коэффициентов регрессии с точностью 12 знаков
plot(x=T$A1, y=T$A8) # нарисовать диаграмму рассеяния
abline(regA8A1, col="red") # нарисовать линию регрессии
mean(regA8A1$residuals)
plot(regA8A1$residuals, main="График остатков", xlab="Номер наблюдения",
     ylab="Остатки")
abline(h=0)
#install.packages("forecast")
library("forecast") # подключить библиотеку forecast
accuracy(regA8A1) # вывод оценок качества регрессии, в том числе MAPE
T<-T[1,] # оставить только одну строку в таблице Т
T$A1<- 1350 # записать значение 1350 в переменную A1
format(predict(regA8A1, newdata=T, interval="confidence", level=0.9), digits=10) # вывод точечного и интервального прогнозов
P<-predict(regA8A1, newdata=T, interval="confidence", level=0.9) # записать прогноз в переменную P
T<-read.table("reg.txt", header=TRUE) # снова прочитать данные из файла
T<-T[order(T$A1),]
plot(x=T$A1, y=T$A8) # нарисовать диаграмму рассеяния
abline(regA8A1) # нарисовать линию регрессии
points(x=1350, y=P[1], col="red") # нарисовать точечный прогноз
lines(x=c(1350,1350,1350), y=P, col="red") # нарисовать интервальный прогноз

#A1-A9
T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию F1
regA9A1<-lm(formula=T$A9 ~T$A1) # построить регрессию
summary(regA9A1) # вывод информации о построенной регрессии
format(coef(regA9A1), digits =12) # вывод коэффициентов регрессии с точностью 12 знаков
plot(x=T$A1, y=T$A9) # нарисовать диаграмму рассеяния
abline(regA9A1, col="red") # нарисовать линию регрессии
mean(regA9A1$residuals)
plot(regA9A1$residuals, main="График остатков", xlab="Номер наблюдения",
     ylab="Остатки")
abline(h=0)
#install.packages("forecast")
library("forecast") # подключить библиотеку forecast
accuracy(regA9A1) # вывод оценок качества регрессии, в том числе MAPE
T<-T[1,] # оставить только одну строку в таблице Т
T$A1<- 1350 # записать значение 1350 в переменную A1
format(predict(regA9A1, newdata=T, interval="confidence", level=0.9), digits=10) # вывод точечного и интервального прогнозов
P<-predict(regA9A1, newdata=T, interval="confidence", level=0.9) # записать прогноз в переменную P
T<-read.table("reg.txt", header=TRUE) # снова прочитать данные из файла
T<-T[order(T$A1),]
plot(x=T$A1, y=T$A9) # нарисовать диаграмму рассеяния
abline(regA9A1) # нарисовать линию регрессии
points(x=1350, y=P[1], col="red") # нарисовать точечный прогноз
lines(x=c(1350,1350,1350), y=P, col="red") # нарисовать интервальный прогноз

#A1-A10
T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию F1
regA10A1<-lm(formula=T$A10 ~T$A1) # построить регрессию
summary(regA10A1) # вывод информации о построенной регрессии
format(coef(regA10A1), digits =12) # вывод коэффициентов регрессии с точностью 12 знаков
plot(x=T$A1, y=T$A10) # нарисовать диаграмму рассеяния
abline(regA10A1, col="red") # нарисовать линию регрессии
mean(regA10A1$residuals)
plot(regA10A1$residuals, main="График остатков", xlab="Номер наблюдения",
     ylab="Остатки")
abline(h=0)
#install.packages("forecast")
library("forecast") # подключить библиотеку forecast
accuracy(regA10A1) # вывод оценок качества регрессии, в том числе MAPE
T<-T[1,] # оставить только одну строку в таблице Т
T$A1<- 1350 # записать значение 1350 в переменную A1
format(predict(regA10A1, newdata=T, interval="confidence", level=0.9), digits=10) # вывод точечного и интервального прогнозов
P<-predict(regA10A1, newdata=T, interval="confidence", level=0.9) # записать прогноз в переменную P
T<-read.table("reg.txt", header=TRUE) # снова прочитать данные из файла
T<-T[order(T$A1),]
plot(x=T$A1, y=T$A10) # нарисовать диаграмму рассеяния
abline(regA10A1) # нарисовать линию регрессии
points(x=1350, y=P[1], col="red") # нарисовать точечный прогноз
lines(x=c(1350,1350,1350), y=P, col="red") # нарисовать интервальный прогноз

#A1-A11
T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию F1
regA11A1<-lm(formula=T$A11 ~T$A1) # построить регрессию
summary(regA11A1) # вывод информации о построенной регрессии
format(coef(regA11A1), digits =12) # вывод коэффициентов регрессии с точностью 12 знаков
plot(x=T$A1, y=T$A11) # нарисовать диаграмму рассеяния
abline(regA11A1, col="red") # нарисовать линию регрессии
mean(regA11A1$residuals)
plot(regA11A1$residuals, main="График остатков", xlab="Номер наблюдения",
     ylab="Остатки")
abline(h=0)
#install.packages("forecast")
library("forecast") # подключить библиотеку forecast
accuracy(regA11A1) # вывод оценок качества регрессии, в том числе MAPE
T<-T[1,] # оставить только одну строку в таблице Т
T$A1<- 1350 # записать значение 1350 в переменную A1
format(predict(regA11A1, newdata=T, interval="confidence", level=0.9), digits=10) # вывод точечного и интервального прогнозов
P<-predict(regA11A1, newdata=T, interval="confidence", level=0.9) # записать прогноз в переменную P
T<-read.table("reg.txt", header=TRUE) # снова прочитать данные из файла
T<-T[order(T$A1),]
plot(x=T$A1, y=T$A11) # нарисовать диаграмму рассеяния
abline(regA11A1) # нарисовать линию регрессии
points(x=1350, y=P[1], col="red") # нарисовать точечный прогноз
lines(x=c(1350,1350,1350), y=P, col="red") # нарисовать интервальный прогноз

#A1-A12
T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию F1
regA12A1<-lm(formula=T$A12 ~T$A1) # построить регрессию
summary(regA12A1) # вывод информации о построенной регрессии
format(coef(regA12A1), digits =12) # вывод коэффициентов регрессии с точностью 12 знаков
plot(x=T$A1, y=T$A12) # нарисовать диаграмму рассеяния
abline(regA12A1, col="red") # нарисовать линию регрессии
mean(regA12A1$residuals)
plot(regA12A1$residuals, main="График остатков", xlab="Номер наблюдения",
     ylab="Остатки")
abline(h=0)
#install.packages("forecast")
library("forecast") # подключить библиотеку forecast
accuracy(regA12A1) # вывод оценок качества регрессии, в том числе MAPE
T<-T[1,] # оставить только одну строку в таблице Т
T$A1<- 1350 # записать значение 1350 в переменную A1
format(predict(regA12A1, newdata=T, interval="confidence", level=0.9), digits=10) # вывод точечного и интервального прогнозов
P<-predict(regA12A1, newdata=T, interval="confidence", level=0.9) # записать прогноз в переменную P
T<-read.table("reg.txt", header=TRUE) # снова прочитать данные из файла
T<-T[order(T$A1),]
plot(x=T$A1, y=T$A12) # нарисовать диаграмму рассеяния
abline(regA12A1) # нарисовать линию регрессии
points(x=1350, y=P[1], col="red") # нарисовать точечный прогноз
lines(x=c(1350,1350,1350), y=P, col="red") # нарисовать интервальный прогноз









#A1-A12
T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию F1
regA12A1<-lm(formula=T$A12 ~T$A1) # построить регрессию
summary(regA12A1) # вывод информации о построенной регрессии
format(coef(regA12A1), digits =12) # вывод коэффициентов регрессии с точностью 12 знаков
plot(x=T$A1, y=T$A12) # нарисовать диаграмму рассеяния
abline(regA12A1, col="red") # нарисовать линию регрессии
mean(regA12A1$residuals)
plot(regA12A1$residuals, main="График остатков", xlab="Номер наблюдения",
     ylab="Остатки")
abline(h=0)
#install.packages("forecast")
library("forecast") # подключить библиотеку forecast
accuracy(regA12A1) # вывод оценок качества регрессии, в том числе MAPE
T<-T[1,] # оставить только одну строку в таблице Т
T$A1<- 1350 # записать значение 1350 в переменную A1
format(predict(regA12A1, newdata=T, interval="confidence", level=0.9), digits=10) # вывод точечного и интервального прогнозов
P<-predict(regA12A1, newdata=T, interval="confidence", level=0.9) # записать прогноз в переменную P
T<-read.table("reg.txt", header=TRUE) # снова прочитать данные из файла
T<-T[order(T$A1),]
plot(x=T$A1, y=T$A12) # нарисовать диаграмму рассеяния
abline(regA12A1) # нарисовать линию регрессии
points(x=1350, y=P[1], col="red") # нарисовать точечный прогноз
lines(x=c(1350,1350,1350), y=P, col="red") # нарисовать интервальный прогноз


setwd("D:/R lab/3") # установить рабочую папку
T<-read.table("reg.txt", header=TRUE) # прочитать данные из файла и записать в таблицу T
#A1-A12
T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию F1
regA12A1<-lm(formula=T$A12 ~T$A1) # построить регрессию
summary(regA12A1) # вывод информации о построенной регрессии
format(coef(regA12A1), digits =12) # вывод коэффициентов регрессии с точностью 12 знаков
plot(x=T$A1, y=T$A12) # нарисовать диаграмму рассеяния
abline(regA12A1, col="red") # нарисовать линию регрессии
mean(regA12A1$residuals)
plot(regA12A1$residuals, main="График остатков", xlab="Номер наблюдения",
     ylab="Остатки")
abline(h=0)
#install.packages("forecast")
library("forecast") # подключить библиотеку forecast
accuracy(regA12A1) # вывод оценок качества регрессии, в том числе MAPE
T<-T[1,] # оставить только одну строку в таблице Т
T$A1<- 1350 # записать значение 1350 в переменную A1
format(predict(regA12A1, newdata=T, interval="confidence", level=0.9), digits=10) # вывод точечного и интервального прогнозов
P<-predict(regA12A1, newdata=T, interval="confidence", level=0.9) # записать прогноз в переменную P
T<-read.table("reg.txt", header=TRUE) # снова прочитать данные из файла
T<-T[order(T$A1),]
plot(x=T$A1, y=T$A12) # нарисовать диаграмму рассеяния
abline(regA12A1) # нарисовать линию регрессии
points(x=1350, y=P[1], col="red") # нарисовать точечный прогноз
lines(x=c(1350,1350,1350), y=P, col="red") # нарисовать интервальный прогноз



