# Generated by Django 5.1.5 on 2025-05-21 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('justdil', '0040_alter_bestproduct_category_alter_newproduct_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bestproduct',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='bestproduct',
            name='j_type',
            field=models.CharField(blank=True, default='', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='newproduct',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='newproduct',
            name='j_type',
            field=models.CharField(blank=True, default='', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='product',
            name='j_type',
            field=models.CharField(blank=True, default='', max_length=10, null=True),
        ),
    ]
