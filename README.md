#

## om_time_to_datetime

Функция предназначена для конвертацмм серии из системных измерений времени Optimacros в даты формата datetime

```py
om_time_to_datetime(series: pd.Series, start_weekday: str = 'Monday', max_days_in_W0: int = 6)
```

- `series` - серия в формате om_time ('FY22', 'Jan 21', '21 Jan 22' и т.д.), которая будет конвертированна в формат `YYYY-MM-DD`
- `start_weekday` (str, optional): Название перого дня недели. По умолчанию 'Monday'.
- `max_days_in_W0` (int, optional): Количество дней в неполной нулевой неделе, принимает значения от 0 до 6. По умолчанию 6.

## datetime_to_om_time

Функция предназначена для конвертации серии фомата datetime к системным измерениям времени в Optimacros

```py
datetime_to_om_time(series: pd.Series, format: str = 'Months', start_weekday: str = 'Monday', max_days_in_W0: int = 6)
```

- `series` - серия в формате datetime, которая будет коныертированна
- `format` - формат в который будет конвертированна серия
  Допустимые варианты параметра:
  - `Years` -  `2022-01-21` → `FY22`
  - `Months` - `2022-01-21` → `Jan 22`
  - `Days` - `2022-01-21` → `21 Jan 22`
  - `Weeks` - `2022-01-21`, `Monday`, `6` → `W5_22`
- `start_weekday` (str, optional): Название перого дня недели. По умолчанию 'Monday'.
- `max_days_in_w0` (int, optional): _Количество дней в неполной нулевой неделе, принимает значения от 0 до 6. По умолчанию 6.

## dataframes_to_om_csv

Функция для преобразования списка из датафреймов в `csv` файл, готовый для импорта в Optimacros

```py
dataframes_to_om_csv(dfs: list, path: str, colunms: list = None, time_column: str = None, datetime_column: str = 'datetime', time_format: str = 'Months', reset_index: bool = True, encoding: str = 'utf-8', sep: str = ';')
```

- `dfs` - список датафреймов
- `path` - путь сохранения файла
- `columns` - колонки, которые останутся в файле
- `time_column` - название колонки с датами, в которой будут созранены конвертированные даты
- `datetime_column` - название колонки в который хранятся даты в формате datetime
    Не обязательный параметр, по умолчанию имеет значение `datetime`
- `time_format` - формат пробразования `datetime_column` → `time_column`
  - Не обязательный параметр, по умолчанию имеет значение `Months`
- `reset_index` - boolean, при `True` файл будет создан без индексов, иначе в файле будут созданы индексы
  - Не обязательный параметр, по умолчанию имеет значение `True`
- `encoding` - кодировка с которой будет создан файл
  - Не обязательный параметр, по умолчанию имеет значение `utf-8`
- `sep` - разделитель с которым будет создан файл
  - Не обязательный параметр, по умолчанию имеет значение `;`

## csv_to_dataframe

Функция конвертации csv файла выгруженого из Optimacros в DataFrame

```py
csv_to_dataframe(filename: str, sep: str = ";", encoding = "UTF 8")
```

- `filename` - Путь к файлу, для конвертации
- `sep` - Разделитель используемый в файле
  - Не обязательный параметр, по умолчанию имеет значение `;`
- `encoding` - Кодировка файла
  - Не обязательный параметр, по умолчанию имеет значение `UTF 8`

## excel_to_dataframe

Функция конвертации excel файла выгруженого из Optimacros в DataFrame

```py
excel_to_dataframe(filename: str)
```

- `filename` - Путь к файлу, для конвертации

## file_to_dataframe

Функция для конвертации любого файла выгруженного из Optimacros в DataFrame

```py 
file_to_dataframe(file_path: str, file_type: str, sep: str = ";", encoding: str = "UTF 8", columns: list[str] = None, invert_columns: bool = False, index_column: str = None, columns_to_convert: dict = None)
```

- `file_path` - Путь к файлу, для конвертации
- `file_type` - Тип файла, доступные варианты : `csv`, `om_csv`, `txt`, `om_txt`, `xlsx`
- sep - Разделитель используемый в файле, параметр актуалент только для `csv`, `om_csv`, `txt`, `om_txt` файлов
  - Не обязательный параметр, по умолчанию имеет значение `;`
- `encoding` - Кодировка файла, параметр актуалент только для `csv`, `om_csv`, `txt`, `om_txt` файлов
  - Не обязательный параметр, по умолчанию имеет значение `UTF 8`
- `columns` - Колонки когоры будут в итоговом DataFrame
  - Не обязательный параметр, по умолчаную `None`, в таком случае в DataFrame будут все колонки оригинального файла
- `invert_columns` - При значении `True` в DataFrame будут все колонки кроме перечисленных в `columns`
  - Не обязательный параметр, по умолчанию имеет значение `False`
- `index_column` - Название колонки, которая станет индексом в DataFrame
  - Не обязательный параметр, по умолчанию имеет значение `None`, в таком случае индекс проставиться автоматически
- `columns_to_convert` - Словарь форматов и колонок которые нужно в них конвертировать
  Пример:

  ```py
    {
      'boolean': ['column_1'],
      'int': ['column_2', 'column_3']
    }
  ```

## convert_int_om_to_pandas

Функция конвертации Serias в формат `numpy.int64`

```py
convert_int_om_to_pandas(series: pd.Series)
```

- `series` - Колонка DataFrame для конвертации

## convert_float_om_to_pandas

Функция конвертации Serias в формат `numpy.float64`

```py
convert_float_om_to_pandas(series: pd.Series)
```

- `series` - Колонка DataFrame для конвертации

## convert_boolean_om_to_pandas

Функция конвертации Serias в формат `boolean`

```py
convert_boolean_om_to_pandas(series: pd.Series)
```

- `series` - Колонка DataFrame для конвертации

## convert_columns

Функция для конвертации колонок Dataframe

```py
convert_columns(df: pd.DataFrame, columns: list[str], data_type: str)
```

- `df` - DataFrame для конвертации
- `columns` - Список колонок для конвертации
- `data_type` - Тип данных в который конвертируем колонку. Доступные варианты: `int`, `float`, `bool`, `om_date`, `date`
  - `int` - Применяет функцию [convert_int_om_to_pandas](#convert_int_om_to_pandas)
  - `float` - Применяет функцию [convert_float_om_to_pandas](#convert_float_om_to_pandas)
  - `bool` - Применяет функцию [convert_boolean_om_to_pandas](#convert_boolean_om_to_pandas)
  - `om_date` - Применяет функцию [om_time_to_datetime](#om_time_to_datetime)
  - `date` - Применяет функцию [convert_boolean_om_to_pandas](#datetime_to_om_time)

## dataframe_to_list

Функция разбивющая DataFrame на список DataFrame по группам с уникальными значениями в перечисленных колонках

```py
dataframe_to_list(df: pd.DataFrame, columns: list[str], invert_columns: bool = False)
```

- `df` - DataFrame для разбиения
- `columns` - Список колонок по которому определяются группы
- `invert_columns` -  При значении `True` для гурппировки будут использоваться все колонки кроме перечисленных в `columns`
  - Не обязательный параметр, по умолчанию имеет значение `False`
