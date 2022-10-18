import sys
sys.path.append('C:/Users/l8985/Nextcloud/OMRUS_PF 3125_Матвей Щербаков/Работа/Скрипты/Библиотека для конвертации OM в pandas DataFrame')
from om_pandas import *
import pandas as pd
import datetime
import pytest
import random
import hashlib
import csv

class generate():
    
    def om_time_to_date_time_test_data(min_Year: int = 2010, max_Year: int = 2020, max_Months: int = 12, max_Day: int = 28):
        MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        MONTHS = MONTHS[:max_Months+1]
        OM_MIN_YEAR = int(str(min_Year)[2:])
        OM_MAX_YEAR = int(str(max_Year)[2:])
        om_time_to_datetime_input_list = ["FY"+ str(i) for i in range(OM_MIN_YEAR,OM_MAX_YEAR+1)]
        om_time_to_datetime_input_list += [i+ ' ' + str(OM_MAX_YEAR) for i in MONTHS]
        om_time_to_datetime_input_list += [str(i) + ' ' + MONTHS[-1] + ' ' + str(OM_MAX_YEAR) for i in range(1,max_Day+1)]
        
        om_time_to_datetime_result_list = [str(datetime.date(i, 1, 1))  for i in range(min_Year,max_Year+1)]
        om_time_to_datetime_result_list += [str(datetime.date(max_Year, i, 1)) for i in range (1,max_Months+1)]
        om_time_to_datetime_result_list += [str(datetime.date(max_Year, max_Months, i)) for i in range(1,max_Day+1)]
        
        test_data = [tuple([pd.Series([om_time_to_datetime_input_list[i]]),pd.Series([om_time_to_datetime_result_list[i]])]) for i in range(len(om_time_to_datetime_input_list))]
        return test_data
    
    
    def date_time_to_om_time_test_data(min_Year: int = 2010, max_Year: int = 2020, max_Months: int = 12, max_Day: int = 28):
        MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        MONTHS = MONTHS[:max_Months+1]
        OM_MIN_YEAR = int(str(min_Year)[2:])
        OM_MAX_YEAR = int(str(max_Year)[2:])
        om_time_to_datetime_input_list = [pd.to_datetime(pd.Series(datetime.date(i, 1, 1)), errors='coerce') for i in range(min_Year,max_Year+1)]
        format = ["Years" for i in range(len(om_time_to_datetime_input_list))]
        
        om_time_to_datetime_input_list += [pd.to_datetime(pd.Series(datetime.date(max_Year, i, 1)), errors='coerce') for i in range (1,max_Months+1)]
        format += ["Months" for i in range(len(om_time_to_datetime_input_list)-len(format))]
        
        om_time_to_datetime_input_list += [pd.to_datetime(pd.Series(datetime.date(max_Year, max_Months, i)), errors='coerce') for i in range(1,max_Day+1)]
        format += ["Days" for i in range(len(om_time_to_datetime_input_list)-len(format))]
        
        
        om_time_to_datetime_result_list = [pd.Series("FY"+ str(i)) for i in range(OM_MIN_YEAR,OM_MAX_YEAR+1)]
        om_time_to_datetime_result_list += [pd.Series(i+ ' ' + str(OM_MAX_YEAR)) for i in MONTHS]
        om_time_to_datetime_result_list += [pd.Series(str(i) + ' ' + MONTHS[-1] + ' ' + str(OM_MAX_YEAR)) for i in range(1,max_Day+1)]
        
        
        test_data = [tuple([om_time_to_datetime_input_list[i], om_time_to_datetime_result_list[i], format[i]]) for i in range(len(om_time_to_datetime_input_list))]
        return test_data

    
    def csv_to_dataframe_test_data(path: list[str], expected_result_path: list[str]):
        test_data = [tuple([i, pd.read_pickle(k)]) for i, k in zip(path, expected_result_path)]
        return test_data
    
    
    def excel_to_dataframe_test_data(path: list[str], expected_result_path: list[str]):
        test_data = [tuple([i, pd.read_pickle(k)]) for i, k in zip(path, expected_result_path)]
        return test_data


    def file_to_dataframe_test_data(path: list[str], file_type: list[str],expected_result_path: list[str]):
        test_data = [tuple([i, pd.read_pickle(k)]) for i, k in zip(path, file_type, expected_result_path)]
        return test_data
    
    def convert_num_om_to_pandas_test_data(tests_count: int):
        test_data = []
        delimiter = [",","."]
        for i in range(tests_count):
            test_value = f"{random.randint(0,10)}{random.choice(delimiter)}{random.randint(0,1000)}"
            test_data.append((pd.Series(test_value), pd.Series(float(test_value.replace(",",".")))))
        return test_data
    
    def convert_boolean_om_to_pandas_test_data(tests_count: int):
        test_data = []
        seq = [0,1, "true", "false"]
        except_seq = [False, True, True, False]
        for i in range(tests_count):
            index = random.randint(0,3)
            test_data.append((pd.Series(seq[index]), pd.Series(except_seq[index])))
        return test_data


