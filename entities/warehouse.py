from entities.transaction import Transaction
from entities.product import Product


class Warehouse:
    def __init__(self, name):
        self.name = name
        self.products = []
        self.suppliers = []
        self.transactions = []

    def add_product(self, product):
        self.products.append(product)
        product.warehouse = self

    def remove_product(self, product):
        self.products.remove(product)
        
    def get_products(self, sort_by=None):
        filtered_products = self.products[:]
        if sort_by:
            filtered_products.sort(key=lambda p: getattr(p, sort_by))
        return filtered_products

    def add_supplier(self, supplier):
        self.suppliers.append(supplier)

    def remove_supplier(self, supplier):
        self.suppliers.remove(supplier)
        products_to_remove = [p for p in self.products if p.supplier == supplier]
        for product in products_to_remove:
            self.remove_product(product)

    def get_suppliers(self):
        return self.suppliers

    def get_supplier_products(self, supplier):
        return [product for product in supplier.products]

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_transactions(self, sort_by=None):
        transactions = self.transactions[:]
        if sort_by:
            if sort_by == "operation":
                transactions.sort(key=lambda t: t.operation_type)
            else:
                transactions.sort(key=lambda t: getattr(t, sort_by))
        return transactions

    def receive_product(self, product, quantity):
        """
        Метод для отримання товару від постачальника.
        """
        try:
            product.supplier.update_product_quantity(product, quantity)
        except ValueError as e:
            print(f"Помилка: {e}")
            return

        found = False
        for p in self.products:
            if p.name == product.name and p.supplier == product.supplier:
                p.quantity += quantity
                found = True
                break

        if not found:
            new_product = Product(product.name, quantity, product.price, product.supplier)
            self.add_product(new_product)
        else:
            print(f"Товар '{product.name}' від постачальника '{product.supplier.name}' вже існує на складі. Кількість оновлено.")

        transaction = Transaction("Отримання", product, quantity, product.supplier)
        self.add_transaction(transaction)
        print(f"Операція '{transaction}' успішно додана.")
