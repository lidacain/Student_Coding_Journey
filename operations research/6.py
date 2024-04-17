import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import geopandas as gpd
import pandas as pd
import numpy as np

# Генерация примерных данных
np.random.seed(0)
n_points = 50
data = {'latitude': np.random.uniform(-90, 90, n_points),
        'longitude': np.random.uniform(-180, 180, n_points),
        'signal_level_dbmW': np.random.uniform(-90, -40, n_points),
        'signal_to_noise_db': np.random.uniform(-15, 20, n_points),
        'transmitter_power_dbmW': np.random.uniform(-40, 10, n_points)}

# Создание GeoDataFrame из данных
df = pd.DataFrame(data)
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

# Создание карты
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})

# Добавление фона мировой карты
ax.stock_img()

# Отображение точек на карте с учетом разных условий (Хорошая связь, Помехи в прямом канале, Помехи в обратном канале)
for condition in ['Хорошая связь', 'Помехи в прямом канале', 'Помехи в обратном канале']:
    condition_gdf = gdf[(gdf['signal_level_dbmW'] >= -90) & (gdf['signal_level_dbmW'] <= -40) &
                        (gdf['signal_to_noise_db'] >= -15) & (gdf['signal_to_noise_db'] <= 20) &
                        (gdf['transmitter_power_dbmW'] >= -40) & (gdf['transmitter_power_dbmW'] <= 10)]

    sc = ax.scatter(condition_gdf['longitude'], condition_gdf['latitude'], label=condition,
                    transform=ccrs.PlateCarree())

# Настройка легенды
ax.legend()

# Настройка заголовка
plt.title('Пространственное распределение условий связи')

# Отображение карты
plt.show()
