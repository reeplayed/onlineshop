from django.db import models
from django.contrib.auth.models import User
from cart.models import Cart

class Address(models.Model):

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=120)
    email = models.EmailField(max_length=120)
    town = models.CharField(max_length=120)
    street = models.CharField(max_length=120)
    postcode = models.CharField(max_length=120)

    def __str__(self):
        return f'Address nr:{self.id}'


class Billing(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return f'Billing nr:{self.id}'
