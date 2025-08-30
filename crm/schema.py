import graphene
from graphene_django.filter import DjangoFilterConnectionField
from .models import Customer, Product, Order
from .filters import CustomerFilter, ProductFilter, OrderFilter
from graphene_django import DjangoObjectType

# Types
class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        filterset_class = CustomerFilter
        interfaces = (graphene.relay.Node,)

class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        filterset_class = ProductFilter
        interfaces = (graphene.relay.Node,)

class OrderNode(DjangoObjectType):
    class Meta:
        model = Order
        filterset_class = OrderFilter
        interfaces = (graphene.relay.Node,)

# Query
class Query(graphene.ObjectType):
    all_customers = DjangoFilterConnectionField(CustomerNode, order_by=graphene.List(of_type=graphene.String))
    all_products = DjangoFilterConnectionField(ProductNode, order_by=graphene.List(of_type=graphene.String))
    all_orders = DjangoFilterConnectionField(OrderNode, order_by=graphene.List(of_type=graphene.String))

    def resolve_all_customers(self, info, order_by=None, **kwargs):
        qs = Customer.objects.all()
        if order_by:
            qs = qs.order_by(*order_by)
        return qs

    def resolve_all_products(self, info, order_by=None, **kwargs):
        qs = Product.objects.all()
        if order_by:
            qs = qs.order_by(*order_by)
        return qs

    def resolve_all_orders(self, info, order_by=None, **kwargs):
        qs = Order.objects.all()
        if order_by:
            qs = qs.order_by(*order_by)
        return qs
import graphene
from graphene_django import DjangoObjectType
from crm.models import Product   # <= لازم تكون كده

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")

class UpdateLowStockProducts(graphene.Mutation):
    # <= لازم يكون الاسم كده بالضبط
    class Arguments:
        pass

    success = graphene.String()
    products = graphene.List(ProductType)

    @classmethod
    def mutate(cls, root, info):
        low_stock = Product.objects.filter(stock__lt=10)
        updated_products = []
        for product in low_stock:
            product.stock += 10   # <= هنا يظهر الرقم 10
            product.save()
            updated_products.append(product)

        return UpdateLowStockProducts(
            success="Low stock products updated successfully!",
            products=updated_products,
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

schema = graphene.Schema(mutation=Mutation)
