from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import Form
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.generic import CreateView
from django.core.exceptions import ObjectDoesNotExist
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
    if not request.user.is_authenticated:
        return render(request,
                      "main/register.html")
    else:
        messages.error("Please logout before registering an account.")
        return redirect("main:homepage")


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
    if not request.user.is_authenticated or not request.user.is_customer:
        messages.error(request, "You do not have customer permissions!")
        return redirect("main:homepage")

    customer = Customer.objects.get(user=request.user)

    if request.method == "POST":
        product_id = int(request.POST.get('prod_id'))
        payment_method = request.POST.get('payment_method')
        if not payment_method:
            messages.error(request, "Your order could not be completed because you did not select a payment method.")
        else:
            product = Product.objects.get(pk=product_id)
            place = Place.objects.get(type=Place.WAREHOUSE, region=customer.region)
            inventory = Inventory.objects.get(product=product, place=place)
            if inventory.quantity > 0:
                purchase = Purchase(customer=customer,
                                    product=product,
                                    place=place)
                purchase.save()
                messages.success(request, f"Your order of {product} has been placed!")
            else:
                messages.error(request, f"Your order could not be completed, {product} is out of stock in your region.")

    try:
        customer_contract = Contract.objects.filter(customer=customer)
    except ObjectDoesNotExist:
        customer_contract = Contract.objects.none()
    saved_cards = Saved_Card.objects.filter(customer=customer)
    return render(request,
                  'main/userpages/customer_page.html',
                  context={'products': Product.objects.all(),
                           'customer': customer,
                           'purchases': Purchase.objects.filter(customer=customer).order_by('-DOT')[0:5],
                           'has_contract': bool(customer_contract),
                           'contract': customer_contract,
                           'saved_cards': saved_cards,
                           })


def contracts(request):
    if not request.user.is_authenticated or not request.user.is_customer:
        messages.error(request, "You do not have customer permissions!")
        return redirect("main:homepage")

    customer = Customer.objects.get(user=request.user)

    if request.method == "POST":
        pass

    try:
        customer_contract = Contract.objects.filter(customer=customer)
    except ObjectDoesNotExist:
        customer_contract = Contract.objects.none()
    has_contract = bool(customer_contract)
    return render(request,
                  'main/contracts.html',
                  context={'has_contract': has_contract,
                           'contract': customer_contract})


def cards(request):
    if not request.user.is_authenticated or not request.user.is_customer:
        messages.error(request, "You do not have customer permissions!")
        return redirect("main:homepage")

    customer = Customer.objects.get(user=request.user)

    if request.method == "POST":
        print(request.POST)
        card_num = request.POST.get('card_num')
        new_card = Saved_Card(customer=customer, card_number=card_num)
        new_card.save()

    saved_cards = Saved_Card.objects.filter(customer=customer)
    return render(request,
                  'main/cards.html',
                  context={'saved_cards': saved_cards})


def marketer_page(request):
    if request.user.is_authenticated:
        if request.user.is_marketer:
            return render(request,
                          'main/userpages/marketer_page.html')
    messages.error(request, "You do not have marketer permissions!")
    return redirect("main:homepage")


def manufacturer_page(request):
    if request.user.is_authenticated:
        if request.user.is_manufacturer:
            red = Reorder.objects.all()
            return render(request,
                          'main/userpages/manufacturer_page.html',
                           context={'red': red})
    messages.error(request, "You do not have manufacturer permissions!")
    return redirect("main:homepage")


def inventory_page(request):
    if request.user.is_authenticated:
        if request.user.is_inventory_worker:
            inventory = Inventory.objects.all()
            return render(request,
                          'main/userpages/inventory_page.html',
                           context={'inventory' : inventory})
    messages.error(request, "You do not have inventory permissions!")
    return redirect("main:homepage")


def shipper_page(request):
    if request.user.is_authenticated:
        if request.user.is_shipper:
            ships = Shipment.objects.all()
            print(ships)
            return render(request,
                          'main/userpages/shipper_page.html',
                           context={'ships': ships}
                           )
    messages.error(request, "You do not have shipper permissions!")
    return redirect("main:homepage")


def manager_page(request):
    if request.user.is_authenticated:
        if request.user.is_manager:
            return render(request,
                          'main/userpages/manager_page.html')

    messages.error(request, "You do not have manager permissions!")
    return redirect("main:homepage")


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

