import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


df = pd.read_csv('serious-injury-outcome-indicators-2000-18-csv.csv')

# Подготовка данных
X = df.drop(['Severity', 'Series_reference', 'Period', 'Data_value', 'Lower_CI', 'Upper_CI'], axis=1)
y = df['Severity']

# Преобразование категориальных признаков в числовые с использованием One-Hot Encoding
X = pd.get_dummies(X)

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=19)

# Обучение модели логистической регрессии
model = LogisticRegression()
model.fit(X_train, y_train)

# Предсказание на тестовой выборке
y_pred = model.predict(X_test)

# Оценка точности модели
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')

# Вывод отчета по классификации
print(classification_report(y_test, y_pred))
