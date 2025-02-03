library("forecast")
setwd("C:/Users/regst/Desktop/учёба/Эконометрика/lab7/indiv1") # установить рабочую папку
T<-readxl::read_excel("ind.xlsx") # прочитать данные из файла и записать в таблицу T

#Проверка наличия корреляции
plot(x=T$Пассажиры, y=T$Машины)
corr <- cor(T$Пассажиры, T$Машины)
print(corr)
T<-T[T$Пассажиры < 10000,]
T<-T[T$Машины < 400,]
plot(x=T$Пассажиры, y=T$Машины)
corr <- cor(T$Машины, T$Пассажиры)
print(corr)
test = cor.test(T$Машины, T$Пассажиры)
print(test)

T<-T[order(T$Машины),] 
regF2F1<-lm(formula=T$Машины ~T$Пассажиры)
summary(regF2F1) 
format(coef(regF2F1), digits =12) 
plot(x=T$Пассажиры, y=T$Машины, main="Диаграмма рассеяния")
abline(regF2F1, col="red") 
mean(regF2F1$residuals)
accuracy(regF2F1) 
T<-T[80,] 

format(predict(regF2F1, newdata=T, interval="confidence", level=0.9), digits=10) 
P<-predict(regF2F1, newdata=T, interval="confidence", level=0.9) 
T<-readxl::read_excel("ind.xlsx") 
T<-T[T$Пассажиры < 10000,]
T<-T[T$Машины < 400,]
T<-T[order(T$Машины),]

plot(x=T$Пассажиры, y=T$Машины, main="Точечный прогноз")
abline(regF2F1) 
points(x=240.7, y=P[1], col="red") 
lines(x=c(240.7,240.7,240.7), y=P, col="red")

########################################################################################################

T<-readxl::read_excel("ind.xlsx") 

T<-T[T$Пассажиры < 10000,]
T<-T[T$Машины < 400,]
T<-T[order(T$Машины),]

regF1F2<-lm(formula=T$Пассажиры ~T$Машины) 
summary(regF1F2) 
format(coef(regF1F2), digits =12)
plot(x=T$Машины, y=T$Пассажиры, main="Диаграмма рассеяния") 
abline(regF1F2, col="red")
mean(regF2F1$residuals)
library("forecast") 
accuracy(regF1F2) 



