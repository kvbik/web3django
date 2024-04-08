import datetime

from web3 import Web3

from django.conf import settings
from django.db import models
from django.utils import timezone

from . import contracts


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
        return f'{self.description} for ${self.price}'

def convert_price_to_amount(usd):
    rate = 3600 # usd per ether
    wei = Web3.to_wei('1', 'ether')
    amount = usd * wei / rate
    return str(int(amount))

def get_default_expire():
    return timezone.now() + datetime.timedelta(hours=1)

def get_decimal_amount_and_symbol(amount, token=None):
    if not token:
        symbol = 'ETH'
        decimal_amount = Web3.from_wei(amount, 'ether')
        return decimal_amount, symbol

    w3 = Web3(Web3.HTTPProvider(settings.INFURA_URL))
    erc20 = w3.eth.contract(token, abi=contracts.ERC20)
    symbol = erc20.functions.symbol().call()
    decimals = 10 ** erc20.functions.decimals().call()
    decimal_amount = amount / decimals
    return decimal_amount, symbol

def get_balance_of(address, token=None):
    w3 = Web3(Web3.HTTPProvider(settings.INFURA_URL))
    if not token:
        balance = w3.eth.get_balance(address)
        return balance

    erc20 = w3.eth.contract(token, abi=contracts.ERC20)
    balance = erc20.functions.balanceOf(address).call()
    return balance

class Payment(models.Model):
    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    token = models.CharField(max_length=128, blank=True, null=True)
    amount = models.CharField(max_length=200)
    expire = models.DateTimeField("payment is not accepted after", default=get_default_expire)
    is_paid = models.BooleanField(default=False)

    def confirm(self):
        amount = int(self.amount)
        balance = get_balance_of(self.address, self.token)
        if balance >= amount:
            self.is_paid = True
            self.save()

    def save(self, *args, **kwargs):
        amount = int(self.amount)
        if amount == -1:
            self.amount = convert_price_to_amount(self.order.price)
        super(Payment, self).save(*args, **kwargs)

    def __str__(self):
        amount = int(self.amount)
        decimal_amount, symbol = get_decimal_amount_and_symbol(amount, self.token)
        return f'{self.order} in {decimal_amount} {symbol.lower()}'

