import graphene
from graphene_django import DjangoObjectType
from crm.models import Product

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass  # ما فيش مدخلات

    success = graphene.String()
    products = graphene.List(ProductType)

    @classmethod
    def mutate(cls, root, info):
        low_stock = Product.objects.filter(stock__lt=10)
        updated_products = []
        for product in low_stock:
            product.stock += 10
            product.save()
            updated_products.append(product)

        return UpdateLowStockProducts(
            success="Low stock products updated successfully!",
            products=updated_products,
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

schema = graphene.Schema(mutation=Mutation)
INSTALLED_APPS = [
    # ...
    "django_crontab",
    "django_celery_beat",
]


CRONJOBS = [
    ('0 */12 * * *', 'crm.cron.update_low_stock'),
]


from celery import crontab

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generate_crm_report',
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),
    },
}
