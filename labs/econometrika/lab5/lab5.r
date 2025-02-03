#install.packages("xlsx", dep = T)
library("xlsx")
setwd("D:/R lab/5/Sasha")
M<-read.xlsx("Milk2.xlsx", sheetIndex = "Milk2",  sep=";")
View(M)

#Название субъекта федерации, Цена на молоко, 
#Среднедушевые доходы, Численность населения,
#Федеральный округ

#Корреляционный анализ числовых переменных таблицы M
cor(data.frame(M$MilkPrice,M$Income,M$Population))

#4. Корреляционный анализ:
#прямая средняя зависимость между Ценами на молоко и Среднедушевыми доходами.
#обратная слабая зависимость между Ценами на молоко и Численностью населения.
#Между экзогенными факторами зависимость слабая. 
#Явление мультиколлинеарности не наблюдается(между признаками нет сильной зависимости)

# 5.Построим диаграмму рассеяния для Цен на молоко и Среднедушевых доходов
plot(x=M$Income,y=M$MilkPrice, main="Зависимость цены от дохода")
# 6.Отсортируем исходные данные по возрастанию Среднедушевых доходов
M<-M[order(M$Income),]

#7. Построим регрессию для Цен на молоко и Среднедушевых доходов
reg1<-lm(M$MilkPrice~M$Income)
summary(reg1)
abline(reg1)
plot(residuals(reg1))
abline(h=0, col="red")
library("forecast")
accuracy(reg1)

#8. Построим регрессию для Цен на молоко и Численности населения
plot(x=M$Population,y=M$MilkPrice, main="Зависимость цены от численности населения" ,xlab = "Среднедушевые доходы", ylab = "Цена на молоко")
M<-M[order(M$Population),]
reg2<-lm(M$MilkPrice~M$Population)
summary(reg2)
abline(reg2)
plot(residuals(reg2))
abline(h=0, col="red")
accuracy(reg2)

#9. Построим множественную линейную регрессию для Цен на молоко, 
# Среднедушевых доходов и Численности населения
reg3<-lm(M$MilkPrice~M$Income+M$Population)
summary(reg3)
accuracy(reg3)
plot(residuals(reg3))
abline(h=0, col="red")

#10. Построим множественную нелинейную регрессию для Цен на молоко, 
# Среднедушевых доходов и Численности населения. 
# Оценка остатков по доходам
M<-M[order(M$Income),]
reg3.1<-lm(M$MilkPrice~M$Income+M$Population)
M<-M[order(M$Income),]
summary(reg3.1)
accuracy(reg3.1)
plot(residuals(reg3.1))
abline(h=0, col="red")

#11. Множественную нелинейную регрессию для Цен на молоко, 
# Среднедушевых доходов и Численности населения
# Оценка остатков по численности населения
M<-M[order(M$Population),]
reg3.2<-lm(M$MilkPrice~M$Income+M$Population)
M<-M[order(M$Income),]
summary(reg3.2)
accuracy(reg3.2)
plot(residuals(reg3.2))
abline(h=0, col="red")

#12. Постройте частные уравнения регрессии
#Частные уравнения регрессии связывают результативный признак с соответствующими факторами х 
#при закреплении других, учитываемых во множественной регрессии, факторов на среднем уровне.

coefficients(reg3.2)
mean(M$Income)
mean(M$Population)
# MilkPrice = 2.004313e+01 + 9.768220e-04*Income - 2.176969e-06*Population + e 

-2.176969e-06*mean(M$Population)+2.004313e+01 #  (16.20918) 
# MilkPrice(Income) = 16.20918 + 9.768220e-04*Income + e           # доход

9.768220e-04*mean(M$Income)+2.004313e+01  #  (40.4781)
# MilkPrice(Population) = 40.4781 - 2.176969e-06*Population + e    # население

#13. Постройте графики для частных коэффициентов эластичности

milk = 2.004313e+01 + 9.768220e-04*mean(M$Income) - 2.176969e-06*mean(M$Population)

#Усредненный коэфф. эластичности фактора дохода
#производная функции по доходам * среднее значение доходов / среднее значение milk
9.768220e-04 * mean(M$Income) / milk

#Усредненный коэфф. эластичности фактора популяции
#производная функции по численности населения * среднее значение численности населения / среднее значение milk
-2.176969e-06 * mean(M$Population) / milk

