# Generated by Django 5.1.5 on 2025-05-13 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('justdil', '0035_cart_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
