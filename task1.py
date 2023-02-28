"""
Написать программу на Python, которая делает следующие действия:
1. Создает 50 zip-архивов, в каждом 100 xml файлов со случайными данными следующей структуры:
<root>
<var name=’id’ value=’<случайное уникальное строковое значение>’/>
<var name=’level’ value=’<случайное число от 1 до 100>’/>
<objects>
<object name=’<случайное строковое значение>’/>
<object name=’<случайное строковое значение>’/>
…
</objects>
</root>
В тэге objects случайное число (от 1 до 10) вложенных тэгов object.
"""

import zipfile
import random
import uuid
import os
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring

from consts_and_utils import DIR, timeit, NUMBER_ARCHIVES, NUMBER_XML_FILES


def get_random_string() -> str:
    """Возвращает случайное уникальное строковое значение"""
    return uuid.uuid4().hex


def generate_xml() -> str:
    """
    Генерация xml в виде:
    <root>
    <var name=’id’ value=’<случайное уникальное строковое значение>’/>
    <var name=’level’ value=’<случайное число от 1 до 100>’/>
    <objects>
    <object name=’<случайное строковое значение>’/>
    <object name=’<случайное строковое значение>’/>
    …
    </objects>
    </root>
    В тэге objects случайное число (от 1 до 10) вложенных тэгов object.
    """
    root = Element('root')
    id_var = SubElement(root, 'var')
    id_var.set('name', 'id')
    id_var.set('value', get_random_string())
    level_var = SubElement(root, 'var')
    level_var.set('name', 'level')
    level_var.set('value', str(random.randint(1, 100)))
    objects = SubElement(root, 'objects')
    for _ in range(random.randint(1, 10)):
        object_element = SubElement(objects, 'object')
        object_element.set('name', get_random_string())

    return tostring(root, encoding='unicode')


def main() -> None:
    """Создание архивов"""
    os.mkdir(DIR)
    for index_zip_archive in range(NUMBER_ARCHIVES):
        zip_name = os.path.join(DIR, 'archive_{}.zip'.format(index_zip_archive))
        with zipfile.ZipFile(zip_name, 'w') as zip_file:
            for index_xml_file in range(NUMBER_XML_FILES):
                xml_name = 'file_{}.xml'.format(index_xml_file)
                xml_data = generate_xml()
                zip_file.writestr(xml_name, xml_data)


if __name__ == "__main__":
    main()
