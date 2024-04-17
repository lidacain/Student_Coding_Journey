import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report


df = pd.read_csv('titanic.csv')

# Предобработка данных
# Заполнение пропущенных значений в столбце 'age' средним значением
df['age'].fillna(df['age'].mean(), inplace=True)

# Преобразование категориальных признаков в числовые с использованием One-Hot Encoding
df = pd.get_dummies(df, columns=['sex', 'embarked', 'class', 'who', 'adult_male', 'deck', 'embark_town', 'alive', 'alone'], drop_first=True)

# Разделение на признаки (X) и целевую переменную (y)
X = df.drop('survived', axis=1)
y = df['survived']

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=19)

# Обучение модели дерева решений
model = DecisionTreeClassifier(random_state=19)
model.fit(X_train, y_train)

# Предсказание на тестовой выборке
y_pred = model.predict(X_test)

# Оценка точности модели
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')

# Вывод отчета по классификации
print(classification_report(y_test, y_pred))
