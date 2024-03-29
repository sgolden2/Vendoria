from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_marketer = models.BooleanField(default=False)
    is_shipper = models.BooleanField(default=False)
    is_manufacturer = models.BooleanField(default=False)
    is_inventory_worker = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

# USER TYPES


class Marketer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return 'MARK ' + str(self.user.username)


class Shipper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return 'SHIP ' + str(self.user.username)


class Manufacturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return 'MANU ' + str(self.user.username)


class InventoryWorker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return 'INVN ' + str(self.user.username)


# NON-USER STRONG ENTITIES


class Region(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.name)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    DOB = models.DateField()
    address = models.CharField(max_length=35)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return 'CUST ' + str(self.user.username)


class Product(models.Model):
    model = models.CharField(max_length=20)
    price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    category = models.CharField(max_length=30)

    def __str__(self):
        return str(self.model)


class Place(models.Model):
    STORE = 'STOR'
    WAREHOUSE = 'WRHS'
    PLACE_TYPES = [
        (STORE, 'Store'),
        (WAREHOUSE, 'Warehouse'),
    ]

    name = models.CharField(max_length=30)
    type = models.CharField(max_length=4,
                            choices=PLACE_TYPES,
                            default=STORE)
    address = models.CharField(max_length=35)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name) + ' | ' + str(self.type) + ' in ' + str(self.region)


class Purchase(models.Model):
    CARD = 'CARD'
    CASH = 'CASH'
    CONTRACT = 'CONT'
    PAYMENT_TYPES = [
        (CARD, 'Card'),
        (CASH, 'Cash'),
        (CONTRACT, 'Contract'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    DOT = models.DateTimeField(default=datetime.now)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=4,
                                      choices=PAYMENT_TYPES,
                                      default=CARD)

    def __str__(self):
        return str(self.customer) + ' PURCHASED ' + str(self.product) + ' | $' + str(self.product.price) + ' | ' + str(self.DOT)


class Inventory(models.Model):
    LOW = 'LOW'
    OK = 'OK'
    FULL = 'FULL'
    INVEN_STATUS = [
        (LOW, 'LOW'),
        (OK, 'OK'),
        (FULL, 'FULL'),
    ]

    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    reorder_threshold = models.IntegerField(default=0)
    reorder_amount = models.IntegerField(default=0)
    max_amount = models.IntegerField(default=100)
    status = models.CharField(max_length=4,
                              choices=INVEN_STATUS,
                              default=OK)

    def __str__(self):
        return str(self.place) + ' | ' + str(self.product) + ' | ' + str(self.quantity) + '/' + str(self.max_amount) + ' -> ' + str(self.status)


# WEAK ENTITIES


class Contract(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    startdate = models.DateField(default=date.today)
    curr_total = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)


class Saved_Card(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=30)


class Ships_To(models.Model):
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.shipper + ' SHIPS TO ' + self.region


class Shipment(models.Model):
    PROCESSED = 'PRC'
    SHIPPED = 'OTW'
    DELIVERED = 'DEL'
    SHIPMENT_STATUS = [
        (PROCESSED, 'Processed'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
    ]

    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    status = models.CharField(max_length=3,
                              choices=SHIPMENT_STATUS,
                              default=PROCESSED)


class Reorder(models.Model):
    PROCESSED = 'PRC'
    SHIPPED = 'OTW'
    DELIVERED = 'DEL'
    REORDER_STATUS = [
        (PROCESSED, 'Processed'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
    ]

    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    status = models.CharField(max_length=3,
                              choices=REORDER_STATUS,
                              default=PROCESSED)


class Makes(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.manufacturer) + ' makes ' + str(self.product)


###  SIGNALS  ###


# this func gets called every time a new record shows up in the Purchase table
@receiver(post_save, sender=Purchase)
def purchase_made(sender, instance, **kwargs):
    inventory = Inventory.objects.get(place=instance.place, product=instance.product)
    inventory.quantity -= 1
    if inventory.quantity <= inventory.reorder_threshold and inventory.reorder_threshold > 0 and not Reorder.objects.filter(inventory=inventory):
        inventory.status = Inventory.LOW
        reorder = Reorder(shipper=inventory.place.shipper, inventory=inventory, status=Reorder.PROCESSED)
        reorder.save()
    elif inventory.quantity >= inventory.max_amount:
        inventory.status = Inventory.FULL
    else:
        inventory.status = Inventory.OK
    inventory.save()


@receiver(post_save, sender=Place)
def create_inventories_on_new_place(sender, instance, **kwargs):
    place = instance
    for product in Product.objects.all():
        inventory = Inventory(place=place, product=product)
        inventory.save()


@receiver(post_save, sender=Product)
def create_inventories_on_new_product(sender, instance, **kwargs):
    product = instance
    for place in Place.objects.all():
        inventory = Inventory(place=place, product=product)
        inventory.save()
