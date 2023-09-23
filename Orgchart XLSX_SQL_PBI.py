from openpyxl import load_workbook
import csv

def read_csv(file_path):
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        return csv.rcsv_reader
    
print(read_csv('Data.csv'))