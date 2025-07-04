import os
import django
from decimal import Decimal
import random
from datetime import datetime, timedelta

# Set up Django environment
# Replace 'alx_backend_graphql.settings' with your actual project settings module
# (e.g., 'your_project_name.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')
django.setup()

# Import your models after Django setup
from crm.models import Customer, Product, Order

def seed_database():
    """
    Populates the database with sample Customer, Product, and Order data.
    """
    print("--- Starting database seeding ---")

    # --- 1. Clear existing data (optional, uncomment if you want to clear) ---
    print("Clearing existing data...")
    Order.objects.all().delete()
    Product.objects.all().delete()
    Customer.objects.all().delete()
    print("Existing data cleared.")

    # --- 2. Create Sample Customers ---
    print("\nCreating sample customers...")
    customers_data = [
        {'name': 'Alice Wonderland', 'email': 'alice@example.com', 'phone': '123-456-7890'},
        {'name': 'Bob The Builder', 'email': 'bob@example.com', 'phone': '987-654-3210'},
        {'name': 'Charlie Chaplin', 'email': 'charlie@example.com', 'phone': '555-123-4567'},
        {'name': 'Diana Prince', 'email': 'diana@example.com', 'phone': '111-222-3333'},
        {'name': 'Eve Harrington', 'email': 'eve@example.com', 'phone': None}, # Test optional phone
    ]
    
    created_customers = []
    for data in customers_data:
        customer, created = Customer.objects.get_or_create(email=data['email'], defaults=data)
        created_customers.append(customer)
        if created:
            print(f"Created Customer: {customer.name} ({customer.email})")
        else:
            print(f"Customer already exists: {customer.name} ({customer.email})")

    # --- 3. Create Sample Products ---
    print("\nCreating sample products...")
    products_data = [
        {'name': 'Laptop Pro', 'price': Decimal('1200.00'), 'stock': 50},
        {'name': 'Wireless Mouse', 'price': Decimal('25.50'), 'stock': 200},
        {'name': 'Mechanical Keyboard', 'price': Decimal('75.99'), 'stock': 100},
        {'name': 'USB-C Hub', 'price': Decimal('30.00'), 'stock': 150},
        {'name': 'External SSD 1TB', 'price': Decimal('99.99'), 'stock': 75},
    ]

    created_products = []
    for data in products_data:
        product, created = Product.objects.get_or_create(name=data['name'], defaults=data)
        created_products.append(product)
        if created:
            print(f"Created Product: {product.name} (Price: {product.price}, Stock: {product.stock})")
        else:
            print(f"Product already exists: {product.name}")

    # --- 4. Create Sample Orders ---
    print("\nCreating sample orders...")
    if created_customers and created_products:
        # Order 1: Alice buys Laptop Pro and Wireless Mouse
        order1 = Order.objects.create(customer=created_customers[0])
        order1.products.set([created_products[0], created_products[1]])
        print(f"Created Order #{order1.id} for {order1.customer.name} with products: "
              f"{[p.name for p in order1.products.all()]}")

        # Order 2: Bob buys Mechanical Keyboard and USB-C Hub
        order2 = Order.objects.create(customer=created_customers[1])
        order2.products.set([created_products[2], created_products[3]])
        print(f"Created Order #{order2.id} for {order2.customer.name} with products: "
              f"{[p.name for p in order2.products.all()]}")

        # Order 3: Charlie buys External SSD
        order3 = Order.objects.create(customer=created_customers[2])
        order3.products.set([created_products[4]])
        print(f"Created Order #{order3.id} for {order3.customer.name} with products: "
              f"{[p.name for p in order3.products.all()]}")

        # Order 4: Diana buys multiple of various products
        order4 = Order.objects.create(customer=created_customers[3])
        # Randomly select a few products
        random_products_for_order = random.sample(created_products, k=random.randint(1, len(created_products)))
        order4.products.set(random_products_for_order)
        print(f"Created Order #{order4.id} for {order4.customer.name} with products: "
              f"{[p.name for p in order4.products.all()]}")

    else:
        print("Not enough customers or products to create orders.")

    print("\n--- Database seeding complete ---")

if __name__ == '__main__':
    seed_database()

