import csv
import geopandas as gpd
from shapely.geometry import Polygon

# Устанавливаем новый предел для поля
csv.field_size_limit(1000000)  # Например, 1 МБ (1000000 байт)

# Функция для преобразования строки с координатами в список кортежей (широта, долгота)
def parse_coordinates(coords_str):
    coords = coords_str.split()
    parsed_coords = []
    
    for i in range(0, len(coords), 2):
        lat = float(coords[i+1])  # Широта (второе значение)
        lon = float(coords[i])    # Долгота (первое значение)
        parsed_coords.append((lon, lat))  # Добавляем пару (долгота, широта) для Shapely
    
    return parsed_coords

# Пути к файлам
input_file_path = 'convert_opendata.csv'  # Исходный CSV файл
output_file_path = 'output.gpkg'  # Финальный результат в GPKG

# Список для хранения данных
data = []

# Открываем CSV файл для чтения
with open(input_file_path, 'r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile, delimiter=';')

    # Обработка строк
    for row in reader:
        try:
            # Читаем координаты из 9-го столбца
            coordinates_str = row['Географические координаты угловых точек участка недр, верхняя и нижняя границы участка недр']

            # Преобразуем координаты в десятичные градусы (широта, долгота)
            coordinates = parse_coordinates(coordinates_str)

            # Создаем объект Polygon для Geopandas
            polygon = Polygon(coordinates)
            
            # Добавляем геометрию и свойства в список
            data.append({
                'geometry': polygon,
                **row  # Сохраняем все остальные атрибуты из строки CSV
            })

        except Exception as e:
            print(f"Ошибка обработки строки: {row}\n{e}")
            continue

# Создаем GeoDataFrame из данных
gdf = gpd.GeoDataFrame(data, crs="EPSG:3857")  # Укажите правильную проекцию, например, EPSG:3857 для ГСК-2011

# Сохраняем данные в GPKG
gdf.to_file(output_file_path, layer='data', driver='GPKG')

print(f"GeoPackage файл сохранен как {output_file_path}")
