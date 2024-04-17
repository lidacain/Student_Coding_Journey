import numpy as np
import matplotlib.pyplot as plt

# Заданный диапазон для переменной x
x_min = -84.7
x_max = -58.6

# Количество выборок
num_samples = 1000

# Количество значений в каждой выборке
sample_size = 50

# Генерация и расчет MSE
mse_values = []

for _ in range(num_samples):
    # Генерация случайных значений x в заданном диапазоне
    true_values = np.random.uniform(x_min, x_max, sample_size)  # Истинные значения (случайные)
    random_samples = np.random.uniform(x_min, x_max, sample_size)  # Случайные выборки

    # Расчет MSE для каждой выборки
    mse = np.mean((random_samples - true_values) ** 2)
    mse_values.append(mse)

# Построение точечного распределения MSE
plt.figure(figsize=(10, 5))
plt.scatter(range(num_samples), mse_values, color='blue', s=5)
plt.xlabel('Номер выборки')
plt.ylabel('Среднеквадратическая ошибка (MSE)')
plt.title('Распределение MSE для 1000 случайных выборок')
plt.grid(True)

# Отображение графика
plt.show()