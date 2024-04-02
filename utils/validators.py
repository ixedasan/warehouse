import re
from exceptions.custom_exceptions import SupplierAlreadyExistsError


def validate_product_name(name):
    if not isinstance(name, str) or len(name) < 3:
        raise ValueError("Назва товару має бути рядком довжиною не менше 3 символів")


def validate_product_quantity(quantity):
    if not isinstance(quantity, int) or quantity < 1:
        raise ValueError("Кількість товару має бути цілим числом більше 0")


def validate_product_price(price):
    if not isinstance(price, (int, float)) or price <= 0:
        raise ValueError("Ціна товару має бути числом більше 0")


def validate_supplier_name(name, suppliers):
    if not isinstance(name, str) or len(name) < 3:
        raise ValueError("Назва постачальника має бути рядком довжиною не менше 3 символів")
    if any(s.name == name for s in suppliers):
        raise SupplierAlreadyExistsError("Постачальник з такою назвою вже існує")


def validate_supplier_contact_info(contact_info):
    if not isinstance(contact_info, str) or (not is_valid_email(contact_info) and not is_valid_phone(contact_info)):
        raise ValueError("Некоректний формат контактної інформації")


def is_valid_email(email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return bool(re.match(email_regex, email))


def is_valid_phone(phone):
    phone_regex = r'^\+?\d{1,3}?[\s-]?\(?\d{3}?\)?[\s-]?\d{3}[\s-]?\d{4}$'
    return bool(re.match(phone_regex, phone))