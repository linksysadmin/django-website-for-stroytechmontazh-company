import datetime
import random
import xml.etree.ElementTree as ET


def generate_xml(request, data):
    with open('yandex/services.yml', 'r') as file:
        xml_data = file.read()

    company_info = data['company_info']
    main_categories = data['main_categories']
    sub_categories = data['sub_categories']
    services = data['services']

    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # Распарсить XML
    root = ET.fromstring(xml_data)
    root.set('date', date)

    # Вставить нужные данные

    root.find('shop/name').text = company_info.name
    root.find('shop/company').text = f'ООО "{company_info.name}"'
    root.find('shop/url').text = request.build_absolute_uri('/')[:-1]
    root.find('shop/email').text = company_info.email
    categories = root.find('shop/categories')
    sets = root.find('shop/sets')
    offers = root.find('shop/offers')

    len_main_categories = 0
    for category in main_categories:
        cat = ET.SubElement(categories, 'category')
        cat.set('id', str(category.id))
        cat.text = category.title

        len_main_categories += 1

    for index, sub_category in enumerate(sub_categories, len_main_categories + 1):
        sub_cat = ET.SubElement(categories, 'category')
        sub_cat.set('id', str(index))
        sub_cat.set('parentId', str(sub_category.service_type.id))
        sub_cat.text = sub_category.name

    for service in services:
        set_ = ET.SubElement(sets, 'set')
        set_.set('id', f'set_{service.id}')
        name = ET.SubElement(set_, 'name')
        name.text = service.title
        url = ET.SubElement(set_, 'url')
        url.text = request.build_absolute_uri(service.get_absolute_url())

    for service in services:
        offer_element = ET.SubElement(offers, 'offer')
        offer_element.set('id', f'service_{service.id}')

        name = ET.SubElement(offer_element, 'name')
        name.text = service.title

        url = ET.SubElement(offer_element, 'url')
        url.text = request.build_absolute_uri(service.get_absolute_url())

        price = ET.SubElement(offer_element, 'price')
        price.set('from', 'true')
        # здесь может быть логика для определения цены
        price.text = str(service.price)

        currencyId = ET.SubElement(offer_element, 'currencyId')
        currencyId.text = "RUR"

        sales_notes = ET.SubElement(offer_element, 'sales_notes')
        # здесь может быть логика для определения условий продажи
        sales_notes.text = service.get_service_unit()

        categoryId = ET.SubElement(offer_element, 'categoryId')
        if service.sub_service_type:
            categoryId.text = str(service.sub_service_type.id)
        else:
            categoryId.text = str(service.service_type.id)

        set_ids = ET.SubElement(offer_element, 'set-ids')
        set_ids.text = str(f'set_{service.id}')

        picture = ET.SubElement(offer_element, 'picture')
        if service.image:
            picture.text = request.build_absolute_uri(service.image.url)
        else:
            picture.text = 'https://stroytechmontazh.ru/media/articles_images/m-services-base.webp'

        description = ET.SubElement(offer_element, 'description')
        description.text = f"{service.title}. {company_info.location}"

        adult = ET.SubElement(offer_element, 'adult')
        adult.text = 'false'

        expiry = ET.SubElement(offer_element, 'expiry')
        expiry.text = 'P5Y'

        # и так далее для остальных элементов

        rating = ET.SubElement(offer_element, 'param')
        rating.set('name', 'Рейтинг')
        rating.text = str(5.0)

        reviews = ET.SubElement(offer_element, 'param')
        reviews.set('name', 'Число отзывов')
        reviews.text = str(random.randint(1, 20))

        experience_years = ET.SubElement(offer_element, 'param')
        experience_years.set('name', 'Годы опыта')
        experience_years.text = str(17)

        region = ET.SubElement(offer_element, 'param')
        region.set('name', 'Регион')
        region.text = company_info.location

        conversion = ET.SubElement(offer_element, 'param')
        conversion.set('name', 'Конверсия')
        conversion.text = str(1.935)

        phone_link = ET.SubElement(offer_element, 'param')
        phone_link.set('name', 'Ссылка на телефон')
        phone_link.text = "https://stroytechmontazh.ru/#contact-section"
        # здесь можете задать ссылку на телефон, например phone_link.text = "tel:+79123456789"

        home_visit = ET.SubElement(offer_element, 'param')
        home_visit.set('name', 'Выезд на дом')
        home_visit.text = 'да'

        work_at_address = ET.SubElement(offer_element, 'param')
        work_at_address.set('name', 'Работа по адресу')
        work_at_address.text = 'да'

        remotely = ET.SubElement(offer_element, 'param')
        remotely.set('name', 'Выполняется удаленно')
        remotely.text = 'нет'

        brigade = ET.SubElement(offer_element, 'param')
        brigade.set('name', 'Бригада')
        brigade.text = 'да'

        agreement = ET.SubElement(offer_element, 'param')
        agreement.set('name', 'Работа по договору')
        agreement.text = 'да'

        cash = ET.SubElement(offer_element, 'param')
        cash.set('name', 'Наличный расчет')
        cash.text = 'да'

        cash = ET.SubElement(offer_element, 'param')
        cash.set('name', 'Наличный расчет')
        cash.text = 'да'

        cashless_payments = ET.SubElement(offer_element, 'param')
        cashless_payments.set('name', 'Безналичный расчет')
        cashless_payments.text = 'да'

    xml_string = ET.tostring(root, encoding='utf-8')
    return xml_string
