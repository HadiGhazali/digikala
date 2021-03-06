# Generated by Django 3.1.4 on 2021-01-29 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0004_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_image', related_query_name='product_image', to='Products.product', verbose_name='product'),
        ),
    ]