@pytest.mark.parametrize("om_time, expected_result",
                         generate.om_time_to_date_time_test_data())
def test_om_time_to_datetime(om_time: pd.Series, expected_result: pd.Series):
    assert all(om_time_to_datetime(om_time) == expected_result)


@pytest.mark.parametrize("date_time, expected_result, format",
                         generate.date_time_to_om_time_test_data())
def test_datetime_to_om_time(date_time: pd.Series, expected_result: pd.Series, format: str):
    assert all(datetime_to_om_time(date_time, format) == expected_result)
    
    
@pytest.mark.parametrize("path, sep, encoding, expected_result",
                         [("tests/test_data/csv.csv", ";", "Windows 1251", "tests/test_data/expected_csv.pkl"),
                          ("tests/test_data/txt.txt", ";", "Windows 1251", "tests/test_data/expected_txt.pkl")])
def test_csv_to_dataframe(path: str, sep: str, encoding: str, expected_result: str):
    assert all(csv_to_dataframe(path) == pd.read_pickle(expected_result))
    
    
@pytest.mark.parametrize("path, expected_result",
                         [("tests/test_data/excel.xlsx", "tests/test_data/expected_excel.pkl")])
def test_excel_to_dataframe(path: str, expected_result: str):
    assert all(excel_to_dataframe(path) == pd.read_pickle(expected_result))
    

@pytest.mark.parametrize("file_path, expected_result, file_type, sep, encoding, columns, invert_columns, index_column",
                         [("tests/test_data/excel.xlsx",
                           "tests/test_data/expected_excel.pkl",
                           "xlsx", ";" ,"UTF 8", None, False, None),
                          ("tests/test_data/csv.csv", 
                           "tests/test_data/expected_csv.pkl",
                           "csv", ";" ,"UTF 8", None, False, None),
                          ("tests/test_data/om_csv.csv", 
                           "tests/test_data/expected_om_csv.pkl",
                           "om_csv", ";" ,"Windows 1251", None, False, None),
                          ("tests/test_data/txt.txt", 
                           "tests/test_data/expected_txt.pkl",
                           "txt", ";" ,"Windows 1251", None, False, None),
                          ("tests/test_data/om_txt.txt", 
                           "tests/test_data/expected_om_txt.pkl",
                           "om_txt", ";" ,"Windows 1251", None, False, None)])  
def test_file_to_dataframe(file_path: str,
                           expected_result: str,
                           file_type: str,
                           sep: str,
                           encoding: str,
                           columns: list[str],
                           invert_columns: bool,
                           index_column: str):
    
    assert all(file_to_dataframe(file_path = file_path,
                                 file_type = file_type,
                                 sep = sep,
                                 encoding = encoding,
                                 columns = columns,
                                 invert_columns = invert_columns,
                                 index_column = index_column) == pd.read_pickle(expected_result))
    
@pytest.mark.parametrize("data, expected_result",
                         generate.convert_num_om_to_pandas_test_data(10))
def test_convert_num_om_to_pandas(data: pd.Series, expected_result: pd.Series):
    assert all(convert_num_om_to_pandas(data) == expected_result)
    

@pytest.mark.parametrize("data, expected_result",
                         generate.convert_boolean_om_to_pandas_test_data(10))
def test_convert_boolean_om_to_pandas(data: pd.Series, expected_result: pd.Series):
    assert all(convert_boolean_om_to_pandas(data) == expected_result)
    

