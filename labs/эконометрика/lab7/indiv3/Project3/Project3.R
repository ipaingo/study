setwd("~/Documents/Универ/эконометрика/indiv3/")
library(forecast)

#M<-read.csv2 ("Monthly car sales in Quebec 196.csv", header=TRUE, sep=",", dec = ",")
#View(M)
M<-readxl::read_excel("8_new.xlsx")

plot(M$House, main="Продажи", ylab="кол-во продаж", xlab="месяц", type="o", col="blue")

acf(M$House, type="correlation", plot=TRUE, main="Коррелограмма")

sn <- ma(M$House, order=12, centre = TRUE) # сгладить временной ряд методом скользящего среднего
plot(M$House, main="Доходы", ylab="кол-во", xlab="месяц", type="o")
lines(sn, col="green") # нарисовать сглаженный ряд

A<-matrix(data=M$House-sn, nrow = 12) # вычесть из значений временного ряда сглаженное значение
SM<-apply(A, 1, function(x) mean(x, na.rm = TRUE))
M.S<-rep(SM,times=9) # записать сезонную составляющую временного ряда

Tr<-M$X-M.S # удалить сезонную составляющую из временного ряда
T<-seq(from=1, to=108) # сформировать значения t
regM<-lm(Tr~T) # построить линейную регрессию
M.Trend<-coef(regM)[1]+coef(regM)[2]*T # записать тренд для временного ряда

M.fit<-M.Trend+M.S # рассчитать значения временного ряда по модели
plot(M$X, main="Продажи", ylab="кол-во", xlab="месяц", type="o") # график временного ряда
lines(M.fit, col="red") # график модели временного ряда
lines(M.Trend, col="green") # график тренда временного ряда
sum(abs((M$X - M.fit)/M$X))/length(M$X)*100 # рассчитать MAPE

M.F<-array(dim = 12) # создать массив для хранения прогноза
T1<-seq(from=109, to=108+18) # создать массив для времени прогноза
M.F<-(coef(regM)[1]+coef(regM)[2]*T1)+SM # рассчитать прогнозные значения
plot(M$X, main="Продажи", ylab="Кол-во", xlab="месяц", type="o", xlim = 
       c(1,130), ylim = c(min(M$X), max(M$X))) # график временного ряда
lines(M.fit, col="red") # график модели временного ряда
lines(x=T1 , y=M.F, col="green") # график прогноза
abline(regM)

Mp.Res<-M$X-M.fit # рассчитать остатки
plot(Mp.Res, type="o", main="Остатки", ylab="тыс. человек", xlab="месяц") # график остатков
acf(Mp.Res, main="Коррелограмма остатков") # коррелограмма остатков
Box.test(Mp.Res) # проверить остатки на белый шум



