import logging


logger = logging.getLogger()


def convert_string_to_dict(string_message: str) -> dict | bool:

    if '|' not in string_message:
        return False
    if not any(symb in string_message for symb in '+:'):
        logger.warning(f'Отсутствуют знаки: "+:"')
        return False

    address = get_address_from_string(string_message)
    standard_services = get_standard_services_from_string(string_message)
    additional_services = get_additional_services_from_string(string_message)

    result_dict_of_services = {
        'address': address,
        'standard_services': standard_services,
        'additional_services': additional_services
    }
    return result_dict_of_services


def get_address_from_string(string_message):
    return string_message.split('|')[0].strip()


def get_standard_services_from_string(string_message: str):
    services = string_message.split('|')[1]
    services_list = services.split('+')
    standard_services = {}
    try:
        for service in services_list[0].strip().split(' '):
            key, value = service.split(':')
            standard_services[int(key)] = int(value)
    except ValueError:
        logger.error('Недостаточно значений для извлечения')
    return standard_services


def get_additional_services_from_string(string_message: str):
    # Обработка дополнительных услуги
    services = string_message.split('|')[1]
    services_list = services.split('+')[1:]
    additional_services = {}
    try:
        for index, service in enumerate(services_list):
            service_items = service.strip().split(':')
            service_info = {
                'service': service_items[0],
                'price': int(service_items[1]),
                'count': int(service_items[2])
            }
            additional_services[index + 1] = service_info
    except IndexError:
        logger.error(f'Неверно введена доп услуга: "{string_message}"')
    return additional_services





