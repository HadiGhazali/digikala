# Generated by Django 3.1.4 on 2021-02-09 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0006_auto_20210205_0856'),
        ('Order', '0003_auto_20201231_1109'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='basketitem',
            unique_together={('shop_product', 'basket')},
        ),
    ]
