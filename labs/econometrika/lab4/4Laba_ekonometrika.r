#Читаем из файла перед каждым регрессионным анализом 
setwd("C:/Users/regst/Desktop/учёба/Эконометрика/lab4")
T<-read.table("reg.txt", header=TRUE)


T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию А1
#Построим несколько нелинейных регрессий для переменных А9 и А1
#Исследуем регрессию: A9 = P1+P2*ln(A1) + eps
reg9<-lm(formula=T$A9 ~T$A1) # построить линейную регрессию
reg9.1<-lm(formula=T$A9 ~log(T$A1)) # построить логарифмическую регрессию
summary(reg9.1) # Все коэффициенты значимы
plot(x=T$A1,y=T$A9) # нарисовать диаграмму рассеяния
abline(reg9, col="red") # нарисовать линейную регрессию
curve(coef(reg9.1)[1] + coef(reg9.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
plot(reg9.1$residuals, main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
library("forecast") # подключить библиотеку forecast
accuracy(reg9.1) # рассчитать оценку регрессии MAPE
#Исследуем регрессию: A9 = P1 + P2/(P3+A1) + eps
reg9.2<-nls(T$A9~p1 + p2/(p3 + T$A1), data=T, start=list(p1=500, p2=-10000, p3=-1000)) #построить нелинейную регрессию с параметрами
summary(reg9.2) # вывести коэффициенты регрессии
P<-coef(reg9.2) # сохранить коэффициенты регрессии в переменной Р
plot(x=T$A1,y=T$A9) # нарисовать диаграмму рассеяния
abline(reg9, col="red") #нарисовать линейную регрессию
curve(coef(reg9.1)[1] + coef(reg9.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
curve(P[1] + P[2]/(x+P[3]), add=TRUE, col="blue") # нарисовать нелинейную регрессию
plot(reg9.2$m$resid(), main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
sum(abs((T$A9 - (P[1]+ P[2]/(P[3]+T$A1)))/T$A9))/length(T$A9)*100 # рассчитать MAPE
#Строим прогноз по регрессии: A9 = P1 + P2/(P3+A1) + eps
P[1] + P[2]/(P[3] + 1350) # рассчитать прогноз для А1=1350


T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию А1
#Построим несколько нелинейных регрессий для переменных А2 и А1
#Исследуем регрессию: A2 = P1+P2*ln(A1) + eps
reg2<-lm(formula=T$A2 ~T$A1) # построить линейную регрессию
reg2.1<-lm(formula=T$A2 ~log(T$A1)) # построить логарифмическую регрессию
summary(reg2.1) # Все коэффициенты значимы
plot(x=T$A1,y=T$A2) # нарисовать диаграмму рассеяния
abline(reg2, col="red") # нарисовать линейную регрессию
curve(coef(reg2.1)[1] + coef(reg2.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
plot(reg2.1$residuals, main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
library("forecast") # подключить библиотеку forecast
accuracy(reg2.1) # рассчитать оценку регрессии MAPE
#Исследуем регрессию: A2 = P1 + P2/(P3+A1) + eps
reg2.2<-nls(T$A2~p1 + p2/(p3 + T$A1), data=T, start=list(p1=500, p2=-10000, p3=-1000)) #построить нелинейную регрессию с параметрами
summary(reg2.2) # вывести коэффициенты регрессии
P<-coef(reg2.2) # сохранить коэффициенты регрессии в переменной Р
plot(x=T$A1,y=T$A2) # нарисовать диаграмму рассеяния
abline(reg2, col="red") #нарисовать линейную регрессию
curve(coef(reg2.1)[1] + coef(reg2.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
curve(P[1] + P[2]/(x+P[3]), add=TRUE, col="blue") # нарисовать нелинейную регрессию
plot(reg2.2$m$resid(), main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
sum(abs((T$A2 - (P[1]+ P[2]/(P[3]+T$A1)))/T$A2))/length(T$A2)*100 # рассчитать MAPE
#Строим прогноз по регрессии: A2 = P1 + P2/(P3+A1) + eps
P[1] + P[2]/(P[3] + 1350) # рассчитать прогноз для А1=1350


T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию А1
#Построим несколько нелинейных регрессий для переменных А3 и А1
#Исследуем регрессию: A3 = P1+P2*ln(A1) + eps
reg3<-lm(formula=T$A3 ~T$A1) # построить линейную регрессию
reg3.1<-lm(formula=T$A3 ~log(T$A1)) # построить логарифмическую регрессию
summary(reg3.1) # Все коэффициенты значимы
plot(x=T$A1,y=T$A3) # нарисовать диаграмму рассеяния
abline(reg3, col="red") # нарисовать линейную регрессию
curve(coef(reg3.1)[1] + coef(reg3.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
plot(reg3.1$residuals, main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
library("forecast") # подключить библиотеку forecast
accuracy(reg3.1) # рассчитать оценку регрессии MAPE

T<-T[1,] # оставить только одну строку в таблице Т
T$A1<- 1350 # записать значение 1350 в переменную F1
format(predict(reg3.1, newdata=T, interval="confidence", level=0.9), digits=10) # вывод точечного и интервального прогнозов

#Исследуем регрессию: A3 = P1 + P2/(P3+A1) + eps
reg3.2<-nls(T$A3~p1 + p2/(p3 + T$A1), data=T, start=list(p1=500, p2=-10000, p3=-1000)) #построить нелинейную регрессию с параметрами
summary(reg3.2) # вывести коэффициенты регрессии
P<-coef(reg3.2) # сохранить коэффициенты регрессии в переменной Р
plot(x=T$A1,y=T$A3) # нарисовать диаграмму рассеяния
abline(reg3, col="red") #нарисовать линейную регрессию
curve(coef(reg3.1)[1] + coef(reg3.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
curve(P[1] + P[2]/(x+P[3]), add=TRUE, col="blue") # нарисовать нелинейную регрессию
plot(reg3.2$m$resid(), main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
sum(abs((T$A3 - (P[1]+ P[2]/(P[3]+T$A1)))/T$A3))/length(T$A3)*100 # рассчитать MAPE

#Строим прогноз по регрессии: A3 = P1 + P2/(P3+A1) + eps
P[1] + P[2]/(P[3] + 1350) # рассчитать прогноз для А1=1350


T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию А1
#Построим несколько нелинейных регрессий для переменных А4 и А1
#Исследуем регрессию: A4 = P1+P2*ln(A1) + eps
reg4<-lm(formula=T$A4 ~T$A1) # построить линейную регрессию
reg4.1<-lm(formula=T$A4 ~log(T$A1)) # построить логарифмическую регрессию
summary(reg4.1) # Все коэффициенты значимы
plot(x=T$A1,y=T$A4) # нарисовать диаграмму рассеяния
abline(reg4, col="red") # нарисовать линейную регрессию
curve(coef(reg4.1)[1] + coef(reg4.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
plot(reg4.1$residuals, main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
library("forecast") # подключить библиотеку forecast
accuracy(reg4.1) # рассчитать оценку регрессии MAPE

T<-T[1,] # оставить только одну строку в таблице Т
T$A1<- 1350 # записать значение 1350 в переменную F1
format(predict(reg4.1, newdata=T, interval="confidence", level=0.9), digits=10) # вывод точечного и интервального прогнозов

#Исследуем регрессию: A4 = P1 + P2/(P3+A1) + eps
reg4.2<-nls(T$A4~p1 + p2/(p3 + T$A1), data=T, start=list(p1=500, p2=-10000, p3=-1000)) #построить нелинейную регрессию с параметрами
summary(reg4.2) # вывести коэффициенты регрессии
P<-coef(reg4.2) # сохранить коэффициенты регрессии в переменной Р
plot(x=T$A1,y=T$A4) # нарисовать диаграмму рассеяния
abline(reg4, col="red") #нарисовать линейную регрессию
curve(coef(reg4.1)[1] + coef(reg4.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
curve(P[1] + P[2]/(x+P[3]), add=TRUE, col="blue") # нарисовать нелинейную регрессию
plot(reg4.2$m$resid(), main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
sum(abs((T$A4 - (P[1]+ P[2]/(P[3]+T$A1)))/T$A4))/length(T$A4)*100 # рассчитать MAPE

#Строим прогноз по регрессии: A4 = P1 + P2/(P3+A1) + eps
P[1] + P[2]/(P[3] + 1350) # рассчитать прогноз для А1=1350


T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию А1
#Построим несколько нелинейных регрессий для переменных А5 и А1
#Исследуем регрессию: A5 = P1+P2*ln(A1) + eps
reg5<-lm(formula=T$A5 ~T$A1) # построить линейную регрессию
reg5.1<-lm(formula=T$A5 ~log(T$A1)) # построить логарифмическую регрессию
summary(reg5.1) # Все коэффициенты значимы
plot(x=T$A1,y=T$A5) # нарисовать диаграмму рассеяния
abline(reg5, col="red") # нарисовать линейную регрессию
curve(coef(reg5.1)[1] + coef(reg5.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
plot(reg5.1$residuals, main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
library("forecast") # подключить библиотеку forecast
accuracy(reg5.1) # рассчитать оценку регрессии MAPE

#Исследуем регрессию: A5 = P1 + P2/(P3+A1) + eps
reg5.2<-nls(T$A5~p1 + p2/(p3 + T$A1), data=T, start=list(p1=500, p2=-10000, p3=-1000)) #построить нелинейную регрессию с параметрами
summary(reg5.2) # вывести коэффициенты регрессии
P<-coef(reg5.2) # сохранить коэффициенты регрессии в переменной Р
plot(x=T$A1,y=T$A5) # нарисовать диаграмму рассеяния
abline(reg5, col="red") #нарисовать линейную регрессию
curve(coef(reg5.1)[1] + coef(reg5.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
curve(P[1] + P[2]/(x+P[3]), add=TRUE, col="blue") # нарисовать нелинейную регрессию
plot(reg5.2$m$resid(), main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
sum(abs((T$A5 - (P[1]+ P[2]/(P[3]+T$A1)))/T$A5))/length(T$A5)*100 # рассчитать MAPE

#Строим прогноз по регрессии: A5 = P1 + P2/(P3+A1) + eps
P[1] + P[2]/(P[3] + 1350) # рассчитать прогноз для А1=1350



T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию А1
#Построим несколько нелинейных регрессий для переменных А6 и А1
#Исследуем регрессию: A6 = P1+P2*ln(A1) + eps
reg6<-lm(formula=T$A6 ~T$A1) # построить линейную регрессию
reg6.1<-lm(formula=T$A6 ~log(T$A1)) # построить логарифмическую регрессию
summary(reg6.1) # Все коэффициенты значимы
plot(x=T$A1,y=T$A6) # нарисовать диаграмму рассеяния
abline(reg6, col="red") # нарисовать линейную регрессию
curve(coef(reg6.1)[1] + coef(reg6.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
plot(reg6.1$residuals, main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
library("forecast") # подключить библиотеку forecast
accuracy(reg6.1) # рассчитать оценку регрессии MAPE

#Исследуем регрессию: A6 = P1 + P2/(P3+A1) + eps
reg6.2<-nls(T$A6~p1 + p2/(p3 + T$A1), data=T, start=list(p1=500, p2=-10000, p3=-1000)) #построить нелинейную регрессию с параметрами
summary(reg6.2) # вывести коэффициенты регрессии
P<-coef(reg6.2) # сохранить коэффициенты регрессии в переменной Р
plot(x=T$A1,y=T$A6) # нарисовать диаграмму рассеяния
abline(reg6, col="red") #нарисовать линейную регрессию
curve(coef(reg6.1)[1] + coef(reg6.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
curve(P[1] + P[2]/(x+P[3]), add=TRUE, col="blue") # нарисовать нелинейную регрессию
plot(reg6.2$m$resid(), main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
sum(abs((T$A6 - (P[1]+ P[2]/(P[3]+T$A1)))/T$A6))/length(T$A6)*100 # рассчитать MAPE

#Строим прогноз по регрессии: A6 = P1 + P2/(P3+A1) + eps
P[1] + P[2]/(P[3] + 1350) # рассчитать прогноз для А1=1350



T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию А1
#Построим несколько нелинейных регрессий для переменных А7 и А1
#Исследуем регрессию: A7 = P1+P2*ln(A1) + eps
reg7<-lm(formula=T$A7 ~T$A1) # построить линейную регрессию
reg7.1<-lm(formula=T$A7 ~log(T$A1)) # построить логарифмическую регрессию
summary(reg7.1) # Все коэффициенты значимы
plot(x=T$A1,y=T$A7) # нарисовать диаграмму рассеяния
abline(reg7, col="red") # нарисовать линейную регрессию
curve(coef(reg7.1)[1] + coef(reg7.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
plot(reg7.1$residuals, main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
library("forecast") # подключить библиотеку forecast
accuracy(reg7.1) # рассчитать оценку регрессии MAPE

#Исследуем регрессию: A7 = P1 + P2/(P3+A1) + eps
reg7.2<-nls(T$A7~p1 + p2/(p3 + T$A1), data=T, start=list(p1=500, p2=-10000, p3=-1000)) #построить нелинейную регрессию с параметрами
summary(reg7.2) # вывести коэффициенты регрессии
P<-coef(reg7.2) # сохранить коэффициенты регрессии в переменной Р
plot(x=T$A1,y=T$A7) # нарисовать диаграмму рассеяния
abline(reg7, col="red") #нарисовать линейную регрессию
curve(coef(reg7.1)[1] + coef(reg7.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
curve(P[1] + P[2]/(x+P[3]), add=TRUE, col="blue") # нарисовать нелинейную регрессию
plot(reg7.2$m$resid(), main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
sum(abs((T$A7 - (P[1]+ P[2]/(P[3]+T$A1)))/T$A7))/length(T$A7)*100 # рассчитать MAPE

#Строим прогноз по регрессии: A7 = P1 + P2/(P3+A1) + eps
P[1] + P[2]/(P[3] + 1350) # рассчитать прогноз для А1=1350


T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию А1
#Построим несколько нелинейных регрессий для переменных А8 и А1
#Исследуем регрессию: A8 = P1+P2*ln(A1) + eps
reg8<-lm(formula=T$A8 ~T$A1) # построить линейную регрессию
reg8.1<-lm(formula=T$A8 ~log(T$A1)) # построить логарифмическую регрессию
summary(reg8.1) # Все коэффициенты значимы
plot(x=T$A1,y=T$A8) # нарисовать диаграмму рассеяния
abline(reg8, col="red") # нарисовать линейную регрессию
curve(coef(reg8.1)[1] + coef(reg8.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
plot(reg8.1$residuals, main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
library("forecast") # подключить библиотеку forecast
accuracy(reg8.1) # рассчитать оценку регрессии MAPE

#Исследуем регрессию: A8 = P1 + P2/(P3+A1) + eps
reg8.2<-nls(T$A8~p1 + p2/(p3 + T$A1), data=T, start=list(p1=500, p2=-10000, p3=-1000)) #построить нелинейную регрессию с параметрами
summary(reg8.2) # вывести коэффициенты регрессии
P<-coef(reg8.2) # сохранить коэффициенты регрессии в переменной Р
plot(x=T$A1,y=T$A8) # нарисовать диаграмму рассеяния
abline(reg8, col="red") #нарисовать линейную регрессию
curve(coef(reg8.1)[1] + coef(reg8.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
curve(P[1] + P[2]/(x+P[3]), add=TRUE, col="blue") # нарисовать нелинейную регрессию
plot(reg8.2$m$resid(), main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
sum(abs((T$A8 - (P[1]+ P[2]/(P[3]+T$A1)))/T$A8))/length(T$A8)*100 # рассчитать MAPE

#Строим прогноз по регрессии: A8 = P1 + P2/(P3+A1) + eps
P[1] + P[2]/(P[3] + 1350) # рассчитать прогноз для А1=1350


T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию А1
#Построим несколько нелинейных регрессий для переменных А10 и А1
#Исследуем регрессию: A10 = P1+P2*ln(A1) + eps
reg10<-lm(formula=T$A10 ~T$A1) # построить линейную регрессию
reg10.1<-lm(formula=T$A10 ~log(T$A1)) # построить логарифмическую регрессию
summary(reg10.1) # Все коэффициенты значимы
plot(x=T$A1,y=T$A10) # нарисовать диаграмму рассеяния
abline(reg10, col="red") # нарисовать линейную регрессию
curve(coef(reg10.1)[1] + coef(reg10.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
plot(reg10.1$residuals, main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
library("forecast") # подключить библиотеку forecast
accuracy(reg10.1) # рассчитать оценку регрессии MAPE

T<-T[1,] # оставить только одну строку в таблице Т
T$A1<- 1350 # записать значение 1350 в переменную F1
format(predict(reg10.1, newdata=T, interval="confidence", level=0.9), digits=10) # вывод точечного и интервального прогнозов


#Исследуем регрессию: A10 = P1 + P2/(P3+A1) + eps
reg10.2<-nls(T$A10~p1 + p2/(p3 + T$A1), data=T, start=list(p1=500, p2=-10000, p3=-1000)) #построить нелинейную регрессию с параметрами
summary(reg10.2) # вывести коэффициенты регрессии
P<-coef(reg10.2) # сохранить коэффициенты регрессии в переменной Р
plot(x=T$A1,y=T$A10) # нарисовать диаграмму рассеяния
abline(reg10, col="red") #нарисовать линейную регрессию
curve(coef(reg10.1)[1] + coef(reg10.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
curve(P[1] + P[2]/(x+P[3]), add=TRUE, col="blue") # нарисовать нелинейную регрессию
plot(reg10.2$m$resid(), main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
sum(abs((T$A10 - (P[1]+ P[2]/(P[3]+T$A1)))/T$A10))/length(T$A10)*100 # рассчитать MAPE

#Строим прогноз по регрессии: A10 = P1 + P2/(P3+A1) + eps
P[1] + P[2]/(P[3] + 1350) # рассчитать прогноз для А1=1350


T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию А1
#Построим несколько нелинейных регрессий для переменных А11 и А1
#Исследуем регрессию: A11 = P1+P2*ln(A1) + eps
reg11<-lm(formula=T$A11 ~T$A1) # построить линейную регрессию
reg11.1<-lm(formula=T$A11 ~log(T$A1)) # построить логарифмическую регрессию
summary(reg11.1) # Все коэффициенты значимы
plot(x=T$A1,y=T$A11) # нарисовать диаграмму рассеяния
abline(reg11, col="red") # нарисовать линейную регрессию
curve(coef(reg11.1)[1] + coef(reg11.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
plot(reg11.1$residuals, main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
library("forecast") # подключить библиотеку forecast
accuracy(reg11.1) # рассчитать оценку регрессии MAPE

T<-T[1,] # оставить только одну строку в таблице Т
T$A1<- 1350 # записать значение 1350 в переменную F1
format(predict(reg11.1, newdata=T, interval="confidence", level=0.9), digits=10) # вывод точечного и интервального прогнозов

#Исследуем регрессию: A11 = P1 + P2/(P3+A1) + eps
reg11.2<-nls(T$A11~p1 + p2/(p3 + T$A1), data=T, start=list(p1=500, p2=-10000, p3=-1000)) #построить нелинейную регрессию с параметрами
summary(reg11.2) # вывести коэффициенты регрессии
P<-coef(reg11.2) # сохранить коэффициенты регрессии в переменной Р
plot(x=T$A1,y=T$A11) # нарисовать диаграмму рассеяния
abline(reg11, col="red") #нарисовать линейную регрессию
curve(coef(reg11.1)[1] + coef(reg11.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
curve(P[1] + P[2]/(x+P[3]), add=TRUE, col="blue") # нарисовать нелинейную регрессию
plot(reg11.2$m$resid(), main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
sum(abs((T$A11 - (P[1]+ P[2]/(P[3]+T$A1)))/T$A11))/length(T$A11)*100 # рассчитать MAPE

#Строим прогноз по регрессии: A11 = P1 + P2/(P3+A1) + eps
P[1] + P[2]/(P[3] + 1350) # рассчитать прогноз для А1=1350



T<-T[order(T$A1),] # сортировать строки в таблице Т по возрастанию А1
#Построим несколько нелинейных регрессий для переменных А12 и А1
#Исследуем регрессию: A12 = P1+P2*ln(A1) + eps
reg12<-lm(formula=T$A12 ~T$A1) # построить линейную регрессию
reg12.1<-lm(formula=T$A12 ~log(T$A1)) # построить логарифмическую регрессию
summary(reg12.1) # Все коэффициенты значимы
plot(x=T$A1,y=T$A12) # нарисовать диаграмму рассеяния
abline(reg12, col="red") # нарисовать линейную регрессию
curve(coef(reg12.1)[1] + coef(reg12.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
plot(reg12.1$residuals, main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
library("forecast") # подключить библиотеку forecast
accuracy(reg12.1) # рассчитать оценку регрессии MAPE

#Исследуем регрессию: A12 = P1 + P2/(P3+A1) + eps
reg12.2<-nls(T$A12~p1 + p2/(p3 + T$A1), data=T, start=list(p1=500, p2=-10000, p3=-1000)) #построить нелинейную регрессию с параметрами
summary(reg12.2) # вывести коэффициенты регрессии
P<-coef(reg12.2) # сохранить коэффициенты регрессии в переменной Р
plot(x=T$A1,y=T$A12) # нарисовать диаграмму рассеяния
abline(reg12, col="red") #нарисовать линейную регрессию
curve(coef(reg12.1)[1] + coef(reg12.1)[2]*log(x), add=TRUE, col="green") # нарисовать нелинейную регрессию
curve(P[1] + P[2]/(x+P[3]), add=TRUE, col="blue") # нарисовать нелинейную регрессию
plot(reg12.2$m$resid(), main="График остатков", xlab="Номер наблюдения", ylab="Остатки")
abline(h=0, col="red")
sum(abs((T$A12 - (P[1]+ P[2]/(P[3]+T$A1)))/T$A12))/length(T$A12)*100 # рассчитать MAPE

#Строим прогноз по регрессии: A12 = P1 + P2/(P3+A1) + eps
P[1] + P[2]/(P[3] + 1350) # рассчитать прогноз для А1=1350



