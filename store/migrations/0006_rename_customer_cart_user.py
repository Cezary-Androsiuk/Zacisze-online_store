# Generated by Django 5.0 on 2023-12-13 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_cart_cartitem_cart_products'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='customer',
            new_name='user',
        ),
    ]
