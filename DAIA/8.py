import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from datetime import timedelta

# Загрузка данных в DataFrame
data = pd.read_csv('lukoil.csv', delimiter=';', parse_dates=['Date'], dayfirst=True)

# Преобразование числовых значений с запятыми в десятичные числа
numeric_cols = ['Volume', 'Open', 'High', 'Low', 'Close', 'Bid', 'Ask']
data[numeric_cols] = data[numeric_cols].replace(',', '.', regex=True)

# Преобразование значений в числовой тип
data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Проход по каждому столбцу, выполнение SVM регрессии и вывод результатов
for column in numeric_cols:
    try:
        # Создание объекта SVM регрессора
        regressor = SVR(kernel='linear')  # Используем линейное ядро для простоты

        # Получение признаков (X) и целевой переменной (y) для регрессии
        X = data.index.values.reshape(-1, 1)  # Используем индексы строк как признаки
        y = data[column].values.reshape(-1, 1)

        # Процесс обучения модели
        regressor.fit(X, y)

        # Прогнозирование значений для графика регрессии
        y_pred = regressor.predict(X)

        # Вывод графика
        plt.figure(figsize=(8, 6))
        plt.scatter(data.index, data[column], color='blue', label='Данные')
        plt.plot(data.index, y_pred, color='red', label='SVM регрессия')
        plt.xlabel('Дата')
        plt.ylabel(column)
        plt.title(f'SVM регрессия для столбца {column}')
        plt.legend()
        plt.show()
    except Exception as e:
        print(f"Ошибка при прогнозировании для столбца {column}: {e}")
