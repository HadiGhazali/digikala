# Generated by Django 3.1.4 on 2020-12-31 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0002_auto_20201231_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Create at'),
        ),
        migrations.AlterField(
            model_name='product',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update at'),
        ),
    ]