@pytest.mark.parametrize("test_data, columns, invert_columns, expected_result",
                         [
                             (
                                 pd.DataFrame(data= {"Group 1" : ["A", "A", "B", "B", "C", "C"],
                                                     "Group 2" : ["1", "2", "1", "2", "1", "2"],
                                                     "Number" : [1,2,3,4,5,6]}),
                                 ["Group 1", "Group 2"],
                                 False,
                                 [pd.DataFrame(data= {"Group 1" : ["A"], "Group 2" : ["1"], "Number" : [1]}, index=[0]),
                                  pd.DataFrame(data= {"Group 1" : ["A"], "Group 2" : ["2"], "Number" : [2]}, index=[1]),
                                  pd.DataFrame(data= {"Group 1" : ["B"], "Group 2" : ["1"], "Number" : [3]}, index=[2]),
                                  pd.DataFrame(data= {"Group 1" : ["B"], "Group 2" : ["2"], "Number" : [4]}, index=[3]),
                                  pd.DataFrame(data= {"Group 1" : ["C"], "Group 2" : ["1"], "Number" : [5]}, index=[4]),
                                  pd.DataFrame(data= {"Group 1" : ["C"], "Group 2" : ["2"], "Number" : [6]}, index=[5])]
                             ),
                             (
                                 pd.DataFrame(data= {"Group 1" : ["A", "A", "B", "B", "C", "C"],
                                                     "Group 2" : ["1", "2", "1", "2", "1", "2"],
                                                     "Number" : [1,2,3,4,5,6]}),
                                 ["Group 1"],
                                 False,
                                 [pd.DataFrame(data= {"Group 1" : ["A", "A"], "Group 2" : ["1", "2"], "Number" : [1,2]}, index=[0,1]),
                                  pd.DataFrame(data= {"Group 1" : ["B", "B"], "Group 2" : ["1", "2"], "Number" : [3,4]}, index=[2,3]),
                                  pd.DataFrame(data= {"Group 1" : ["C", "C"], "Group 2" : ["1", "2"], "Number" : [5,6]}, index=[4,5])]
                             ),
                             (
                                 pd.DataFrame(data= {"Group 1" : ["A", "A", "B", "B", "C", "C"],
                                                     "Group 2" : ["1", "2", "1", "2", "1", "2"],
                                                     "Number" : [1,2,3,4,5,6]}),
                                 ["Group 2"],
                                 False,
                                 [pd.DataFrame(data= {"Group 1" : ["A", "B", "C"], "Group 2" : ["1", "1", "1"], "Number" : [1,3,4]}, index=[0,2,4]),
                                  pd.DataFrame(data= {"Group 1" : ["A", "B", "C"], "Group 2" : ["2", "2", "2"], "Number" : [2,4,6]}, index=[1,3,5])]
                             ),
                             (
                                 pd.DataFrame(data= {"Group 1" : ["A", "A", "B", "B", "C", "C"],
                                                     "Group 2" : ["1", "2", "1", "2", "1", "2"],
                                                     "Number" : [1,2,3,4,5,6]}),
                                 ["Number"],
                                 True,
                                 [pd.DataFrame(data= {"Group 1" : ["A"], "Group 2" : ["1"], "Number" : [1]}, index=[0]),
                                  pd.DataFrame(data= {"Group 1" : ["A"], "Group 2" : ["2"], "Number" : [2]}, index=[1]),
                                  pd.DataFrame(data= {"Group 1" : ["B"], "Group 2" : ["1"], "Number" : [3]}, index=[2]),
                                  pd.DataFrame(data= {"Group 1" : ["B"], "Group 2" : ["2"], "Number" : [4]}, index=[3]),
                                  pd.DataFrame(data= {"Group 1" : ["C"], "Group 2" : ["1"], "Number" : [5]}, index=[4]),
                                  pd.DataFrame(data= {"Group 1" : ["C"], "Group 2" : ["2"], "Number" : [6]}, index=[5])]
                             ),
                             (
                                 pd.DataFrame(data= {"Group 1" : ["A", "A", "B", "B", "C", "C"],
                                                     "Group 2" : ["1", "2", "1", "2", "1", "2"],
                                                     "Number" : [1,2,3,4,5,6]}),
                                 ["Group 2", "Number"],
                                 True,
                                 [pd.DataFrame(data= {"Group 1" : ["A", "A"], "Group 2" : ["1", "2"], "Number" : [1,2]}, index=[0,1]),
                                  pd.DataFrame(data= {"Group 1" : ["B", "B"], "Group 2" : ["1", "2"], "Number" : [3,4]}, index=[2,3]),
                                  pd.DataFrame(data= {"Group 1" : ["C", "C"], "Group 2" : ["1", "2"], "Number" : [5,6]}, index=[4,5])]
                             )
                         ])
def test_dataframe_to_list(test_data : pd.DataFrame, columns : list[str], invert_columns : bool, expected_result : list[pd.DataFrame]):
    for data, result in zip(dataframe_to_list(test_data, columns, invert_columns), expected_result):
        assert all(data == result)
        
