# Generated by Django 3.1.4 on 2021-03-03 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Products', '0012_auto_20210303_1746'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFavoriteProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favorite_product_product', related_query_name='user_favorite_product_product', to='Products.product', verbose_name='Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favorite_product_user', related_query_name='user_favorite_product_user', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
