import pandas as pd
import os

# Ваш код для получения списка файлов
tree = os.walk('data')
data_files = []
target_file = 'data.csv'

for item in tree:
    files = item[-1]
    if len(files) > 0 and target_file in files:
        path = os.path.join(item[0], target_file)
        data_files.append(path)

# Ваш код для чтения данных из файлов
data_files_df = []

for path in data_files:
    df = pd.read_csv(path, index_col=0)
    date, name = path.split('/')[1:3]
    df['name'] = name
    df['date'] = date
    data_files_df.append(df)

# Создание общего DataFrame
combined_df = pd.concat(data_files_df, ignore_index=True)

# Сохранение в CSV
combined_df.to_csv('data.csv', index=False)
