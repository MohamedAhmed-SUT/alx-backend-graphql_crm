INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crm',  # التطبيق الجديد
    'graphene_django',  # مكتبة GraphQL
]

GRAPHENE = {
    "SCHEMA": "alx_backend_graphql_crm.schema.schema"
}
