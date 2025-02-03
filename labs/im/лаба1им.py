#1 пункт
import numpy as np
import scipy.integrate as integrate
from scipy.stats import norm
import math

# Параметры задачи
max_claim = 90000 # Максимальная страховая выплата
num_clients = 100 # Количество клиентов
reserve = 5700000 # Резерв компании

# Функция плотности распределения
def claim_density(x, max_claim):
    A = 20 / (max_claim**5)
    return A * x**3 * (max_claim - x)

# Метод Неймана для генерации выборки
def sample_claims(max_claim, num_samples):
    claims = []
    while len(claims) < num_samples:
        x = np.random.uniform(0, max_claim) # x1 от 0 до K
        max_density = np.max(claim_density(np.linspace(0, max_claim, 10000), max_claim)) # M
        y = np.random.uniform(0, max_density) # x2
        if y < claim_density(x, max_claim): #x2 < f(x1)
            claims.append(x)
    return np.array(claims)

# Метод Монте-Карло для оценки вероятности разорения
def simulate_bankruptcy(num_clients, max_claim, reserve, num_simulations=1000):
    bankruptcies = 0
    for _ in range(num_simulations):
        claims = sample_claims(max_claim, num_clients) # Метод Неймана
        total_claims = np.sum(claims) # суммирование выборочных значений
        if total_claims > reserve: # сумма всех выплат > резерва
            bankruptcies += 1
    return bankruptcies / num_simulations # доля случаев банкротства

# Аппроксимация на основе центральной предельной теоремы
def approximate_bankruptcy_probability(num_clients, max_claim, reserve):
    # теор значение мат ожидания
    mean, error = integrate.quad(lambda x: x * claim_density(x, max_claim), 0, max_claim)
    # подсчёт дисперсии
    variance, error = integrate.quad(lambda x: (x - mean)**2 * claim_density(x, max_claim), 0, max_claim)
    std_dev = np.sqrt(variance)
    z = (reserve - mean * num_clients) / (np.sqrt(num_clients) * std_dev)
    return 1 - 0.5 * (1 + math.erf(z / np.sqrt(2)))

# Вызов функций для получения результатов
mc_result = simulate_bankruptcy(num_clients, max_claim, reserve)
clt_result = approximate_bankruptcy_probability(num_clients, max_claim, reserve)

print("Вероятность разорения (Монте-Карло):", mc_result)
print("Вероятность разорения (Центральная предельная теорема):", clt_result)