#график эластичности для доходов
plot(9.768220e-04 * M[order(M$Income),]$Income / milk, type = 'l', main = 'График эластичности по доходу',
     xlab = 'Наблюдение', ylab = 'Коэффициент эластичности', col='blue')
#график эластичности для численности населения
plot(-2.176969e-06 * M[order(M$Population),]$Population / milk, type = 'l', main = 'График эластичности по численности населения',
     xlab = 'Наблюдение', ylab = 'Коэффициент эластичности', col='red')


#14. Построим множественную нелинейную регрессию для Цен на молоко,
#Среднедушевых доходов, Численности населения и Федерального округа. 
#Будем считать, что фактор Федеральный округ влияет на свободный член. Создадим 8
#фиктивных переменных и заполним их данными.
ZCFO<-rep(0, times=length(M$FO))
ZUFO<-rep(0, times=length(M$FO))
ZSZFO<-rep(0, times=length(M$FO))
ZUrFO<-rep(0, times=length(M$FO))
ZPFO<-rep(0, times=length(M$FO))
ZSKFO<-rep(0, times=length(M$FO))
ZSFO<-rep(0, times=length(M$FO))
ZDVFO<-rep(0, times=length(M$FO))
ZCFO[M$FO=="ЦФО"]<-1
ZUFO[M$FO=="ЮФО"]<-1
ZSZFO[M$FO=="СЗФО"]<-1
ZUrFO[M$FO=="УФО"]<-1
ZPFO[M$FO=="ПФО"]<-1
ZSKFO[M$FO=="СКФО"]<-1
ZSFO[M$FO=="СФО"]<-1
ZDVFO[M$FO=="ДВФО"]<-1
M1<-data.frame(M,ZCFO,ZUFO,ZSZFO,ZUrFO,ZPFO,ZSKFO,ZSFO,ZDVFO)
rm(ZCFO,ZUFO,ZSZFO,ZUrFO,ZPFO,ZSKFO,ZSFO, ZDVFO)
M1<-M1[order(M1$MilkPrice),]
View(M1)

#15. Построим множественную нелинейную регрессию с учетом фиктивных переменных.
reg4.1<-lm(M1$MilkPrice ~ M1$Income +M1$Population + M1$ZCFO + M1$ZUFO + M1$ZSZFO + M1$ZUrFO + M1$ZPFO + M1$ZSKFO + M1$ZSFO + M1$ZDVFO)
summary(reg4.1)
accuracy(reg4.1)

coefficients(reg4.1)
plot(residuals(reg4.1))
abline(h=0, col="red")

zcfo<- M[M$FO == "ЦФО", ]
zufo<- M[M$FO == "ЮФО", ]
zszfo<- M[M$FO == "СЗФО", ]
zurfo<- M[M$FO == "УФО", ]
zpfo<- M[M$FO == "ПФО", ]
zskfo<- M[M$FO == "СКФО", ]
zsfo<- M[M$FO == "СФО", ]
zdvfo<- M[M$FO == "ДВФО", ]
mean(zcfo$MilkPrice)  # 31.33
mean(zufo$MilkPrice)  # 31.95167
mean(zszfo$MilkPrice) # 40.46636
mean(zurfo$MilkPrice) # 42.75833
mean(zpfo$MilkPrice)  # 29.62786
mean(zskfo$MilkPrice) # 33.89143
mean(zsfo$MilkPrice)  # 36.64917
mean(zdvfo$MilkPrice) # 56.95875

#16. Ответьте на вопросы:
#  a. Оказывает ли фактор Федеральный округ влияние на Цены на молоко? Да
#  b. В каком федеральном округе самые высокие цены на молоко?
#     Дальневосточный федеральный округ (56.95875)

#  c. В каком федеральном округе самые низкие цены на молоко?
#     Приволжский федеральный округ (29.62786)

#  d. Можно ли использовать построенную модель для прогнозирования?
#     MAPE = 9.57%, но остатки распределены неравномерно. Модель не стоит 
#     использовать для прогнозирования.


#17. Запишем для каждого федерального округа соответствующее уравнение регрессии:
#e. Центральный федеральный округ:
#MilkPrice= 17,2511 + 0,000827604*Income - 0,00000131397*Population +E
#f. Южный федеральный округ:
#MilkPrice= 21,2280 + 0,000827604*Income - 0,00000131397*Population +E
#g. Северо-западный федеральный округ:
#MilkPrice= 21,0397 + 0,000827604*Income - 0,00000131397*Population +E


