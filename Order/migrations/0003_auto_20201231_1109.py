# Generated by Django 3.1.4 on 2020-12-31 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0003_auto_20201231_1034'),
        ('Order', '0002_auto_20201231_1034'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='Order',
            new_name='order',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='shop_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.shopproduct', verbose_name='Order Item'),
        ),
    ]