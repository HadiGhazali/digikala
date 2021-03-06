# Generated by Django 3.1.4 on 2021-02-05 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0005_auto_20210129_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_product_product', related_query_name='shop_product_product', to='Products.product', verbose_name='product'),
        ),
    ]
