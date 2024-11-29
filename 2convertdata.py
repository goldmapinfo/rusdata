import csv
import geojson

# Функция для преобразования строки с координатами в список кортежей (широта, долгота)
def parse_coordinates(coords_str):
    coords = coords_str.split()
    return [(float(coords[i+1]), float(coords[i])) for i in range(0, len(coords), 2)]

# Пути к файлам
input_file_path = 'test2.csv'  # Исходный CSV файл
output_file_path = 'output.geojson'  # Финальный результат в GeoJSON

# Список для хранения данных
features = []

# Открываем CSV файл для чтения
with open(input_file_path, 'r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile, delimiter=';')

    # Обработка строк
    for row in reader:
        # Читаем координаты из 9-го столбца
        coordinates_str = row['Географические координаты угловых точек участка недр, верхняя и нижняя границы участка недр']

        # Преобразуем координаты в десятичные градусы (широта, долгота)
        coordinates = parse_coordinates(coordinates_str)

        # Создаем GeoJSON объект для полигона
        polygon = geojson.Polygon([coordinates])
        
        # Добавляем к списку
        feature = geojson.Feature(geometry=polygon, properties=row)
        features.append(feature)

# Создаем объект GeoJSON с указанием проекции ГСК-2011
geojson_data = geojson.FeatureCollection(features)

# Добавляем информацию о проекции (ГСК-2011)
geojson_data["crs"] = {
    "type": "name",
    "properties": {
        "name": "urn:ogc:def:crs:OGC:1.3:CRS84"  # Этот код будет соответствовать ГСК-2011, измените его при необходимости
    }
}

# Записываем результат в файл .geojson
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    geojson.dump(geojson_data, outfile, ensure_ascii=False, indent=4)

print(f"GeoJSON файл сохранен как {output_file_path}")
