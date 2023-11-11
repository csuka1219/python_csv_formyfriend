import os
import pandas as pd
import pyexcel

def get_filenames():
    current_directory = os.getcwd()

    file_names = os.listdir(current_directory)

    filtered_files = [file for file in file_names if file.startswith("napi_csoport_")]
    return filtered_files

def concat_files_and_add_muszakcolumn():
    files = get_filenames()
    concatenated_data = pd.DataFrame()

    for file in files:
        data = pd.read_csv(file, sep=';', encoding='utf-8')
        concatenated_data = pd.concat([concatenated_data, data], ignore_index=True)

    #* HA BELEKERÜL EGY UNNAMED OSZLOP A EXCELBE AKKOR EZT A SORT KOMMENTELD VISSZA
    # concatenated_data = concatenated_data.iloc[:, :-1]
    concatenated_data['Műszak'] = 'teljes'
    return concatenated_data

def format_date(date_range):
    return date_range.split(' - ')[0]

def convert_time_to_fraction(time_str):
    components = list(map(int, time_str.split(':')))
    hours, minutes = components[:2]
    seconds = components[2] if len(components) == 3 else 0
    result = hours + (minutes + seconds/60) / 60
    return round(result, 2)

def format_intervall(concatenated_data):
    concatenated_data['Időtartományok'] = concatenated_data['Időtartományok'].apply(format_date)
    return concatenated_data

def format_teljesmunkaidocolunm(concatenated_data):
    concatenated_data['Teljes munkaidő'] = concatenated_data['Teljes munkaidő'].apply(convert_time_to_fraction)
    return concatenated_data

def save_file(concatenated_data):
    concatenated_data.to_csv('output.csv', encoding='utf-8-sig', index=False, sep = ';')
    sheet = pyexcel.get_sheet(file_name="output.csv", delimiter=";")
    sheet.save_as("output.xlsx")

def start():
    concatenated_data = concat_files_and_add_muszakcolumn()
    concatenated_data = format_intervall(concatenated_data)
    concatenated_data = format_teljesmunkaidocolunm(concatenated_data)
    save_file(concatenated_data)

if  __name__ == "__main__":
    start()
