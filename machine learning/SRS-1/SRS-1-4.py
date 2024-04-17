import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

# Шаг 1: Загрузка данных
df = pd.read_csv('Covid19.csv')

# Шаг 2: Подготовка данных
# Кодирование категориальных переменных
label_encoder = LabelEncoder()
df['Weekday'] = label_encoder.fit_transform(df['Weekday'])
df['Country'] = label_encoder.fit_transform(df['Country'])
df['Commodity'] = label_encoder.fit_transform(df['Commodity'])
df['Transport_Mode'] = label_encoder.fit_transform(df['Transport_Mode'])
df['Measure'] = label_encoder.fit_transform(df['Measure'])

# Шаг 3: Разделение данных
X = df[['Year', 'Weekday', 'Country', 'Commodity', 'Transport_Mode', 'Measure', 'Value']]
y = df['Direction']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=19)

# Шаг 4: Обучение модели наивного Байеса
model = GaussianNB()
model.fit(X_train, y_train)

# Шаг 5: Оценка производительности модели
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f'Accuracy: {accuracy}')
print('Classification Report:')
print(classification_report(y_test, y_pred))
