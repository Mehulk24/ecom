# Generated by Django 5.1.5 on 2025-05-18 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('justdil', '0038_cart_m_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='size',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
