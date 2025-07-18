# Generated by Django 5.1.5 on 2025-04-08 18:03

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('justdil', '0014_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]
