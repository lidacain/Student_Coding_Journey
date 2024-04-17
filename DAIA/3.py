import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# Генерация дат начиная с 2 декабря 2023 года, с шагом в месяц на 60 месяцев вперед
start_date = datetime(2023, 12, 2)
date_range = [start_date + timedelta(days=30 * i) for i in range(60)]  # Генерация 60 дат

# Загрузка данных в DataFrame
data = pd.read_csv('lukoil.csv', delimiter=';', parse_dates=['Date'], dayfirst=True)

# Преобразование числовых значений с запятыми в десятичные числа
numeric_cols = ['Volume', 'Open', 'High', 'Low', 'Close', 'Bid', 'Ask']
data[numeric_cols] = data[numeric_cols].replace(',', '.', regex=True)

# Преобразование значений в числовой тип
data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Создание пустого DataFrame для хранения прогнозов
forecast_data = pd.DataFrame(columns=['Date'] + numeric_cols)

# Добавление дат в первый столбец в формате 'день.месяц.год'
date_strings = [date.strftime('%d.%m.%Y') for date in date_range]
forecast_data['Date'] = date_strings

# Проход по каждому столбцу, выполнение линейной регрессии и сохранение прогнозов
for column in numeric_cols:
    # Создание объекта регрессора
    regressor = LinearRegression()

    # Получение признаков (X) и целевой переменной (y) для регрессии
    X = data.index.values.reshape(-1, 1)  # Используем индексы строк как признаки
    y = data[column].values.reshape(-1, 1)

    # Процесс обучения модели
    regressor.fit(X, y)

    # Прогнозирование значений для графика регрессии на 60 месяцев вперед
    X_forecast = pd.Series(range(len(data), len(data) + 60))
    X_forecast = X_forecast.values.reshape(-1, 1)
    y_pred = regressor.predict(X_forecast)

    # Добавление прогноза в DataFrame
    forecast_data[column] = y_pred.flatten()

# Преобразование прогнозов в числовой тип и суммирование значений по дате
forecast_data[numeric_cols] = forecast_data[numeric_cols].apply(pd.to_numeric, errors='coerce')
forecast_data_summed = forecast_data.groupby('Date')[numeric_cols].sum().reset_index()

# Сохранение прогнозов с суммированными значениями в CSV файл
forecast_data_summed.to_csv('forecasts_summed.csv', index=False, sep=';', date_format='%d.%m.%Y')