#35.56 + коэф для округа конкретного из reg4.1
format(coef(reg4.1), digits =8)
mean(coefficients(reg4.1)[4]+35.56)  #17.24628 
mean(coefficients(reg4.1)[5]+35.56)  #21.22323
mean(coefficients(reg4.1)[6]+35.56)  #21.03489
mean(coefficients(reg4.1)[7]+35.56)  #19.91181
mean(coefficients(reg4.1)[8]+35.56)  #17.63019
mean(coefficients(reg4.1)[9]+35.56)  #22.90860
mean(coefficients(reg4.1)[10]+35.56) #24.51846
mean(coefficients(reg4.1)[11]+35.56) #35,56448

#УФО
#MilkPrice = 19.91181 + 8.736e-05*Income - 1.314e-06*Population + e
#ПФО
#MilkPrice = 17.63019 + 8.736e-05*Income - 1.314e-06*Population + e
#СКФО
#MilkPrice = 22.90860 + 8.736e-05*Income - 1.314e-06*Population + e
#СФО
#MilkPrice = 24.51846 + 8.736e-05*Income - 1.314e-06*Population + e
#ДВФО
#MilkPrice = 35,56448 + 8.276e-05*Income - 1.313e-06*Population + e

#18. Проверьте по критерию Чоу наличие неоднородности в данных.
reg3.2<-lm(M$MilkPrice~M$Income+M$Population)
reg4.1<-lm(M1$MilkPrice ~ M1$Income +M1$Population + M1$ZCFO + M1$ZUFO + M1$ZSZFO + M1$ZUrFO + M1$ZPFO + M1$ZSKFO + M1$ZSFO + M1$ZDVFO)

Q<- sum(residuals(reg3.2)^2)  #сумма квадратов остатков от общих данных                   
Q#3952.937

Q_fikt <- sum(residuals(reg4.1)^2) #сумма квадратов остатков от каждой группы             
Q_fikt#1934.660

k <-8 #количество регрессоров с константой, т.е.всех коэффициентов в модели
n <-length(M[,1]) # наблюдений 82
F_Chow <-((Q-Q_fikt)/(k+1)) / (Q_fikt/(n-2*(k-1)))
F_Chow # 7.882107

F_crit <- 2.07 #k1=m=8  и k2=n-m-1=82-11=71 по таблице распределения Фишера-Снедекора
F_crit
# F_Chow > F_crit  => следует ввести фиктивные переменные для описания модели,
# т.к. гипотеза об однородности отвергается(нулевая гипотеза)

#Если F > Fкритическое (при выбранном уровне значимости), 
#то основная гипотеза отвергается и нужно оценивать две отдельные регрессии.


