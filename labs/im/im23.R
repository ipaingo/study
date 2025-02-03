# pass_count: Счетчик пройденных фотонов.
# reflect_count: Счетчик отраженных фотонов.
# absorbed_energy: Матрица для хранения поглощенной энергии.

# Установка начальных параметров
wavelength <- 337 # Длина волны в нм
N <- 10000 # Количество фотонов
W_threshold <- 0.0001 # Пороговое значение статистического веса
m <- 10 # Количество раз, на которое может уменьшиться статистический вес фотона
l<-0.02 # Глубина слоя неоднородности

# Начальный индекс слоя
layer_index <- 1
sum <- 0
# Оптические параметры модели кожи из таблицы
layers <- data.frame(
  layer = c("Эпидермис", "Папиллярная дерма", "Поверхностное сосудистое сплетение", 
            "Ретикулярная дерма", "Глубокое сосудистое сплетение", "Неоднородность"),
  mu_a = c(32, 23, 40, 23, 46, 51), # Коэффициент поглощения в см^-1
  mu_s = c(165, 227, 246, 227, 253, 186), # Коэффициент рассеяния в см^-1
  g = c(0.72, 0.72, 0.72, 0.72, 0.72, 0.8), # Фактор анизотропии
  d = c(0.01, 0.02, 0.02, 0.09, 0.06, NA) # Толщина слоя в см (неоднородность не имеет толщины)
)



# Генерация случайных координат для неоднородности
generate_heterogeneity_coordinates <- function() {
  #сумма слоев 0.2
  # Вычисляем оставшуюся длину после l
  remaining_length <- 0.2 - l
  
  # Ограничиваем максимальный радиус так, чтобы не выйти за границы слоев
  max_radius <- min(remaining_length / 2, 0.1)
  
  # Минимальный радиус принимаем равным 0.001, чтобы не выйти за границы слоев
  min_radius <- 0.001
  
  # Генерация случайного радиуса для неоднородности
  heterogeneity_radius <- runif(1, min_radius, max_radius)
  
  # Генерация случайных координат для неоднородности
  heterogeneity_x <- 0
  heterogeneity_y <- 0
  heterogeneity_z <- l
  
  return(c(heterogeneity_x, heterogeneity_y, heterogeneity_z, heterogeneity_radius))
}

# Генерируем координаты неоднородности, радуис
heterogeneity_info <- generate_heterogeneity_coordinates()
heterogeneity_coordinates <- heterogeneity_info[1:3]
heterogeneity_radius <- heterogeneity_info[4]
heterogeneity_radius <- 0.01
# Заменяем NA в последнем столбце d на сгенерированный диаметр
layers$d[6] <- heterogeneity_radius*2

