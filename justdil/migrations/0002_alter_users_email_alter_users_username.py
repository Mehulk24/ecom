# Generated by Django 5.1.5 on 2025-03-18 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('justdil', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
