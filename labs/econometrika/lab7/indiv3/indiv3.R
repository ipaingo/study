library(forecast)
setwd("C:/Users/regst/Desktop/учёба/Эконометрика/lab7/indiv3")
#Прочитать данные из файла в таблицу M
M<-readxl::read_excel("8_new.xlsx")

main_ <- 'Количество проданных домов'
xlab_ <- 'Месяц, Начиная с 1976-01'
ylab_ <- 'Количество домов, ед.'

#исследование Количества проданных домов (описывается аддитивной моделью)
plot(M$House, 
     main=main_, 
     ylab=ylab_, 
     xlab=xlab_, 
     type="o", col="blue")# Строим коррелограмму
acf(M$House, type="correlation", plot=TRUE, main="Коррелограмма")
# наличие тренда и сезонных колебаний с периодом 6 месяцев

#Провести сглаживание временного ряда методом скользящего среднего
sn <- ma(M$House, order=12, centre = TRUE) # сгладить временной ряд методом
plot(M$House, 
     main=main_, 
     ylab=ylab_, 
     xlab=xlab_,  
     type="o")
lines(sn, col="green") # нарисовать сглаженный ряд

#Рассчитать сезонную компоненту временного ряда
A<-matrix(data=M$House-sn, nrow = 25) # вычесть из значений временного ряда
SM<-apply(A, 1, function(x) mean(x, na.rm = TRUE))
M.S<-rep(SM,times=5) # записать сезонную составляющую временного ряда

#Рассчитать тренд временного ряда
Tr<-M$House-M.S # удалить сезонную составляющую из временного ряда
T<-seq(from=1, to=125) # сформировать значения t
regM<-lm(Tr~T) # построить линейную регрессию
M.Trend<-coef(regM)[1]+coef(regM)[2]*T # записать тренд для временного ряда

#Рассчитать значения временного ряда по модели
M.fit<-M.Trend+M.S # рассчитать значения временного ряда по модели
plot(M$House, 
     main=main_, 
     ylab=ylab_, 
     xlab=xlab_, 
     type="o") # график
lines(M.fit, col="red") # график модели временного ряда
lines(M.Trend, col="green") # график тренда временного ряда
sum(abs((M$House - M.fit)/M$House))/length(M$House)*100 # рассчитать MAPE
# Относительная ошибка аппроксимации равна 19.82298%

#Построить прогноз
M.F<-array(dim = 25) # создать массив для хранения прогноза
T1<-seq(from=1, to=125+3*25) # создать массив для времени прогноза
M.F<-(coef(regM)[1]+coef(regM)[2]*T1)+SM # рассчитать прогнозные значения
plot(M$House, 
     main=main_, 
     ylab=ylab_, 
     xlab=xlab_, 
     type="o", 
     xlim = c(1,125+12*3), 
     ylim = c(min(M$House), max(M$House))) # график временного ряда
lines(M.fit, col="red",lwd = 2) # график модели временного ряда
lines(x=T1 , y=M.F, col="green") # график прогноза
abline(regM)

#Исследовать остатки
M.Res<-M$House-M.fit # рассчитать остатки
plot(M.Res, type="o", main="Остатки",  ylab=ylab_, xlab=xlab_) # график остатков
#Автокорреляция измеряет степень сходства между временным рядом и его 
#запаздывающей версией в течение последовательных интервалов времени.
acf(M.Res, main="Коррелограмма остатков") # коррелограмма остатков
acf(M.Res, pl= FALSE )
#Автокорреляция при задержке 0 равна 1 .
#Автокорреляция при задержке 1 составляет 0.861 и тд
#По оси X отображается количество задержек, а по оси 
#Y — автокорреляция при этом количестве задержек. 
Box.test(M.Res) # проверить остатки на белый шум

#Box-Pierce test
#data:  M.Res
#X-squared = 92.592, df = 1, p-value < 2.2e-16

