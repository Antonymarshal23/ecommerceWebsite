# Generated by Django 4.2.2 on 2023-08-14 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0014_alter_product_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='slug',
        ),
    ]
