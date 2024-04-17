import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import timedelta

# Загрузка данных в DataFrame
data = pd.read_csv('lukoil.csv', delimiter=';', parse_dates=['Date'], dayfirst=True)

# Преобразование числовых значений с запятыми в десятичные числа
numeric_cols = ['Volume', 'Open', 'High', 'Low', 'Close', 'Bid', 'Ask']
data[numeric_cols] = data[numeric_cols].replace(',', '.', regex=True)

# Преобразование значений в числовой тип
data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Создание прогнозов для каждого столбца
forecast_period = 60  # Прогноз на 60 месяцев

plt.figure(figsize=(12, 8))

for col in numeric_cols:
    try:
        model = SARIMAX(data[col], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))  # Пример параметров модели
        fitted = model.fit()

        # Прогноз на 60 месяцев вперед
        forecast = fitted.forecast(steps=forecast_period)

        # Построение прогноза для каждого столбца на одном графике
        plt.plot(pd.date_range(start=data['Date'].max() + timedelta(days=1), periods=forecast_period, freq='M'), forecast, label=col)
    except Exception as e:
        print(f"Ошибка при прогнозировании для столбца {col}: {e}")

plt.xlabel('Дата')
plt.ylabel('Значение')
plt.title('Прогнозы по разным столбцам')
plt.legend()
plt.tight_layout()
plt.show()