# Функция для моделирования траектории движения фотонов и расчета поглощенной энергии в плоскости xz
simulate_photon_path <- function(layers, wavelength, N, W_threshold, m, heterogeneity_coordinates) {
  pass_count <- 0 # Счетчик пройденных фотонов
  reflect_count <- 0 # Счетчик отраженных фотонов
  absorbed_energy <- matrix(0, nrow = 100, ncol = 100) # Матрица для хранения поглощенной энергии
  photon_trajectories <- list() # Список для хранения траекторий фотонов
  
  for (i in 1:N) {
    W <- 1 # Изначальный статистический вес фотона
    absorbed <- FALSE # Переменная для отслеживания поглощения фотона
    
    # Начальное положение фотона
    x <- 0
    y <- 0
    z <- 0
    
    trajectory <- matrix(NA, nrow = 1000, ncol = 3) # Матрица для хранения траектории текущего фотона
    trajectory_row <- 1 # Индекс строки в матрице траектории
    
    while (W > W_threshold) {
      # Проверяем, попал ли фотон в область неоднородности
      if (sqrt((x - heterogeneity_coordinates[1])^2 + (y - heterogeneity_coordinates[2])^2 + (z - heterogeneity_coordinates[3])^2) <= heterogeneity_radius) {
        layer <- nrow(layers) # Устанавливаем слой неоднородности
      } else {
        layer <- layer_index
        layer_index <- layer_index + 1
        if (layer_index > nrow(layers)) {
          layer_index <- 1
        }
      }
      
      # Рассчитываем вероятность поглощения
      Pa <- layers$mu_a[layer] / (layers$mu_a[layer] + layers$mu_s[layer])
      
      # Уменьшаем вес
      delta_W <- W * Pa
      W <- W - delta_W
      
      # Если вес стал меньше порогового значения, фотон может быть поглощен или продолжить движение
      if (W <= W_threshold) {
        
        # Генерируем случайное число для определения судьбы фотона (поглощение или продолжение движения)
        # Происходит деление на 2 см по x и z, каждый пиксель - 0.02 см
        # x ~ [-1;=1], z ~ [0;2]
        if (runif(1) < 1/m) {
          absorbed <- TRUE
          x_pixel_index <- as.integer((x + 1) / 2 * ncol(absorbed_energy)) 
          z_pixel_index <- as.integer(z / 2 * nrow(absorbed_energy)) 
          
          # Проверяем, что индексы находятся в пределах границ матрицы
          if (x_pixel_index >= 1 && x_pixel_index <= ncol(absorbed_energy) && 
              z_pixel_index >= 1 && z_pixel_index <= nrow(absorbed_energy)) { 
            # Увеличиваем поглощенную энергию в соответствующей ячейке матрицы
            absorbed_energy[z_pixel_index, x_pixel_index] <- absorbed_energy[z_pixel_index, x_pixel_index] + (wavelength * W) / layers$d[layer]
          }
          break
        } 
        else {
          W <- W*m # Если фотон не поглощается 
        }
      }
      
      # Генерируем новое направление движения 
      
      phi <- 2 * pi * runif(1) # Генерируем азимутальный угол phi в диапазоне [0, 2*pi]
      
      # Выбираем новый cos(theta) в соответствии с распределением
      cos_theta_new <- (1 + layers$g[layer]^2 -  ((1 - layers$g[layer]^2) / (1 - layers$g[layer] + 2 * layers$g[layer] * runif(1)))^2) / (2 * layers$g[layer])
      
      # Пересчитываем новые углы
      theta_new <- acos(cos_theta_new)
      phi_new <- phi
      
      # Определение компонентов исходного направляющего вектора V
      Vx <- 0
      Vy <- 0
      Vz <- 1
      
      # Направляющий вектор после рассеяния V'
      # Рассчитываем новые компоненты направляющего вектора
      Vx_next <- Vx
      Vy_next <- Vy
      Vz_next <- Vz
      
      # Рассчитываем новые компоненты направляющего вектора
      if (abs(Vz_next) != 1) {
        # Если |Vz_next| != 1
        V_prime_x <- Vx_next * cos(theta_new) + (sin(theta_new) / sqrt(1 - Vz_next^2)) * (Vx_next * Vz_next * cos(phi_new) - Vy_next * sin(phi_new))
        V_prime_y <- Vy_next * cos(theta_new) + (sin(theta_new) / sqrt(1 - Vz_next^2)) * (Vy_next * Vz_next * cos(phi_new) + Vx_next * sin(phi_new))
        V_prime_z <- Vz_next * cos(theta_new) - sin(theta_new) * cos(phi_new) * sqrt(1 - Vz_next^2)
      } else {
        # Если |Vz_next| = 1
        V_prime_x <- sin(theta_new) * cos(phi_new)
        V_prime_y <- sin(theta_new) * sin(phi_new)
        V_prime_z <- sign(Vz_next) * cos(theta_new)
      }
      
      # Обновляем значения направляющего вектора на следующем шаге
      Vx <- V_prime_x
      Vy <- V_prime_y
      Vz <- V_prime_z
      
      # Фактическое перемещение фотона с использованием нового направляющего вектора V'
      # step_length = t - поглощение фотона на луче
      step_length <- -log(runif(1)) / (layers$mu_a[layer] + layers$mu_s[layer])
      x <- x + step_length * V_prime_x
      y <- y + step_length * V_prime_y
      z <- z + step_length * V_prime_z
      
      # Сохраняем координаты фотона для построения траектории
      if (trajectory_row > nrow(trajectory)) {
        trajectory <- rbind(trajectory, matrix(NA, nrow = 1000, ncol = 3))
      }
      trajectory[trajectory_row, ] <- c(x, y, z)
      trajectory_row <- trajectory_row + 1
      
      # Проверяем, вышел ли фотон за границу ткани, в этом случае считаем его отраженным
      if (z <= 0) {
        reflect_count <- reflect_count + 1
        break
      }
    }
    
    # Учитываем поглощение
    if (absorbed) {
      pass_count <- pass_count + 1
    }
    
    # Добавляем траекторию фотона в список
    photon_trajectories[[i]] <- trajectory[1:(trajectory_row - 1), ]
  }
  
  # Вычисляем коэффициенты пропускания и отражения
  transmission <- pass_count / N
  reflection <- reflect_count / N
  
  # Нормализуем распределение поглощенной энергии
  absorbed_energy_distribution <- absorbed_energy / sum(absorbed_energy)
  return(list(transmission = transmission, reflection = reflection, absorbed_energy_distribution = absorbed_energy_distribution, photon_trajectories = photon_trajectories))
}