@pytest.mark.parametrize("dfs, path, keep_only, time_column, datetime_column, time_format, reset_index, encoding, sep, expected_result_path",
                         [
                             (
                                 [pd.DataFrame(data= {"Group 1" : ["Jan 22"], "Group 2" : ["FY22"], "Group 3": ["1 Jan 22"], "Group 4": ["2022-01-01"], "Number" : [1]}, index=[0]),
                                  pd.DataFrame(data= {"Group 1" : ["Jan 22"], "Group 2" : ["FY22"], "Group 3": ["2 Jan 22"], "Group 4": ["2022-01-02"], "Number" : [2]}, index=[1]),
                                  pd.DataFrame(data= {"Group 1" : ["Feb 22"], "Group 2" : ["FY22"], "Group 3": ["1 Feb 22"], "Group 4": ["2022-02-01"], "Number" : [3]}, index=[2]),
                                  pd.DataFrame(data= {"Group 1" : ["Feb 22"], "Group 2" : ["FY22"], "Group 3": ["2 Feb 22"], "Group 4": ["2022-02-02"], "Number" : [4]}, index=[3]),
                                  pd.DataFrame(data= {"Group 1" : ["Mar 22"], "Group 2" : ["FY22"], "Group 3": ["1 Mar 22"], "Group 4": ["2022-03-01"], "Number" : [5]}, index=[4]),
                                  pd.DataFrame(data= {"Group 1" : ["Mar 22"], "Group 2" : ["FY22"], "Group 3": ["2 Mar 22"], "Group 4": ["2022-03-02"], "Number" : [6]}, index=[5])],
                                 "tests/test_data/test.csv",
                                 None,
                                 None,
                                 None,
                                 None,
                                 True,
                                 "utf-8",
                                 ";",
                                 "tests/test_data/test_output_None_None_None_None_True_utf-8_;.csv"
                              )
                          ]
                         )       
def test_dataframes_to_om_csv(dfs: list,
                         path: str,
                         keep_only: list,
                         time_column: str,
                         datetime_column: str,
                         time_format: str,
                         reset_index: bool,
                         encoding: str,
                         sep: str,
                         expected_result_path: str):
  
    dataframes_to_om_csv(dfs, path, keep_only, time_column, datetime_column, time_format, reset_index, encoding, sep)
    with open(path, 'r') as result, open(expected_result_path, 'r') as expected_result:
        result_list = list(csv.DictReader(result))
        expected_result_list = list(csv.DictReader(expected_result))
    assert result_list == expected_result_list
    
    
@pytest.mark.parametrize("dfs, path, keep_only, time_column, datetime_column, time_format, reset_index, encoding, sep, expected_result_path",
                         [
                             (
                                 [pd.DataFrame(data= {"Group 1" : ["Jan 22"], "Group 2" : ["FY22"], "Group 3": ["1 Jan 22"], "Group 4": ["2022-01-01"], "Number" : [1]}, index=[0]),
                                  pd.DataFrame(data= {"Group 1" : ["Jan 22"], "Group 2" : ["FY22"], "Group 3": ["2 Jan 22"], "Group 4": ["2022-01-02"], "Number" : [2]}, index=[1]),
                                  pd.DataFrame(data= {"Group 1" : ["Feb 22"], "Group 2" : ["FY22"], "Group 3": ["1 Feb 22"], "Group 4": ["2022-02-01"], "Number" : [3]}, index=[2]),
                                  pd.DataFrame(data= {"Group 1" : ["Feb 22"], "Group 2" : ["FY22"], "Group 3": ["2 Feb 22"], "Group 4": ["2022-02-02"], "Number" : [4]}, index=[3]),
                                  pd.DataFrame(data= {"Group 1" : ["Mar 22"], "Group 2" : ["FY22"], "Group 3": ["1 Mar 22"], "Group 4": ["2022-03-01"], "Number" : [5]}, index=[4]),
                                  pd.DataFrame(data= {"Group 1" : ["Mar 22"], "Group 2" : ["FY22"], "Group 3": ["2 Mar 22"], "Group 4": ["2022-03-02"], "Number" : [6]}, index=[5])],
                                 "tests/test_data/test.csv",
                                 None,
                                 None,
                                 None,
                                 None,
                                 True,
                                 "utf-8",
                                 ";",
                                 "tests/test_data/test_output_None_None_None_None_True_utf-8_;.csv"
                              )
                          ]
                         )       
def test_hash_dataframes_to_om_csv(dfs: list,
                         path: str,
                         keep_only: list,
                         time_column: str,
                         datetime_column: str,
                         time_format: str,
                         reset_index: bool,
                         encoding: str,
                         sep: str,
                         expected_result_path: str):
    BUF_SIZE = 65536
    hash_result = hashlib.md5()
    hash_expected_result = hashlib.md5()
    
    dataframes_to_om_csv(dfs, path, keep_only, time_column, datetime_column, time_format, reset_index, encoding, sep)
    with open(path, "rb") as result:
        while True:
            data = result.read(BUF_SIZE)
            if not data:
                break
            hash_result.update(data)
    with open(expected_result_path, "rb") as expected_result:
        while True:
            data = expected_result.read(BUF_SIZE)
            if not data:
                break
            hash_expected_result.update(data)
    assert hash_result.hexdigest() == hash_expected_result.hexdigest()