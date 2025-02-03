setwd("C:/Users/regst/Desktop/учёба/Эконометрика/lab6")
M <- read.csv2("Milk09-12.csv", header = FALSE, sep = ";", dec = ",", 
               col.names = c("Month", "Price1", "Price2"), fileEncoding = "WINDOWS-1251")
library(forecast)

plot(M$Price1, main="Цена на молоко", ylab="цена, руб.", xlab="месяц, номер", type="o")
#Временной ряд имеет линейную возрастающую тенденцию

x<-seq(from=1, to=length(M$Price1))
reg1<-lm(M$Price1~x)
abline(reg1)


plot(M$Price2, main="Цена на молоко", ylab="цена, руб.", xlab="месяц, номер", type="o")
#Временной ряд имеет возрастающую нелинейную тенденцию.

reg2<-lm(M$Price2~x)
abline(reg2)


# 1) Построить уравнение нелинейного тренда временного ряда.
M <- read.csv2("Milk09-12.csv", header = FALSE, sep = ";", dec = ",", 
               col.names = c("Month", "Price1", "Price2"), fileEncoding = "WINDOWS-1251")
MM2 = data.frame(y = as.vector(M$Price2), x = seq(1, length(M[,1])))
plot(M$Price2, main="Цена на молоко", ylab="цена, руб.", xlab="месяц, номер", type="o")
# экспоненциальная тенденция
model <- nls(y ~ a * exp(x * b), data=MM2, start=list(a=10, b=0))
model
# Построение уравнения нелинейного тренда (экспоненциальная тенденция)
a <- coef(model)[1]
a # 12.22746
b <- coef(model)[2]
b # 0.03143328
# На графике отображаем нелинейную тенденцию (экспоненциальная тенденция)
curve(a * exp(x * b), add=TRUE, col="blue", lwd=2)

# Построение уравнения нелинейного тренда (квадратичная тенденция)
model2 = nls(y ~ a0*x + a1*x^2 + a2, data = MM2, start=list(a0 = 10, a1 = 0, a2 = 0))
# Построение уравнения нелинейного тренда (экспоненциальная тенденция)
a0 <- coef(model2)[1]
a0 #-0.4940429
a1 <-coef(model2)[2]
a1 #0.02649331 
a2 <- coef(model2)[3]
a2 #20.25144
# нарисовать нелинейную тенденцию 
curve(a0*x + a1*x^2 + a2, add=TRUE, col="red", lwd=2)

summary(model)
plot(residuals(model), main = 'Остатки нелинейной модели (экспонента)')
abline(h=0, col="red")

summary(model2)
plot(residuals(model2), main = 'Остатки нелинейной модели (квадратичная)')
abline(h=0, col="red")

