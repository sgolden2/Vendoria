from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Manufacturer, Shipper, Product, Reorder
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


# Create your views here.


def homepage(request):
    return render(request,
                  'main/homepage.html')


def login_page(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            u = form.cleaned_data.get('username')
            p = form.cleaned_data.get('password')
            user = authenticate(username=u, password=p)
            if user is not None:
                login(request, user)
                messages.info(request, f"you've been logged in as {u}")
                return redirect("main:homepage")
            else:
                messages.error(request, "somethin's wrong with that username or password")
        else:
            messages.error(request, "somethin's wrong with that username or password")
    form = AuthenticationForm()
    return render(request,
                  "main/login.html",
                  context={'form': form})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"account created successfully: {username}")
            login(request, user)
            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request=request,
                          template_name="main/register.html",
                          context={"form": form})

    form = UserCreationForm
    return render(request,
                  'main/register.html',
                  context={"form": form}
                  )


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "logged out")
    return redirect("main:homepage")


def header(request):
    products = Product.objects.all()
    return render(request,
                  'main/customer_page.html'
                  )


# USER SPECIFIC PAGES


def customer_page(request):
    products = Product.objects.all()
    return render(request,
                   'main/userpages/customer_page.html',
                    context={"products": products})

def marketer_page(request):
    return render(request,
                  'main/userpages/marketer_page.html')


def manufacturer_page(request):
    products = Product.objects.all()
    reorders = Reorder.objects.filter(inventory__product__manufacturer__user=request.user)
    return render(request,
                  'main/userpages/manufacturer_page.html',
                  context={"reorders": reorders})


def inventory_page(request):
    return render(request,
                  'main/userpages/inventory_page.html')


def shipper_page(request):
    return render(request,
                  'main/userpages/shipper_page.html')


def manager_page(request):
    return render(request,
                  'main/userpages/manager_page.html')
