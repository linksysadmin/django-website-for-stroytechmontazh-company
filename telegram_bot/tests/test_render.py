import datetime
import unittest

from config import BASE_DIR
from service.converting import get_additional_services_from_string, get_standard_services_from_string, \
    convert_string_to_dict
from service.file_handler import create_excel_file

ADDRESS = 'test_ADDRESS'
STANDARD_SERVICES = '1:5 2:6 3:7'
ADDITIONAL_SERVICES = '+ Промывка Котла:300:4 + Ремонт бака: 100 : 2'
string = f'{ADDRESS} | {STANDARD_SERVICES} {ADDITIONAL_SERVICES}'

string_without_standard_services = f'{ADDRESS} | {ADDITIONAL_SERVICES}'
string_without_additional_services = f'{ADDRESS} | {STANDARD_SERVICES}'
string_without_special_symbols = f'{ADDRESS} | 153 26 37'
string_without_address = f'| {STANDARD_SERVICES}{ADDITIONAL_SERVICES}'

dict_data = {'address': f'{ADDRESS}',
             'standard_services': {1: 5, 2: 6, 3: 7},
             'additional_services': {
                 1: {'service': 'Промывка Котла', 'price': 300, 'count': 4},
                 2: {'service': 'Ремонт бака', 'price': 100, 'count': 2},
             }}

dict_without_additional_services = {'standard_services': {}}
dict_without_standard_services = {'additional_services': {}}
path = f"{BASE_DIR}/static/objects_offers/{ADDRESS}_{datetime.datetime.now().strftime('%Y-%m-%d')}.xlsx"


class TestConvertStringToDict(unittest.TestCase):

    def test_convert(self):
        self.assertEqual(convert_string_to_dict(string), dict_data)
        self.assertEqual(get_standard_services_from_string(string), dict_data['standard_services'])
        self.assertEqual(get_standard_services_from_string(string_without_additional_services), dict_data['standard_services'])
        self.assertEqual(get_additional_services_from_string(string), dict_data['additional_services'])
        self.assertEqual(get_additional_services_from_string(string_without_standard_services),
                         dict_data['additional_services'])


class TestGeneratingExcelFile(unittest.TestCase):


    def test_retrieve_data_from_dict(self):
        self.assertEqual(create_excel_file(dict_without_additional_services), False)
        self.assertEqual(create_excel_file(dict_without_standard_services), False)
        self.assertEqual(create_excel_file(dict_data), path)
