library(dplyr)
library(ggplot2)
library(lubridate)

dados <- read.csv("./steam_raspagem.csv")

dados$Price <- as.numeric(gsub("R\\$ ", "", gsub(",", ".", dados$Price)))
dados$Discount <- as.numeric(sub("%", "", dados$Discount)) / 100
dados$Rating <- as.numeric(sub("%", "", dados$Rating)) / 100

dados$Release <- dmy(paste("01", dados$Release))

summary(dados)


ggplot(dados, aes(x = Price)) + 
  geom_histogram(bins = 30, fill = "blue", alpha = 0.7) +
  labs(title = "Histograma de Preços", x = "Preço (R$)", y = "Frequência")

ggplot(dados, aes(x = Discount)) + 
  geom_histogram(bins = 30, fill = "green", alpha = 0.7) +
  labs(title = "Histograma de Descontos", x = "Desconto", y = "Frequência")

ggplot(dados, aes(x = Rating)) + 
  geom_histogram(bins = 30, fill = "red", alpha = 0.7) +
  labs(title = "Histograma de Avaliações", x = "Avaliação", y = "Frequência")


