# Generated by Django 5.0.4 on 2024-04-08 07:50

import django.db.models.deletion
import payments.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('buyer', models.EmailField(max_length=254)),
                ('price', models.IntegerField()),
                ('purchased', models.DateTimeField(verbose_name='date of purchase')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=128)),
                ('amount', models.IntegerField()),
                ('expire', models.DateTimeField(default=payments.models.get_default_expire, verbose_name='payment is not accepted after')),
                ('is_paid', models.BooleanField(default=False)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='payments.order')),
            ],
        ),
    ]
