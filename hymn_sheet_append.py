import requests
import PyPDF2
import os
from urllib.request import urlopen
from os import listdir, walk
from os.path import isfile, join
import re

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
    append_pdf = PyPDF2.PdfMerger()
    for unique_file in all_files:
        append_pdf.append(f'{ full_path }\\{ unique_file }')
    append_pdf.write(f'{full_path}\\{ final_name }.pdf')
    append_pdf.close()

def split_pages(originalFileName, newPath):
    originalFileContent = PdfReader(open(originalFileName, "rb"))
    for i in range(len(originalFileContent.pages)):
        output = PdfWriter()
        output.add_page(originalFileContent.pages[i])
        with open(newPath % (i + 1), "wb") as outputStream:
            output.write(outputStream)

def num_sort(test_string):
    return list(map(int, re.findall(r'\d+', test_string)))[0]

full_path = ''
check_path(full_path)
download_hymns(1, 1348, 'h', full_path) #traditionais
download_hymns(1, 75, 's', full_path) #suplementos
download_hymns(1424, 1503, 'n', full_path) #novos
filenames = get_file_names(full_path)
filenames.sort(key=num_sort) 
append_hymns(filenames, full_path, 'full_hymns')
