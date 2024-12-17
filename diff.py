import pandas as pd
from datetime import date

# Чтение данных из CSV-файлов
previous_df = pd.read_csv(
    'PreviousData.csv',
    sep=';',
    quoting=3,           # Игнорирует кавычки, чтобы избежать ошибок
    on_bad_lines='skip', # Пропускает проблемные строки
    engine='python'      # Использует более гибкий парсер
)
current_df = pd.read_csv(
    'opendata.csv',
    sep=';',
    quoting=3,           # Игнорирует кавычки, чтобы избежать ошибок
    on_bad_lines='skip', # Пропускает проблемные строки
    engine='python'      # Использует более гибкий парсер
    )

# Получаем текущую дату
today = date.today().strftime('%Y-%m-%d')
output_file_name = f'change_{today}.csv'

# Проверяем наличие одинаковых столбцов в обоих файлах
if not set(previous_df.columns) == set(current_df.columns):
    raise ValueError("Файлы имеют разные наборы столбцов.")

# Объединяем DataFrame'ы с помощью merge() и находим различия
merged_df = pd.merge(
    left=previous_df,
    right=current_df,
    how='outer',
    indicator=True
)

# Фильтруем строки, которые отличаются или присутствуют только в одном из файлов
changes_df = merged_df.query("_merge != 'both'")

# Сохраняем результат в новый CSV-файл
changes_df.to_csv(output_file_name, index=False)
print(f"Различия сохранены в файл {output_file_name}")
