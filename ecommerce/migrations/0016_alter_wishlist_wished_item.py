# Generated by Django 4.2.2 on 2023-08-14 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0015_remove_wishlist_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='wished_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecommerce.product'),
        ),
    ]
