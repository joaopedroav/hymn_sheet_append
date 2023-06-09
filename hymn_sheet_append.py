import requests
import fitz
import os
from urllib.request import urlopen
from os import listdir, walk
from os.path import isfile, join

MAIN_URL = ''

def check_path(full_path):
    isExist = os.path.exists(full_path)
    if not isExist:
        os.makedirs(full_path)

def download_hymns(start, end, category, full_path):
    if start > end:
        raise ValueError("'End' value can't be higher than 'start' value")

    i = start
    urlpart = ''
    while i <= end:
        hymn_index = str(i)
        if category == 'h':
            urlpart = f'{ hymn_index.zfill(4) }.cif'
        elif category == 's':
            urlpart = f'S{ hymn_index.zfill(2) }.cif'
        elif category == 'n':
            urlpart = f'{ hymn_index }.let'
        url = f'{ MAIN_URL }/download.php?file=Uploaded-pdf-Files/{ urlpart }.pdf'
        print(url)
        headers=requests.head(url).headers
        downloadable = 'attachment' in headers.get('Content-Disposition', '')
        if (downloadable):        
            with urlopen(url) as file:
                content = file.read()
            
            full_name_path = f'{ full_path }\\{ hymn_index }.pdf'
            with open(full_name_path, 'wb') as download:
                download.write(content)
            
        else:
            print(f"File { url } doesn't exist or it's not available")
        i = i + 1

def get_file_names(full_path):
    for (dirpath, dirnames, filenames) in walk(full_path):
        return filenames

def append_hymns(all_files, full_path, final_name):
    doc = fitz.open()
    for unique_file in all_files:
        with fitz.open(f'{ full_path }\\{ unique_file }') as mfile:
            doc.insert_pdf(mfile)
    doc.save(f'{full_path}\\{ final_name }.pdf')
    doc.close()
            

full_path = 'C:\\Users\\Desenv\\Downloads\\hymns'
check_path(full_path)
download_hymns(1, 1348, 'h', full_path) #traditionais
download_hymns(1, 75, 's', full_path) #suplementos
download_hymns(1424, 1500, 'n', full_path) #novos
filenames = get_file_names(full_path)
append_hymns(filenames, full_path, 'full_hymns')
