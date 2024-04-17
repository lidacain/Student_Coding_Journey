import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import geopandas as gpd
import pandas as pd
import numpy as np

# Генерация случайных данных для координат и качества связи
np.random.seed(0)
n_points = 50
data = {'latitude': np.random.uniform(-90, 90, n_points),
        'longitude': np.random.uniform(-180, 180, n_points),
        'signal_quality': np.random.uniform(0, 100, n_points)}

# Создание GeoDataFrame из данных
df = pd.DataFrame(data)
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

# Создание карты
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})

# Добавление фона мировой карты
ax.stock_img()

# Отображение точек на карте с цветом, отражающим качество связи
sc = ax.scatter(gdf['longitude'], gdf['latitude'], c=gdf['signal_quality'], cmap='coolwarm', transform=ccrs.PlateCarree())
plt.colorbar(sc, label='Качество сигнала')

# Настройка заголовка
plt.title('Карта')

# Отображение карты
plt.show()
