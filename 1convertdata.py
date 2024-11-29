import csv

# Функция для преобразования из DMS в десятичные градусы
def dms_to_decimal(degrees, minutes, seconds):
    return float(degrees) + float(minutes)/60 + float(seconds)/3600

# Пути к файлам
input_file_path = 'test1.csv'  # Исходный файл
output_file_path = 'test2.csv'  # Финальный результат

# Открываем исходный CSV файл для чтения и записи
with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8', newline='') as outfile:
    reader = csv.reader(infile, delimiter=';')
    writer = csv.writer(outfile, delimiter=';')

    # Читаем и записываем заголовок
    header = next(reader)
    writer.writerow(header)

    # Обработка строк
    for row in reader:
        # Проверяем, что строка содержит нужное количество столбцов
        if len(row) > 8:
            coordinates = row[8]  # 9-й столбец (индекс 8)

            # Шаг 1: Разделяем координаты на части (градусы, минуты, секунды)
            coords = coordinates.split()

            # Шаг 2: Переводим пары (широта и долгота) в десятичные градусы
            decimal_coords = []
            for i in range(0, len(coords), 3):
                degrees = coords[i]
                minutes = coords[i+1]
                seconds = coords[i+2]
                decimal = dms_to_decimal(degrees, minutes, seconds)
                decimal_coords.append(str(decimal))

            # Обновляем 9-й столбец с новыми десятичными значениями
            row[8] = ' '.join(decimal_coords)

        # Записываем обработанную строку в новый файл
        writer.writerow(row)

print(f"Файл с преобразованными координатами сохранён как {output_file_path}")
