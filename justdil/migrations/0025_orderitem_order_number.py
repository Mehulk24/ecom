# Generated by Django 5.1.5 on 2025-04-27 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('justdil', '0024_bestproduct_bestproductimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='order_number',
            field=models.CharField(default='', max_length=20),
        ),
    ]