#для каждого федерального округа график линейной зависимости Цен на
#молоко от Среднедушевых доходов при зафиксированной средней численности
#населения в федеральном округе. 
plot(x=M$Income, y=M$MilkPrice, main="Зависимость цены от Среднедушевых доходов" ,xlab = "Среднедушевые доходы", ylab = "Цена на молоко")
points(x=M$Income[M$FO=="ЦФО"], y=M$MilkPrice[M$FO=="ЦФО"], col=1)
abline(a=coef(reg4.1)[3]*mean(M$Population[M$FO=="ЦФО"])+coef(reg4.1)[1]+coef(reg4.1)[4], b=coef(reg4.1)[2], col=1)
points(x=M$Income[M$FO=="ЮФО"], y=M$MilkPrice[M$FO=="ЮФО"], col=2)
abline(a=coef(reg4.1)[3]*mean(M$Population[M$FO=="ЮФО"])+coef(reg4.1)[1]+coef(reg4.1)[5], b=coef(reg4.1)[2], col=2)
points(x=M$Income[M$FO=="СЗФО"], y=M$MilkPrice[M$FO=="СЗФО"], col=3)
abline(a=coef(reg4.1)[3]*mean(M$Population[M$FO=="СЗФО"])+coef(reg4.1)[1]+coef(reg4.1)[6], b=coef(reg4.1)[2], col=3)
points(x=M$Income[M$FO=="УФО"], y=M$MilkPrice[M$FO=="УФО"], col=4)
abline(a=coef(reg4.1)[3]*mean(M$Population[M$FO=="УФО"])+coef(reg4.1)[1]+coef(reg4.1)[7], b=coef(reg4.1)[2], col=4)
points(x=M$Income[M$FO=="ПФО"], y=M$MilkPrice[M$FO=="ПФО"], col=5)
abline(a=coef(reg4.1)[3]*mean(M$Population[M$FO=="ПФО"])+coef(reg4.1)[1]+coef(reg4.1)[8], b=coef(reg4.1)[2], col=5)
points(x=M$Income[M$FO=="СКФО"], y=M$MilkPrice[M$FO=="СКФО"], col=6)
abline(a=coef(reg4.1)[3]*mean(M$Population[M$FO=="СКФО"])+coef(reg4.1)[1]+coef(reg4.1)[9], b=coef(reg4.1)[2], col=6)
points(x=M$Income[M$FO=="СФО"], y=M$MilkPrice[M$FO=="СФО"], col=7)
abline(a=coef(reg4.1)[3]*mean(M$Population[M$FO=="СФО"])+coef(reg4.1)[1]+coef(reg4.1)[10], b=coef(reg4.1)[2], col=7)
points(x=M$Income[M$FO=="ДВФО"], y=M$MilkPrice[M$FO=="ДВФО"], col=8)
abline(a=coef(reg4.1)[3]*mean(M$Population[M$FO=="ДВФО"])+coef(reg4.1)[1], b=coef(reg4.1)[2], col=8)
legend(10000,83,legend = c("ЦФО","ЮФО","СЗФО","УФО","ПФО","СКФО","СФО","ДВФО"), col = c(1,2,3,4,5,6,7,8), lwd=1, pch = c(1, 1, 1,1,1,1,1,1))


#21. Проведите эксперимент: Введите в регрессию фиктивную переменную для
#Дальневосточного федерального округа вместо фиктивной переменной для
#центрального федерального округа.

reg5<-lm(M1$MilkPrice ~ M1$Income +M1$Population+ M1$ZDVFO + M1$ZUFO + M1$ZSZFO + M1$ZUrFO + M1$ZPFO + M1$ZSKFO + M1$ZSFO + M1$ZDVFO)
summary(reg5)
library(forecast)
accuracy(reg5)
plot(residuals(reg5))
abline(h=0, col="red")

#22. Проведите эксперимент: Введите в регрессию фиктивную переменную для
#Дальневосточного федерального округа вместо фиктивной переменной для южного
#федерального округа.

reg5.2<-lm(M1$MilkPrice ~ M1$Income +M1$Population + M1$ZCFO + M1$ZDVFO + M1$ZSZFO + M1$ZUrFO + M1$ZPFO + M1$ZSKFO + M1$ZSFO+ M1$ZDVFO)
summary(reg5.2)
accuracy(reg5.2)
plot(residuals(reg5.2))
abline(h=0, col="red")

#23. Постройте множественную регрессию для Цен на молоко, Среднедушевых
#доходов, Численности населения и Федерального округа. При этом, фактор
#Федеральный округ влияет на коэффициент при факторе Среднедушевые доходы.

# наилучшая
reg5.3<-lm(M$MilkPrice ~ M$Income * M$FO + M$Population)
summary(reg5.3)
accuracy(reg5.3)
plot(residuals(reg5.3))
abline(h=0, col="red")

#24. Постройте множественную регрессию для Цен на молоко, Среднедушевых
#доходов, Численности населения и Федерального округа. При этом, фактор
#Федеральный округ влияет на коэффициент при факторе Численность населения.

reg5.4<-lm(M$MilkPrice ~ M$Income + M$Population * M$FO)
summary(reg5.4)
accuracy(reg5.4)
plot(residuals(reg5.4))
abline(h=0, col="red")

#25. Выберите наилучшую модель для описания изменений Цен на молоко.
# Сравниваем MAPE различных моделей
accuracy(reg5)[5]    # 9.573791
accuracy(reg5.2)[5]  # 9.573791
accuracy(reg5.3)[5]  # 8.631434  - наилучшая модель
accuracy(reg5.4)[5]  # 9.009739

# Наименьший показатель MAPE (при количестве наблюдений = 82) 
# среди моделей с фиктивными  переменными у модели, 
# в которой фактор ФО влияет на коэффициент среднедушевого дохода.

