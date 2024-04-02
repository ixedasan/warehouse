import datetime


class Transaction:
    def __init__(self, operation_type, product, quantity, supplier=None):
        self.date = datetime.date.today().isoformat()
        self.operation_type = operation_type
        self.product_name = product.name
        self.quantity = quantity
        self.supplier = supplier.name if supplier else None

    def __str__(self):
        return f"{self.date} - {self.operation_type} - {self.product_name} - Кількість: {self.quantity} - Постачальник: {self.supplier}"