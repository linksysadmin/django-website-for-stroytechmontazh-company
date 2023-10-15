import datetime
import logging

from openpyxl.styles import Border, Side
from openpyxl import Workbook
from sqlalchemy.exc import ArgumentError

from config import BASE_DIR
from service.models import session, Service


logger = logging.getLogger()

DIR_FOR_SAVE_FILE = f'{BASE_DIR}/static/objects_offers'
COLUMNS_NAME = ['Номер услуги', 'Услуга', 'Стоимость', 'Количество', 'Сумма']


def get_additional_services(services):
    """ ADD ADDITIONAL SERVICES """
    try:
        rows = []
        additional_services = services.get('additional_services')
        for key, value in additional_services.items():
            service_id = 'Дополнительно'
            row = [service_id, value['service'], value['price'], value['count'], (value['price'] * value['count'])]

            rows.append(row)
        return rows
    except Exception as e:
        logger.error(e)
        return False


def get_standard_services(services):
    """ ADD STANDARD SERVICES """
    try:
        rows = []
        standard_services_ids = services.get('standard_services')
        services_ = session.query(Service).filter(Service.id.in_(standard_services_ids)).all()
        for row in services_:
            amount_work = standard_services_ids[row.id]
            row = [row.id, row.title, row.price, amount_work, (row.price * amount_work)]
            rows.append(row)
        return rows
    except ArgumentError:
        logger.error('Неверный аргумент')
        return False


def create_excel_file(dict_data: dict) -> str | bool:
    try:
        if not dict_data['address']:
            return False
        elif not dict_data['standard_services']:
            additional_services = get_additional_services(dict_data)
            rows = additional_services
        elif not dict_data['additional_services']:
            standard_services = get_standard_services(dict_data)
            rows = standard_services

        else:
            standard_services = get_standard_services(dict_data)
            additional_services = get_additional_services(dict_data)
            rows = standard_services + additional_services
    except KeyError as e:
        logger.error(f'В словаре отсутствует ключ {e}')
        return False

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = dict_data['address']
    sheet.append(COLUMNS_NAME)

    for row in rows:
        sheet.append(row)

    count_of_lines = len(sheet['E'])

    # ADD SUM
    sheet[f'E{count_of_lines + 2}'] = f'=SUM(E2:E{count_of_lines})'

    # ADD DATE
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    sheet[f'A{count_of_lines + 2}'] = f'Дата: {date}'

    # STYLE
    column_size = {"A": 17, "B": 50, "C": 12, "D": 15, "E": 12}
    for letter, size in column_size.items():
        sheet.column_dimensions[letter].width = size

    thins = Side(border_style="medium", color="000000")
    sheet[f'A{count_of_lines + 2}'].border = Border(top=thins, bottom=thins, left=thins, right=thins)

    path = f"{DIR_FOR_SAVE_FILE}/{dict_data['address']}_{date}.xlsx"
    # SAVE
    workbook.save(filename=path)

    return path

