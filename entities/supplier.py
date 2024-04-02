from utils.validators import validate_supplier_name, validate_supplier_contact_info
from exceptions.custom_exceptions import SupplierAlreadyExistsError


class Supplier:
    def __init__(self, name, contact_info, warehouse):
        validate_supplier_name(name, warehouse.suppliers)
        validate_supplier_contact_info(contact_info)
        self.name = name
        self.contact_info = contact_info
        self.products = []
        self.warehouse = warehouse
        warehouse.add_supplier(self)

    def __str__(self):
        return f"{self.name} - {self.contact_info}"

    def add_product(self, product):
        if product.name in [p.name for p in self.products]:
            raise ValueError(f"Товар '{product.name}' вже існує у списку товарів постачальника '{self.name}'.")
        self.products.append(product)

    def remove_product(self, product):
        if product not in self.products:
            raise ValueError(f"Товар '{product.name}' не знайдено у списку товарів постачальника '{self.name}'.")
        self.products.remove(product)
        print(f"Товар '{product.name}' успішно видалений у постачальника '{self.name}'.")

    def update_product(self, product, new_quantity, new_price, new_name=None):
        if product not in self.products:
            raise ValueError(f"Товар '{product.name}' не знайдено у списку товарів постачальника '{self.name}'.")

        product.quantity = new_quantity
        product.price = new_price
        if new_name:
            old_name = product.name
            product.name = new_name
            print(f"Назву товару '{old_name}' змінено на '{new_name}'.")
        else:
            print(f"Інформація про товар '{product.name}' успішно оновлена у постачальника '{self.name}'.")

    def update_product_quantity(self, product, quantity):
        """
        Метод для оновлення кількості товару у постачальника.
        При отриманні товару зменшуємо кількість товару у постачальника.
        """
        for p in self.products:
            if p.name == product.name:
                if p.quantity < quantity:
                    raise ValueError(f"У постачальника '{self.name}' недостатня кількість товару '{product.name}' для отримання.")
                p.quantity -= quantity
                return
        else:
            raise ValueError(f"Товар '{product.name}' не знайдено у списку товарів постачальника '{self.name}'.")