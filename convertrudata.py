import csv

# Устанавливаем новый предел для поля
csv.field_size_limit(1000000)  # Например, 1 МБ (1000000 байт)

# Пути к файлам
input_file_path = 'opendata.csv'   # Исходный файл
output_file_path = 'convert_opendata.csv'  # Финальный результат
errors_file_path = 'errors_opendata.csv'  # Файл для ошибок

# Функция для преобразования из DMS в десятичные градусы
def dms_to_decimal(degrees, minutes, seconds):
    return float(degrees) + float(minutes)/60 + float(seconds)/3600

# Открываем исходный CSV файл для чтения и записи
with open(input_file_path, 'r', encoding='utf-8') as infile, \
     open(output_file_path, 'w', encoding='utf-8', newline='') as outfile, \
     open(errors_file_path, 'w', encoding='utf-8', newline='') as errorfile:

    reader = csv.reader(infile, delimiter=';')
    writer = csv.writer(outfile, delimiter=';')
    error_writer = csv.writer(errorfile, delimiter=';')

    # Читаем и записываем заголовок
    header = next(reader)
    writer.writerow(header)
    error_writer.writerow(header)  # Записываем заголовок в файл ошибок

    # Обработка строк
    for row in reader:
        try:
            # Проверяем, что строка содержит нужное количество столбцов
            if len(row) > 8:
                coordinates = row[8]  # 9-й столбец (индекс 8)

                # Операции из первого скрипта
                # Шаг 1: Удаляем всё до "Д(гр,мин,сек)"
                if "Д(гр,мин,сек)" in coordinates:
                    coordinates = coordinates.split("Д(гр,мин,сек)", 1)[-1]

                # Шаг 2: Удаляем всё после "Исключаемая область" или "Верхняя граница"
                if "Исключаемая область" in coordinates:
                    coordinates = coordinates.split("Исключаемая область", 1)[0]
                elif "Верхняя граница" in coordinates:
                    coordinates = coordinates.split("Верхняя граница", 1)[0]

                # Шаг 3: Удаляем лишние пробелы
                coordinates = ' '.join(coordinates.split())

                # Шаг 4: Удаляем каждое третье "выражение"
                expressions = coordinates.split()
                cleaned_expressions = [exp for i, exp in enumerate(expressions, start=1) if i % 3 != 1]

                # Шаг 5: Заменяем °, ', " на пробелы и удаляем N, Е
                final_expressions = []
                for exp in cleaned_expressions:
                    for char in ['°', "'", '"']:
                        exp = exp.replace(char, ' ')  # Заменяем на пробел
                    exp = exp.replace('N', '').replace('Е', '').replace('E', '')  # Удаляем N и Е
                    final_expressions.append(exp)

                # Объединённые выражения
                coordinates = ' '.join(final_expressions)

                # Операции из второго скрипта
                # Шаг 6: Разделяем координаты на части (градусы, минуты, секунды)
                coords = coordinates.split()

                # Шаг 7: Переводим пары (широта и долгота) в десятичные градусы
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

        except (ValueError, IndexError) as e:
            # Записываем ошибочную строку в файл ошибок
            error_writer.writerow(row)
            continue  # Пропускаем ошибочную строку и продолжаем обработку

print(f"Файл с обработанными и преобразованными координатами сохранён как {output_file_path}")
print(f"Ошибочные строки сохранены в {errors_file_path}")
