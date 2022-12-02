import pandas as pd
import numpy as np
from typing import NoReturn
import datetime


def om_time_to_datetime(series: pd.Series, start_weekday: str = 'Monday', max_days_in_W0: int = 6) -> pd.Series:
    """Функция для конвертации дат формата ОМ в datetime.

    Args:
        series (pd.Series): Серия с датой в формате OM.
        start_weekday (str, optional): Название перого дня недели. По умолчанию 'Monday'.
        max_days_in_W0 (int, optional): Количество дней в неполной нулевой неделе, принимает значения от 0 до 6. По умолчанию 6.
    """
    date_example = series.iloc[0]

    if len(date_example) == 4:
        # only year
        return pd.to_datetime(series.str.lstrip('FY'), format='%y')
    elif len(date_example) == 6:
        # month and year
        return pd.to_datetime(series, format='%b %y')
    elif date_example[0] == "W":
        # week and year
        if max_days_in_W0 > 6:
            raise ValueError(f"Argument max_days_in_W0 can`t be more 6. Your value is {max_days_in_W0}.")
        weekday_mapping = {'Monday': 1,
                        'Tuesday': 2,
                        'Wednesday': 3,
                        'Thursday': 4,
                        'Friday': 5,
                        'Saturday': 6,
                        'Sunday': 0}
        df_convert_week = pd.DataFrame()
        df_convert_week['om_week'] = series
        df_convert_week['Year'] = df_convert_week['om_week'].apply(lambda x: x[-2:])
        
        # Определение коичества дней в нелоных неделях по годам
        first_weeks = pd.DataFrame()
        first_weeks['date'] = pd.Series([datetime.datetime.strptime(f"{day} {year}", "%d %y") for year in df_convert_week['Year'].unique() for day in range(1,8)])
        first_weeks['om_week'] = datetime_to_om_time(first_weeks['date'], "Weeks", start_weekday, max_days_in_W0)
        first_weeks['Year'] = first_weeks['om_week'].apply(lambda x : x[-2:])
        first_weeks['count_W0'] = first_weeks['om_week'].apply(lambda x : 1 if x[:2] == "W0" else 0)
        W0 = first_weeks.groupby('Year').sum()
        df_convert_week['count_W0'] = df_convert_week['om_week'].apply(lambda x : W0.loc[x[-2:], 'count_W0'])
        
        df_convert_week['first_start_weekday'] = str(weekday_mapping[start_weekday]) + " 01 " + df_convert_week['om_week'].apply(lambda x : x[-2:])
        df_convert_week['first_start_weekday_dt'] = pd.to_datetime(df_convert_week['first_start_weekday'], format="%w %W %y")
        df_convert_week['offset'] = df_convert_week['first_start_weekday_dt'].dt.strftime("%d").apply(lambda x : int(x) if int(x)<7 else int(x)-7)
        df_convert_week['count_W0-om_week'] = df_convert_week['count_W0'].apply(str) + "-" + df_convert_week['om_week']
        df_convert_week['day_num_1'] = df_convert_week['count_W0-om_week'].apply(lambda x : int(x[3:][:-3])*7 if int(x[0]) < max_days_in_W0 else (int(x[3:][:-3])-1)*7) + df_convert_week['offset']
        df_convert_week['offset-day_num_1'] = df_convert_week['offset'].apply(str) + "-" + df_convert_week['day_num_1'].apply(str)
        df_convert_week['day_num'] = df_convert_week['offset-day_num_1'].apply(lambda x : int(x[2:]) if int(x[:1]) == 0 and int(x[2:]) - 7 >= 0 else 1 if int(x[2:]) - 7 < 1 else int(x[2:])-7)
        df_convert_week['day year'] = df_convert_week['day_num'].apply(str) + " " + df_convert_week['om_week'].apply(lambda x : x[-2:])
        df_convert_week['date'] = pd.to_datetime(df_convert_week['day year'], format = "%d %y")
        return df_convert_week['date']
    elif len(date_example) >= 8 and len(date_example) <= 9:
        # day, month and year
        return pd.to_datetime(series, format='%d %b %y')
    else: 
        raise ValueError(
            f"Can't convert date of unsupported fromat {date_example} from Optimacros format to pandas datetime")


