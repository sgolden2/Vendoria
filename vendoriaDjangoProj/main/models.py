from django.db import models
from datetime import date


# Create your models here.

# STRONG ENTITIES


class Customer(models.Model):
    fname = models.CharField(max_length=30)
    MI = models.CharField(max_length=1)
    lname = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    DOB = models.DateField()
    address = models.CharField(max_length=35)

    def __str__(self):
        return str(self.fname) + ' ' + str(self.MI) + ' ' + str(self.lname)


class Shipper(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.name)


class Region(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.name)


class Manufacturer(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.name)


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
    DOT = models.DateTimeField()
    amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    item_count = models.IntegerField()
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=4,
                                      choices=PAYMENT_TYPES,
                                      default=CARD)

    def __str__(self):
        return str(self.customer) + ' | ' + str(self.amount) + ' | ' + str(self.DOT)


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
    quantity = models.IntegerField()
    reorder_threshold = models.IntegerField()
    reorder_amount = models.IntegerField()
    max_amount = models.IntegerField()
    status = models.CharField(max_length=4,
                              choices=INVEN_STATUS,
                              default=OK)

    def __str__(self):
        return str(self.place) + ' | ' + str(self.product) + ' | ' + str(self.quantity) + '/' + str(self.max_amount) + ' -> ' + str(self.status)


# WEAK ENTITIES

class Cart(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product + 'IS MEMBER OF ' + self.purchase


class Contract(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    startdate = models.DateField(default=date.today)
    curr_total = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)

    def __str__(self):
        return 'Customer: ' + self.customer + ' | Current Total: ' + self.curr_total + '| Account Created On: ' + self.startdate


class Saved_Card(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=20),

    def __str__(self):
        return self.customer + ' | ' + self.card_number


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

    def __str__(self):
        if self.status == self.PROCESSED:
            return 'SHIPPER ' + self.shipper + ' HAS PROCESSED ORDER ' + self.purchase
        elif self.status == self.SHIPPED:
            return 'ORDER ' + self.purchase + 'IS ON THE WAY VIA ' + self.shipper
        elif self.status == self.DELIVERED:
            return 'SHIPPER ' + self.shipper + ' HAS DELIVERED ORDER ' + self.purchase


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

    def __str__(self):
        if self.status == self.PROCESSED:
            return 'SHIPPER ' + self.shipper + ' HAS PROCESSED REORDER OF ' + self.inventory
        elif self.status == self.SHIPPED:
            return 'REORDER OF ' + self.inventory + 'IS ON THE WAY VIA ' + self.shipper
        elif self.status == self.DELIVERED:
            return 'SHIPPER ' + self.shipper + ' HAS DELIVERED REORDER OF ' + self.inventory


class Makes(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.manufacturer) + ' makes ' + str(self.product)
