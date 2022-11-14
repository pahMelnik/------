import pandas as pd
import numpy as np
from typing import NoReturn



def om_time_to_datetime(series: pd.Series) -> pd.Series:
    date_example = series.iloc[0]

    if len(date_example) == 4:
        # only year
        return pd.to_datetime(series.str.lstrip('FY'), format='%y')
    elif len(date_example) == 6:
        # month and year
        return pd.to_datetime(series, format='%b %y')
    elif len(date_example) >= 8 and len(date_example) <= 9:
        # day, month and year
        return pd.to_datetime(series, format='%d %b %y')
    else:
        raise ValueError(
            f"Can't convert date of unsupported fromat {date_example} from Optimacros format to pandas datetime")


def datetime_to_om_time(series: pd.Series, format: str = 'Months') -> pd.Series:
    series = pd.to_datetime(series, format='%Y-%m-%d')
    if format == 'Years':
        return 'FY' + series.dt.strftime('%y')
    elif format == 'Months':
        return series.dt.strftime('%b %y')
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
