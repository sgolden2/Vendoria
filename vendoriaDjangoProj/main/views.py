from django.shortcuts import render
from django.http import HttpResponse
from .models import Manufacturer, Shipper, Product


# Create your views here.
def homepage(request):
    return HttpResponse("This is some dope god damn <strong>TESTING</strong>.")


def manufacturers(request):
    return render(request,
                  'main/manufacturers.html',
                  context={"manus": Manufacturer.objects.all}
                  )


def shippers(request):
    return render(request,
                  'main/shippers.html',
                  context={"ships": Shipper.objects.all}
                  )


def products(request):
    return render(request,
                  'main/products.html',
                  context={"prods": Product.objects.all})


def login(request):
    return render(request,
                  'main/login.html')


def header(request):
    return render(request,
                  'main/header.html')