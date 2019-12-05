from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.generic import CreateView 
from .models import *
from .forms import CustomerRegistrationForm, InventoryRegistrationForm, ManufacturerRegistrationForm, \
    MarketerRegistrationForm, ManagerRegistrationForm, ShipperRegistrationForm

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


#def register(request):
#    if request.method == "POST":
#        form = UserCreationForm(request.POST)
#        if form.is_valid():
#            user = form.save()
#            username = form.cleaned_data.get('username')
#            messages.success(request, f"account created successfully: {username}")
#            login(request, user)
#            return redirect("main:homepage")
#        else:
#            for msg in form.error_messages:
#                messages.error(request, f"{msg}: {form.error_messages[msg]}")
#
#            return render(request=request,
#                          template_name="main/register.html",
#                          context={"form": form})
#
#    form = UserCreationForm
#    return render(request,
#                  'main/register.html',
#                  context={"form": form}
#                  )

def register(request):
    return render(request,
                  "main/register.html")



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


# USER SPECIFIC PAGES


def customer_page(request):
    customer = Customer.objects.get(user=request.user)
    return render(request,
                  'main/userpages/customer_page.html',
                  context={'products': Product.objects.all(),
                           'customer': customer,
                           'purchases': Purchase.objects.filter(customer=customer),
                           })


def marketer_page(request):
    return render(request,
                  'main/userpages/marketer_page.html')


def manufacturer_page(request):
    return render(request,
                  'main/userpages/manufacturer_page.html')


def inventory_page(request):
    return render(request,
                  'main/userpages/inventory_page.html')


def shipper_page(request):
    return render(request,
                  'main/userpages/shipper_page.html')


def manager_page(request):
    return render(request,
                  'main/userpages/manager_page.html')


class CustomerRegistrationView(CreateView):
    model = User
    form_class = CustomerRegistrationForm
    template_name = 'main/user_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main:homepage')


class MarketerRegistrationView(CreateView):
    model = User
    form_class = MarketerRegistrationForm
    template_name = 'main/user_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main:homepage')


class ManufacturerRegistrationView(CreateView):
    model = User
    form_class = ManufacturerRegistrationForm
    template_name = 'main/user_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main:homepage')


class InventoryRegistrationView(CreateView):
    model = User
    form_class = InventoryRegistrationForm
    template_name = 'main/user_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main:homepage')


class ShipperRegistrationView(CreateView):
    model = User
    form_class = ShipperRegistrationForm
    template_name = 'main/user_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main:homepage')


class ManagerRegistrationView(CreateView):
    model = User
    form_class = ManagerRegistrationForm
    template_name = 'main/user_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main:homepage')

