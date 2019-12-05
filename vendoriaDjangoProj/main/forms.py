from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import DateField, DateInput, CharField, ModelChoiceField, Select
from .models import User, Customer, InventoryWorker, Manager, Manufacturer, Marketer, Shipper, Region


class CustomerRegistrationForm(UserCreationForm):
    dob = DateField(required=True, widget=DateInput(attrs={'placeholder': 'MM/DD/YYYY', 'required': 'required'}))
    address = CharField(max_length=35, strip=True)
    regions = Region.objects.all()
    region = ModelChoiceField(queryset=regions)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        print(self.cleaned_data)
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        dob = self.cleaned_data.get('dob')
        address = self.cleaned_data.get('address')
        region = self.cleaned_data.get('region')
        Customer.objects.create(user=user, DOB=dob, address=address, region=region)
        return user


class InventoryRegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_inventory_worker = True
        user.save()
        InventoryWorker.objects.create(user=user)
        return user


class ManagerRegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_manager = True
        user.save()
        Manager.objects.create(user=user)
        return user


class ManufacturerRegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_manufacturer = True
        user.save()
        Manufacturer.objects.create(user=user)
        return user


class MarketerRegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_marketer = True
        user.save()
        Marketer.objects.create(user=user)
        return user


class ShipperRegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_shipper = True
        user.save()
        Shipper.objects.create(user=user)
        return user

