import matplotlib.pyplot as plt

# Данные для графиков (замените их своими данными)
x_values = [1, 2, 3, 4, 5]
y_data1 = [10, 20, 15, 30, 25]  # Результаты моделирования
y_data2 = [12, 18, 17, 28, 24]  # Экспериментальные данные

# Создание графика
plt.figure(figsize=(10, 5))

# Построение графиков
plt.plot(x_values, y_data1, marker='o', label='Моделирование', color='blue')
plt.plot(x_values, y_data2, marker='x', label='Эксперимент', color='red')

# Настройка внешнего вида графика
plt.xlabel('Номер измерения или местоположение')
plt.ylabel('Значение параметра')
plt.title('Сравнение результатов моделирования и эксперимента')
plt.legend()
plt.grid(True)

# Отображение графика
plt.show()
