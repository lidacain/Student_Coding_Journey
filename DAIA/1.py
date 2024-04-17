import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Загрузка данных в DataFrame
data = pd.read_csv('lukoil.csv', delimiter=';', parse_dates=['Date'], dayfirst=True)

# Преобразование числовых значений с запятыми в десятичные числа
numeric_cols = ['Volume', 'Open', 'High', 'Low', 'Close', 'Bid', 'Ask']
data[numeric_cols] = data[numeric_cols].replace(',', '.', regex=True)

# Преобразование значений в числовой тип
data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Создание общего графика для всех столбцов
fig, ax = plt.subplots(figsize=(25, 16))

# Проход по каждому столбцу, выполнение линейной регрессии и вывод результатов на общем графике
for column in numeric_cols:
    # Создание объекта регрессора
    regressor = LinearRegression()

    # Получение признаков (X) и целевой переменной (y) для регрессии
    X = data.index.values.reshape(-1, 1)  # Используем индексы строк как признаки
    y = data[column].values.reshape(-1, 1)

    # Процесс обучения модели
    regressor.fit(X, y)

    # Прогнозирование значений для графика регрессии
    y_pred = regressor.predict(X)

    # Вывод линейной регрессии на общем графике
    ax.scatter(data.index, data[column], label=column)
    ax.plot(data.index, y_pred, label=f'{column}_LinearRegression')

# Получение месяцев для меток на оси X (Дата)
months = data['Date'].dt.month
formatted_dates = [f'{m}' for m in months]

# Настройка меток дат для оси X (Дата) с уменьшенным размером шрифта
ax.set_xticks(data.index)
ax.set_xticklabels(formatted_dates, rotation=45, ha='right', fontsize=8)

# Настройка отображения
plt.xlabel('Дата')
plt.ylabel('Значение')
plt.title('Линейная регрессия для всех столбцов')
plt.legend()
plt.tight_layout()
plt.show()
