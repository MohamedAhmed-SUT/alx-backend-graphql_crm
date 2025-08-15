import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql_crm.settings")
django.setup()

from crm.models import Customer, Product

# Seed Customers
Customer.objects.create(name="John Doe", email="john@example.com", phone="+1234567890")
Customer.objects.create(name="Jane Smith", email="jane@example.com", phone="123-456-7890")

# Seed Products
Product.objects.create(name="Phone", price=500.00, stock=5)
Product.objects.create(name="Tablet", price=300.00, stock=3)

print("Database seeded successfully.")
