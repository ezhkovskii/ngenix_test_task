"""
Обрабатывает директорию с полученными zip архивами, разбирает вложенные xml файлы и формирует 2 csv файла:
Первый: id, level - по одной строке на каждый xml файл
Второй: id, object_name - по отдельной строке для каждого тэга object (получится от 1 до 10 строк на каждый xml файл)
Очень желательно сделать так, чтобы задание 2 эффективно использовало ресурсы многоядерного процессора.
"""


import os
import zipfile
from xml.etree.ElementTree import ElementTree
import csv
from itertools import chain
from concurrent import futures

from consts_and_utils import DIR, timeit


def get_xml_info(xml_file: zipfile.ZipExtFile) -> dict:
    """
    Парсинг xml файла.
    Вытаскиваем id, level и name из objects.
    """
    tree = ElementTree(file=xml_file)
    root = tree.getroot()

    id_value = root.find('var[@name="id"]').get('value')
    level_value = root.find('var[@name="level"]').get('value')
    objects = [obj.get('name') for obj in root.findall('objects/object')]
    
    return {'id': id_value, 'level': level_value, 'objects': objects}


def processing_archive(zip_name: str) -> list:
    """
    Обработка zip архива.
    """
    xml_info_files = []
    with zipfile.ZipFile(zip_name, 'r') as zip_file:
        xml_info_files = []
        for xml_name in zip_file.namelist():
            if xml_name.endswith('.xml'):
                xml_file = zip_file.open(xml_name)
                xml_info_files.append(get_xml_info(xml_file))

    return xml_info_files


def create_csv_files(xml_info_files: list) -> None:
    """
    Создание csv файлов.
    Первый: id, level - по одной строке на каждый xml файл
    Второй: id, object_name - по отдельной строке для каждого тэга object (получится от 1 до 10 строк на каждый xml файл)
    """
    with open('csv_file1.csv', 'w', newline='') as csv_file1, open('csv_file2.csv', 'w', newline='') as csv_file2:
        csv_writer1 = csv.writer(csv_file1)
        csv_writer2 = csv.writer(csv_file2)

        for xml in xml_info_files:
            csv_writer1.writerow([xml['id'], xml['level']])
            for obj in xml['objects']:
                csv_writer2.writerow([xml['id'], obj])


@timeit
def main_multiprocessing(zip_files: list) -> None:
    """
    Обработка zip архивов в многоядерном режиме.
    """
    result = []
    with futures.ProcessPoolExecutor(6) as executor:
        result += executor.map(processing_archive, zip_files)
        result = list(chain(*result))
    create_csv_files(result)         
      

@timeit
def main(zip_files: list) -> None:
    """
    Обработка zip архивов в обычном режиме.
    """
    result = []
    for zip_name in zip_files:
        result += processing_archive(zip_name)
    create_csv_files(result)   


if __name__ == "__main__":
    zip_files = [os.path.join(DIR, zip_name) for zip_name in os.listdir(DIR)  if zip_name.endswith('.zip')]
    main_multiprocessing(zip_files)

    #main(zip_files)