# Моделируем траектории фотонов и вычисляем характеристики
results <- simulate_photon_path(layers, wavelength, N, W_threshold, m, heterogeneity_coordinates)



library(plotly)

###################
# Создаем пустой график
plot <- plot_ly()

# Добавляем точку начальной позиции
plot <- add_markers(plot, x = ~0, y = ~0, z = ~0, color = I("red"), symbol = I(20), name = "Начальная позиция")

# Добавляем траектории фотонов
for (i in 1:10) {
  trajectory <- results$photon_trajectories[[i]]
  # Если траектория не пустая, добавляем ее к графику
  if (!is.null(trajectory)) {
    # Добавляем начальную точку траектории (0, 0, 0)
    trajectory <- rbind(c(0, 0, 0), trajectory)
    # Строим линии между всеми точками траектории
    for (j in 1:(nrow(trajectory) - 1)) {
      plot <- add_trace(plot, type = 'scatter3d', mode = 'lines', x = c(trajectory[j, 1], trajectory[j + 1, 1]), 
                        y = c(trajectory[j, 2], trajectory[j + 1, 2]), z = c(trajectory[j, 3], trajectory[j + 1, 3]), 
                        name = paste("Траектория", i), color = I("blue"), showlegend = i == 1)
    }
  }
}

# Устанавливаем заголовок и метки осей
plot <- layout(plot, title = "Траектории фотонов", scene = list(xaxis = list(title = "X"), yaxis = list(title = "Y"), zaxis = list(title = "Z")))

# Отображаем график
plot

# Создаем пустой график
plot_absorbed_energy <- plot_ly()

# Добавляем тепловую карту с распределением поглощенной энергии
plot_absorbed_energy <- add_heatmap(plot_absorbed_energy, z = ~results$absorbed_energy_distribution, 
                                    colors = colorRamp(c("blue", "yellow", "red")), 
                                    x = 1:100, y = 1:100)

# Устанавливаем заголовок и метки осей
plot_absorbed_energy <- layout(plot_absorbed_energy, title = "Распределение поглощенной энергии в плоскости xz", 
                               xaxis = list(title = "X"), yaxis = list(title = "Z"))

# Отображаем график
plot_absorbed_energy

# Выводим результаты
print(paste("Коэффициент пропускания:", results$transmission))
print(paste("Коэффициент отражения:", results$reflection))

