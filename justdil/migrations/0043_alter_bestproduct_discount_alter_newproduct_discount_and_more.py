# Generated by Django 5.1.5 on 2025-06-07 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('justdil', '0042_alter_bestproduct_discount_alter_newproduct_discount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bestproduct',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='newproduct',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
