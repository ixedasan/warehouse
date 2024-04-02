from entities.warehouse import Warehouse
from interfaces.cli import run_cli

def main():
    warehouse_name = input("Введіть назву складу: ")
    warehouse = Warehouse(warehouse_name)
    run_cli(warehouse)

if __name__ == "__main__":
    main()