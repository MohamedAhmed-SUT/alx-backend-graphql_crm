import re
import graphene
from graphene_django import DjangoObjectType
from django.db import transaction
from django.utils import timezone
from .models import Customer, Product, Order

# --------------------
# GraphQL Types
# --------------------
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone")

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "stock")

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "customer", "products", "total_amount", "order_date")

# --------------------
# Mutations
# --------------------
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        # Validate unique email
        if Customer.objects.filter(email=email).exists():
            raise Exception("Email already exists")

        # Validate phone format
        if phone and not re.match(r"^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{3}[-.\s]?\d{4}$", phone):
            raise Exception("Invalid phone format")

        customer = Customer.objects.create(name=name, email=email, phone=phone)
        return CreateCustomer(customer=customer, message="Customer created successfully")

class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(graphene.JSONString, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    @transaction.atomic
    def mutate(self, info, input):
        created_customers = []
        errors = []

        for data in input:
            try:
                name = data["name"]
                email = data["email"]
                phone = data.get("phone")

                if Customer.objects.filter(email=email).exists():
                    errors.append(f"Email already exists: {email}")
                    continue

                if phone and not re.match(r"^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{3}[-.\s]?\d{4}$", phone):
                    errors.append(f"Invalid phone format: {phone}")
                    continue

                cust = Customer(name=name, email=email, phone=phone)
                cust.save()
                created_customers.append(cust)

            except KeyError as e:
                errors.append(f"Missing field: {e}")

            except Exception as e:
                errors.append(str(e))

        return BulkCreateCustomers(customers=created_customers, errors=errors)

class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int()

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock=0):
        if price <= 0:
            raise Exception("Price must be positive")
        if stock < 0:
            raise Exception("Stock cannot be negative")

        product = Product.objects.create(name=name, price=price, stock=stock)
        return CreateProduct(product=product)

class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)
        order_date = graphene.DateTime()

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids, order_date=None):
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise Exception("Invalid customer ID")

        products = Product.objects.filter(pk__in=product_ids)
        if len(products) != len(product_ids):
            raise Exception("One or more product IDs are invalid")

        if not products:
            raise Exception("At least one product must be selected")

        order = Order.objects.create(
            customer=customer,
            order_date=order_date or timezone.now()
        )
        order.products.set(products)
        total = sum([p.price for p in products])
        order.total_amount = total
        order.save()

        return CreateOrder(order=order)

# --------------------
# Root Schema
# --------------------
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()

class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    products = graphene.List(ProductType)
    orders = graphene.List(OrderType)

    def resolve_customers(root, info):
        return Customer.objects.all()

    def resolve_products(root, info):
        return Product.objects.all()

    def resolve_orders(root, info):
        return Order.objects.all()
