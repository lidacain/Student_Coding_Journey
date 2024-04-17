import random
import matplotlib.pyplot as plt

# Исходные данные
max_iterations = 1000
adaptive_coefficient = 0.1

# Пустые списки для хранения данных для графика
downlink_history, uplink_history = [], []

# Функции для расчета мощности прямого и обратного канала
def calculate_power(is_downlink):
    # Ваш код для расчета мощности в зависимости от типа канала
    return random.uniform(0, 50) if is_downlink else random.uniform(0, 30)

# Основной цикл
for n in range(max_iterations):
    downlink_power = calculate_power(True)
    uplink_power = calculate_power(False) 

    downlink_history.append(downlink_power)
    uplink_history.append(uplink_power)

    adaptive_coefficient += 0.01

# Создание графика
plt.figure(figsize=(10, 5))
plt.plot(range(1, max_iterations+1), downlink_history, label='Прямой канал')
plt.plot(range(1, max_iterations+1), uplink_history, label='Обратный канал')
plt.xlabel('Итерация')
plt.ylabel('Мощность dBM')
plt.title('Мощность прямого и обратного канала с течением времени')
plt.legend()
plt.grid(True)
plt.show()