def datetime_to_om_time(series: pd.Series, format: str = 'Months', start_weekday: str = 'Monday', max_days_in_W0: int = 6) -> pd.Series:
    """Функция для конвертации дат формата datetime (dd-MM-YY) в даты формата OM.

    Args:
        series (pd.Series): Серия формата datetime.
        format (str, optional): Формат результата, допустимые варианты: "Years", "Months", "Weeks", "Days". По умолчанию 'Months'.
        start_weekday (str, optional): Название перого дня недели. По умолчанию 'Monday'.
        max_days_in_w0 (int, optional): _Количество дней в неполной нулевой неделе, принимает значения от 0 до 6. По умолчанию 6.
    """
    series = pd.to_datetime(series, format='%Y-%m-%d')
    if format == 'Years':
        return 'FY' + series.dt.strftime('%y')
    elif format == 'Months':
        return series.dt.strftime('%b %y')
    elif format == 'Weeks':
        if max_days_in_W0 > 6:
            raise ValueError(f"Argument max_days_in_W0 can`t be more 6. Your value is {max_days_in_W0}.")
        weekday_mapping = {'Monday': 1,
                       'Tuesday': 2,
                       'Wednesday': 3,
                       'Thursday': 4,
                       'Friday': 5,
                       'Saturday': 6,
                       'Sunday': 7}
        weekday_offset = weekday_mapping[start_weekday]
        df_weeks = pd.DataFrame()
        df_weeks['day_num'] = series.dt.strftime("%j").apply(lambda x : int(x))
        df_weeks['offset'] = series.apply(lambda x : x.replace(month = 1, day = 1)).dt.strftime("%w").apply(lambda x : int(x) if x != "0" else 7)
        df_weeks['day_num+offset'] = df_weeks['day_num'] + df_weeks['offset'] - 1
        df_weeks['week_num'] = df_weeks['day_num+offset'].apply(lambda x : (x - weekday_offset)//7)
        if len(df_weeks[df_weeks['week_num'] == -1]) != 0:
            df_weeks['week_num'] = df_weeks['week_num'] + 1
        if len(df_weeks[df_weeks['week_num'] == 0]) > max_days_in_W0:
            df_weeks['week_num'] = df_weeks['week_num'] + 1
        df_weeks['week'] = "W" + df_weeks['week_num'].apply(str) + "_" + series.dt.strftime("%y")
        return df_weeks['week']
    elif format == 'Days':
        return series.dt.strftime('%d %b %y').str.lstrip('0')
    else:
        raise ValueError(f"Can't convert date to unsupported fromat {format}")


def dataframes_to_om_csv(dfs: list,
                         path: str,
                         colunms: list = None,  # type: ignore
                         time_column: str = None,  # type: ignore
                         datetime_column: str = 'datetime',
                         time_format: str = 'Months',
                         reset_index: bool = True,
                         encoding: str = 'utf-8',
                         sep: str = ';') -> NoReturn:  # type: ignore
    if reset_index  == False:
        output = pd.concat(
            map(lambda df: df.reset_index(), dfs), ignore_index=True)
    else :
        output = pd.concat(dfs, ignore_index=True)
        
    if time_column is not None:
        output[time_column] = datetime_to_om_time(
            output[datetime_column], format=time_format)

    if colunms is not None:
        output = output.loc[:, colunms]

    output.to_csv(path, sep=sep, encoding=encoding, index=False)


def csv_to_dataframe(filename: str, sep: str = ";", encoding = "UTF 8") -> pd.DataFrame:
    df = pd.read_csv(filepath_or_buffer=filename, sep=sep, encoding=encoding)
    df.reset_index(inplace=True)
    offset = df.loc[1].count() - df.loc[0].count()
    df.columns = df.loc[0][-1*offset-1:-1].index.to_list() + df.loc[0][offset:].to_list()
    df = df[1:]
    df = df.reset_index(drop=True)
    return df


def excel_to_dataframe(filename: str) -> pd.DataFrame:
    df = pd.read_excel(filename)
    dim_count = df.loc[0].count()-1
    dims = df.loc[0][0:dim_count].to_list()
    cubes = df.loc[1][dim_count:].to_list()
    df.columns = dims+cubes
    df = df[2:]
    df = df.reset_index(drop=True)
    return df


def file_to_dataframe(file_path: str,
                      file_type: str,
                      sep: str = ";",
                      encoding: str = "UTF 8",
                      columns: list[str] = None,  # type: ignore
                      invert_columns: bool = False,
                      index_column: str = None,  # type: ignore
                      columns_to_convert: dict = None) -> pd.DataFrame:  # type: ignore
    """
        Function for convert files to DataFrame, where dimension and cubes in columns.
        Work whis multicubes, where all dimensions in rows and cubes in columns.
    """
    if file_type in ['csv', 'txt']:
        df = csv_to_dataframe(filename=file_path, sep=sep, encoding=encoding)
    elif file_type in ['om_csv', 'om_txt']:
        df = pd.read_csv(filepath_or_buffer=file_path, sep=sep, encoding=encoding)
    elif file_type in ['xlsx']:
        df = excel_to_dataframe(filename=file_path)
    else:
        raise ValueError(f"Unsupport file extension: {file_type}")
    if columns != None:
        columns_list = columns
        if invert_columns == True:
            columns_list = []
            for i in df.columns.to_list():
                if i not in columns:
                    columns_list.append(i)
        df = df[columns_list]
    if columns_to_convert != None:
        for type in columns_to_convert.keys():
            df = convert_columns(df, columns_to_convert[type], type)
    if index_column != None:
        df = df.set_index(index_column)
    return df


def convert_int_om_to_pandas(series: pd.Series) -> pd.Series:
    series = series.replace(to_replace= r",",value= ".", regex=True)
    series = series.apply(np.float64)
    series = series.apply(np.rint)
    series = series.apply(np.int64)
    return series

def convert_float_om_to_pandas(series: pd.Series) -> pd.Series:
    series = series.replace(to_replace= r",",value= ".", regex=True)
    series = series.apply(np.float64)
    return series

def convert_boolean_om_to_pandas(series: pd.Series) -> pd.Series:
    if type(series.loc[0]) == str :
        series = series.apply(lambda x: True if x == 'true' else False)

    elif type(series[0]) == np.int64:
        series = series.apply(bool)
    return series


def convert_columns(df: pd.DataFrame, columns: list[str], data_type: str) -> pd.DataFrame:
    if data_type == 'int':
        for i in columns:
            df[i] = convert_int_om_to_pandas(df[i])

    elif data_type == 'float':
        for i in columns:
            df[i] = convert_float_om_to_pandas(df[i])
    
    elif data_type == 'bool':
        for i in columns:
            df[i] = convert_boolean_om_to_pandas(df[i])

    elif data_type == 'om_date':
        for i in columns:
            df[i] = om_time_to_datetime(df[i])

    elif data_type == 'date':
        for i in columns:
            df[i] = datetime_to_om_time(df[i])

    else:
        raise ValueError(f"Unsupport data type of columns: {data_type}")
    return df


def dataframe_to_list(df: pd.DataFrame, columns: list[str], invert_columns: bool = False) -> list[pd.DataFrame]:
    columns_list = columns
    if invert_columns == True:
        columns_list = []
        for i in df.columns.to_list():
            if i not in columns:
                columns_list.append(i)
    gb = df.groupby(columns_list)
    gb_list = [gb.get_group(x) for x in gb.groups.keys()]
    return gb_list
