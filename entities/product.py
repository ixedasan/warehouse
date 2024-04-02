from utils.validators import validate_product_name, validate_product_quantity, validate_product_price


class Product:
    def __init__(self, name, quantity, price, supplier):
        validate_product_name(name)
        validate_product_quantity(quantity)
        validate_product_price(price)
        self.name = name
        self.quantity = quantity
        self.price = price
        self.supplier = supplier

    def get_supplier_quantity(self):
        """
        Повертає кількість товару, наявного у постачальника.
        """
        for product in self.supplier.products:
            if product.name == self.name:
                return product.quantity
        return 0