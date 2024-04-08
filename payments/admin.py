from django.contrib import admin
from django.forms import NumberInput
from django.db import models

from .models import Order, Payment


class OrderAdmin(admin.ModelAdmin):
    @admin.display(boolean=True)
    def is_paid(self, obj):
        return obj.is_paid()

    list_display = ["__str__", "buyer", "price", "purchased", "is_paid"]
    ordering = ["purchased"]

class PaymentAdmin(admin.ModelAdmin):
    @admin.action(description="Check received payments")
    def confirm(self, request, queryset):
        for obj in queryset:
            obj.confirm()

    list_display = ["__str__", "address", "amount", "is_paid"]
    actions = [confirm]


admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)

