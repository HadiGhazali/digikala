# Generated by Django 3.1.4 on 2021-02-12 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0004_shop_satisfaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='satisfaction',
            field=models.PositiveIntegerField(blank=True, default=3.5, null=True, verbose_name='satisfaction'),
        ),
    ]
