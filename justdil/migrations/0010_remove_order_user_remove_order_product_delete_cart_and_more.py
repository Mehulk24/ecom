# Generated by Django 5.1.5 on 2025-03-25 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('justdil', '0009_n_users_is_active_n_users_is_admin_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='N_Users',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
