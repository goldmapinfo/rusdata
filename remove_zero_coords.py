import geojson

# Путь к исходному и выходному файлу (один и тот же)
file_path = '/home/alvarets/dev/RusData/output.geojson'

# Загружаем исходный файл GeoJSON
with open(file_path, 'r', encoding='utf-8') as f:
    data = geojson.load(f)

# Обрабатываем объекты в GeoJSON
updated_features = []

for feature in data['features']:
    geometry = feature['geometry']
    
    # Проверяем, если это полигон (или MultiPolygon)
    if geometry['type'] == 'Polygon':
        # Фильтруем координаты
        geometry['coordinates'] = [
            [coord for coord in ring if coord != [0.0, 0.0]] for ring in geometry['coordinates']
        ]
        if geometry['coordinates']:  # Если координаты не пустые, добавляем объект
            updated_features.append(feature)
    elif geometry['type'] == 'MultiPolygon':
        # Фильтруем для MultiPolygon
        geometry['coordinates'] = [
            [[coord for coord in ring if coord != [0.0, 0.0]] for ring in polygon] 
            for polygon in geometry['coordinates']
        ]
        if geometry['coordinates']:  # Если координаты не пустые, добавляем объект
            updated_features.append(feature)

# Обновляем данные в GeoJSON
data['features'] = updated_features

# Перезаписываем исходный файл
with open(file_path, 'w', encoding='utf-8') as f:
    geojson.dump(data, f, indent=2)

print(f"Файл успешно перезаписан: {file_path}")
