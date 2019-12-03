from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Manufacturer, Shipper, Product
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


# Create your views here.
def homepage(request):
    return render(request,
                  'main/homepage.html')


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
    return render(request,
                  'main/header.html',
                  context={
                      "req": request
                  })
