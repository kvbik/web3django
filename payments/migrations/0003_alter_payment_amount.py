# Generated by Django 5.0.4 on 2024-04-08 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_payment_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.CharField(max_length=200),
        ),
    ]
