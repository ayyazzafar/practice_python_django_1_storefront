from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Customer, Collection, Order, OrderItem
from django.db.models import Count
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType


def say_hello(request):
    queryresult = Product.objects.all()
    return render(request, 'hello.html', {'name': 'Mosh', 'result':   list(queryresult)})
