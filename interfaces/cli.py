from entities import Product, Supplier, Transaction
from utils import validate_supplier_contact_info, validate_supplier_name


def show_menu():
    print("\nМеню:")
    print("1. Додати товар(постачальнику)")
    print("2. Видалити товар(у постачальника)")
    print("3. Оновити інформацію про товар(у постачальника)")
    print("4. Переглянути список товарів на складі")
    print("5. Додати постачальника")
    print("6. Видалити постачальника")
    print("7. Переглянути список постачальників")
    print("8. Переглянути товари постачальника")
    print("9. Додати операцію отримання")
    print("10. Додати операцію відвантаження")
    print("11. Переглянути історію операцій")
    print("0. Вихід")


def get_user_choice():
    choice = input("Введіть номер операції: ")
    return choice


def add_product(warehouse):
    name = input("Введіть назву товару: ")
    try:
        quantity = int(input("Введіть кількість товару: "))
        price = float(input("Введіть ціну товару: "))
        supplier = select_supplier(warehouse)
        if supplier:
            product = Product(name, quantity, price, supplier)
            supplier.add_product(product)
            print(f"Товар '{product.name}' успішно доданий до списку товарів постачальника '{supplier.name}'.")
    except ValueError as e:
        print(f"Помилка: {e}")


def remove_product(warehouse):
    if not warehouse.suppliers:
        print("Немає постачальників у базі даних.")
        return

    supplier = select_supplier(warehouse)
    if supplier:
        product = select_product(supplier.products)
        if product:
            try:
                supplier.remove_product(product)
            except ValueError as e:
                print(f"Помилка: {e}")


def update_product(warehouse):
    if not warehouse.suppliers:
        print("Немає постачальників у базі даних.")
        return

    supplier = select_supplier(warehouse)
    if supplier:
        product = select_product(supplier.products)
        if product:
            try:
                new_quantity = int(input("Введіть нову кількість товару: "))
                new_price = float(input("Введіть нову ціну товару: "))
                new_name = input("Введіть нову назву товару (або натисніть Enter, якщо не хочете змінювати назву): ")
                supplier.update_product(product, new_quantity, new_price, new_name if new_name else None)
            except ValueError as e:
                print(f"Помилка: {e}")


def view_products(warehouse):
    sort_option = input("Введіть критерій сортування (name, quantity, price, нічого для відсутності сортування): ")
    products = warehouse.get_products(sort_by=sort_option if sort_option else None)
    if not products:
        print("На складі немає товарів.")
    else:
        print("Список товарів на складі:")
        for product in products:
            print(f"{product.name} - Кількість: {product.quantity}, Ціна: {product.price}, Постачальник: {product.supplier.name}")


def add_supplier(warehouse):
    name = input("Введіть назву постачальника: ")
    contact_info = input("Введіть контактну інформацію постачальника (електронна адреса або номер телефону): ")

    try:
        supplier = Supplier(name, contact_info, warehouse)
        print(f"Постачальник '{supplier.name}' успішно доданий.")
    except ValueError as e:
        print(f"Помилка: {e}")


def remove_supplier(warehouse):
    supplier = select_supplier(warehouse)
    if supplier:
        warehouse.remove_supplier(supplier)
        print(f"Постачальник '{supplier.name}' успішно видалений.")


def view_suppliers(warehouse):
    suppliers = warehouse.get_suppliers()
    if not suppliers:
        print("Немає постачальників у базі даних.")
    else:
        print("Список постачальників:")
        for supplier in suppliers:
            print(supplier)


def view_supplier_products(warehouse):
    supplier = select_supplier(warehouse)
    if supplier:
        products = warehouse.get_supplier_products(supplier)
        if not products:
            print(f"Немає товарів від постачальника '{supplier.name}' на складі.")
        else:
            print(f"Товари від постачальника '{supplier.name}':")
            for product in products:
                print(f"{product.name} - Кількість: {product.quantity}, Ціна: {product.price}")


def add_receiving_transaction(warehouse):
    supplier = select_supplier(warehouse)
    if supplier:
        product = select_product(supplier.products)
        if product:
            try:
                quantity = int(input("Введіть кількість товару: "))
                warehouse.receive_product(product, quantity)
            except ValueError as e:
                print(f"Помилка: {e}")
        else:
            print("Товар не знайдено у постачальника.")


def add_shipping_transaction(warehouse):
    product = select_product(warehouse.products)
    if product:
        try:
            quantity = int(input("Введіть кількість товару: "))
            if product.quantity < quantity:
                print(f"Недостатня кількість товару'{product.name}' на складі.")
                return
            transaction = Transaction("Відвантаження", product, quantity)
            warehouse.add_transaction(transaction)
            product.quantity -= quantity
            print(f"Операція '{transaction}' успішно додана.")
        except ValueError as e:
            print(f"Помилка: {e}")


def view_transactions(warehouse):
    valid_sort_options = ["date", "product", "quantity", "operation"]
    sort_option = input("Введіть критерій сортування (date, product, quantity, operation, нічого для відсутності сортування): ")
    if sort_option and sort_option not in valid_sort_options:
        print("Некоректний критерій сортування.")
        return

    transactions = warehouse.get_transactions(sort_by=sort_option if sort_option else None)
    if not transactions:
        print("Немає операцій у базі даних.")
    else:
        print("Історія операцій:")
        for transaction in transactions:
            print(transaction)


def select_supplier(warehouse, message=None):
    if not warehouse.suppliers:
        print("Немає постачальників у базі даних.")
        return None
    if message:
        print(message)
    for i, supplier in enumerate(warehouse.suppliers, start=1):
        print(f"{i}. {supplier.name}")

    while True:
        choice = input("Введіть номер постачальника: ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(warehouse.suppliers):
                return warehouse.suppliers[index]
            else:
                print("Некоректний номер постачальника.")
        except ValueError:
            print("Некоректний ввід.")


def select_product(products):
    if not products:
        print("Немає товарів.")
        return None
    print("Список товарів:")
    for i, product in enumerate(products, start=1):
        print(f"{i}. {product.name} - Кількість: {product.quantity}, Ціна: {product.price}, Постачальник: {product.supplier.name}")
    while True:
        choice = input("Введіть номер товару: ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(products):
                return products[index]
            else:
                print("Некоректний номер товару.")
        except ValueError:
            print("Некоректний ввід.")


def run_cli(warehouse):
    while True:
        try:
            show_menu()
            choice = get_user_choice()

            if choice == "1":
                add_product(warehouse)
            elif choice == "2":
                remove_product(warehouse)
            elif choice == "3":
                update_product(warehouse)
            elif choice == "4":
                view_products(warehouse)
            elif choice == "5":
                add_supplier(warehouse)
            elif choice == "6":
                remove_supplier(warehouse)
            elif choice == "7":
                view_suppliers(warehouse)
            elif choice == "8":
                view_supplier_products(warehouse)
            elif choice == "9":
                add_receiving_transaction(warehouse)
            elif choice == "10":
                add_shipping_transaction(warehouse)
            elif choice == "11":
                view_transactions(warehouse)
            elif choice == "0":
                break
            else:
                print("Невірний вибір. Спробуйте ще раз.")
        except Exception as e:
            print(f"Сталася помилка: {e}")