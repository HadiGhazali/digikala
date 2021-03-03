# Generated by Django 3.1.4 on 2021-03-03 18:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Products', '0013_userfavoriteproduct'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfavoriteproduct',
            unique_together={('product', 'user')},
        ),
    ]
