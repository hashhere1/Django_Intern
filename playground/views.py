from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, OrderItem, Customer
from django.db.models import F, Func, Value, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Count, Max, Min, Sum, Avg
from django.contrib.contenttypes.models import ContentType
from store.models import Order
from django.db import transaction




# Create your views here.

def say_hello(request):
    # collection = Collection()
    # collection.title = "Video Games"
    # collection.featured_product = Product(pk=1)
    # collection.save()

    # collection = Collection(pk=4)
    # collection.delete()

    # Collection.objects.filter(pk__gt=5).delete()
    # Collection.objects.filter(pk= 5).update(featured_product=None)  
    # with transaction.atomic():
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()

    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = 1
    #     item.quantity = 40
    #     item.unit_prize = 100

    #     item.save()

    query_set = Product.objects.raw('SELECT * FROM store_product')
    
    return render(request, "hello.html", {"name": "Hassaan", "Products": query_set})