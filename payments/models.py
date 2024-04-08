import datetime

from web3 import Web3

from django.conf import settings
from django.db import models
from django.utils import timezone


class Order(models.Model):
    description = models.CharField(max_length=200)
    buyer = models.EmailField()
    price = models.IntegerField()
    purchased = models.DateTimeField("date of purchase")

    def pending_payments(self):
        now = timezone.now()
        return self.payments.filter(expire__gte=now)

    def is_paid(self):
        return self.payments.filter(is_paid=True).exists()

    def __str__(self):
        return '{} for ${}'.format(self.description, self.price)


def get_default_expire():
    return timezone.now() + datetime.timedelta(hours=1)

class Payment(models.Model):
    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    amount = models.IntegerField()
    expire = models.DateTimeField("payment is not accepted after", default=get_default_expire)
    is_paid = models.BooleanField(default=False)

    def confirm(self):
        w3 = Web3(Web3.HTTPProvider(settings.INFURA_URL))
        balance = w3.eth.get_balance(self.address)
        if balance >= self.amount:
            self.is_paid = True
            self.save()

    def __str__(self):
        decimal = Web3.from_wei(self.amount, 'ether')
        return '{} in {} ether'.format(self.order, decimal)

