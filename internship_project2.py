import mysql.connector
from datetime import datetime

class Database:
    def __init__(self, host="localhost", user="root", password="password", database="inventory_db"):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

class Product:
    def __init__(self, db):
        self.db = db

    def add_product(self, name, description, price, stock_quantity, reorder_level):
        query = '''
            INSERT INTO products (name, description, price, stock_quantity, reorder_level)
            VALUES (%s, %s, %s, %s, %s)
        '''
        self.db.cursor.execute(query, (name, description, price, stock_quantity, reorder_level))
        self.db.conn.commit()

    def update_product(self, product_id, stock_quantity):
        query = '''
            UPDATE products
            SET stock_quantity = %s
            WHERE product_id = %s
        '''
        self.db.cursor.execute(query, (stock_quantity, product_id))
        self.db.conn.commit()

    def delete_product(self, product_id):
        query = '''
            DELETE FROM products
            WHERE product_id = %s
        '''
        self.db.cursor.execute(query, (product_id,))
        self.db.conn.commit()

    def view_products(self):
        query = '''
            SELECT * FROM products
        '''
        self.db.cursor.execute(query)
        return self.db.cursor.fetchall()

    def check_reorder(self):
        query = '''
            SELECT product_id, name, stock_quantity, reorder_level FROM products
        '''
        self.db.cursor.execute(query)
        products = self.db.cursor.fetchall()
        reorder_needed = []
        for product in products:
            if product[2] <= product[3]:
                reorder_needed.append((product[1], product[2], product[3]))
        return reorder_needed


class Supplier:
    def __init__(self, db):
        self.db = db

    def add_supplier(self, name, contact_info):
        query = '''
            INSERT INTO suppliers (name, contact_info)
            VALUES (%s, %s)
        '''
        self.db.cursor.execute(query, (name, contact_info))
        self.db.conn.commit()

    def view_suppliers(self):
        query = '''
            SELECT * FROM suppliers
        '''
        self.db.cursor.execute(query)
        return self.db.cursor.fetchall()

    def place_order(self, supplier_id, product_id, quantity):
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = '''
            INSERT INTO orders (supplier_id, product_id, quantity, order_date)
            VALUES (%s, %s, %s, %s)
        '''
        self.db.cursor.execute(query, (supplier_id, product_id, quantity, order_date))
        self.db.conn.commit()


class Inventory:
    def __init__(self, db):
        self.db = db
        self.product_manager = Product(db)
        self.supplier_manager = Supplier(db)

    def add_product(self, name, description, price, stock_quantity, reorder_level):
        self.product_manager.add_product(name, description, price, stock_quantity, reorder_level)

    def update_product(self, product_id, stock_quantity):
        self.product_manager.update_product(product_id, stock_quantity)

    def delete_product(self, product_id):
        self.product_manager.delete_product(product_id)

    def view_inventory(self):
        return self.product_manager.view_products()

    def add_supplier(self, name, contact_info):
        self.supplier_manager.add_supplier(name, contact_info)

    def view_suppliers(self):
        return self.supplier_manager.view_suppliers()

    def place_order(self, supplier_id, product_id, quantity):
        self.supplier_manager.place_order(supplier_id, product_id, quantity)

    def generate_reports(self):
        products = self.product_manager.view_products()
        return [{"name": p[1], "stock": p[4], "reorder_level": p[5]} for p in products]


# Example Usage
db = Database(host="localhost", user="root", password="Supandi$21", database="inventory_db")
inventory = Inventory(db)

# Adding products
inventory.add_product(name="Product A", description="Description A", price=10.0, stock_quantity=50, reorder_level=10)
inventory.add_product(name="Product B", description="Description B", price=15.0, stock_quantity=30, reorder_level=5)

# Adding supplier
inventory.add_supplier(name="Supplier A", contact_info="contact@suppliera.com")

# View inventory and suppliers
print("Inventory:")
for product in inventory.view_inventory():
    print(product)

print("\nSuppliers:")
for supplier in inventory.view_suppliers():
    print(supplier)

# Place an order from Supplier A
inventory.place_order(supplier_id=1, product_id=1, quantity=20)

# Update product stock level
inventory.update_product(product_id=1, stock_quantity=70)

# Check products that need reorder
print("\nReorder Check for Products:")
reorders = inventory.product_manager.check_reorder()
for product in reorders:
    print(f"Product {product[0]} needs reorder. Current stock: {product[1]}, Reorder level: {product[2]}")

# Generate report
print("\nInventory Report:")
print(inventory.generate_reports())

# Close database connection
db.close()
