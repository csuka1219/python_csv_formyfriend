import os
import pandas as pd
import pyexcel

csvPath = 'c:\\Users\\Peti\\Desktop\\Report\\csv\\'
output = 'C:\\Users\\Peti\\Desktop\\Report\\output\\'
# csvPath = 'D:\\Work\\szkriptek\\'
# output = 'D:\\Work\\szkriptek\\'

def get_filenames():
    current_directory = os.chdir(csvPath)

    file_names = os.listdir(current_directory)

    filtered_files = [file for file in file_names if file.startswith("napi_csoport_")]
    return filtered_files

def concat_files_and_add_muszakcolumn():
    files = get_filenames()
    concatenated_data = pd.DataFrame()
    for file in files:
        data = pd.read_csv(file, sep=';', encoding='utf-8')
        concatenated_data = pd.concat([concatenated_data, data], ignore_index=True)

    concatenated_data = concatenated_data.loc[:, ~concatenated_data.columns.str.contains('^Unnamed')]
    # concatenated_data = concatenated_data.iloc[:, :-1]
    concatenated_data['Műszak'] = ''
    return concatenated_data

def format_date(date_range):
    return date_range.split(' - ')[0]

def convert_to_hours_minutes(time_str):
    components = list(map(int, time_str.split(':')))
    hours, minutes = components[:2]
    if hours > 7:
        return 0
    seconds = components[2] if len(components) == 3 else 0
    result = hours + (minutes + seconds/60) / 60
    return round(result, 2)

def update_shift_status(time_str):
    if time_str == "0:00":
        return "nem"
    return "teljes"

def format_intervall(concatenated_data):
    concatenated_data['Időtartományok'] = concatenated_data['Időtartományok'].apply(format_date)
    return concatenated_data

def format_teljesmunkaidocolumn(concatenated_data):
    concatenated_data['Teljes munkaidő'] = concatenated_data['Teljes munkaidő'].apply(convert_to_hours_minutes)
    return concatenated_data

def format_muszakcolumn(concatenated_data):
    concatenated_data['Műszak'] = concatenated_data['Munka kezdés'].apply(update_shift_status)
    concatenated_data['Műszak'] = concatenated_data['Regisztrált kilépési idő'].apply(update_shift_status)
    return concatenated_data

def save_file(concatenated_data):
    concatenated_data.to_csv(f'{output}output.csv', encoding='utf-8-sig', index=False, sep = ';')
    sheet = pyexcel.get_sheet(file_name=f"{output}output.csv", delimiter=";")
    sheet.save_as(f"{output}output.xlsx")

def start():
    concatenated_data = concat_files_and_add_muszakcolumn()
    concatenated_data = format_intervall(concatenated_data)
    concatenated_data = format_teljesmunkaidocolumn(concatenated_data)
    concatenated_data = format_muszakcolumn(concatenated_data)
    save_file(concatenated_data)

if  __name__ == "__main__":
    start()
