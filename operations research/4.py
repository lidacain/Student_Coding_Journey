import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# Пример данных с координатами и качеством связи
latitude = [51.2, 51.3, 51.4, 51.5]
longitude = [7.1, 7.2, 7.3, 7.4]
signal_quality = [90, 80, 95, 70]

# Создание карты
fig = plt.figure(figsize=(10, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

# Добавление фона карты
ax.stock_img()

# Преобразование координат в формат карты
x, y = longitude, latitude

# Построение точек на карте с цветом, отражающим качество связи
sc = ax.scatter(x, y, c=signal_quality, cmap='viridis', s=150, transform=ccrs.PlateCarree(), edgecolors='k', linewidth=1)

# Добавление цветовой шкалы
cbar = plt.colorbar(sc, orientation='vertical')
cbar.set_label('Качество связи')

# Настройка заголовка и добавление аннотаций
plt.title('Расчетное пространственное распределение качества связи')
for i, (lat, lon, quality) in enumerate(zip(latitude, longitude, signal_quality)):
    ax.text(lon, lat, f'{quality}%', transform=ccrs.PlateCarree(), fontsize=10, ha='center', va='bottom')

# Отображение карты
plt.show()
