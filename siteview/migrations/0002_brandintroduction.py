# Generated by Django 3.1.4 on 2021-02-04 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteview', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandIntroduction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Brand', models.CharField(max_length=250, verbose_name='Title')),
                ('image', models.ImageField(upload_to='siteview/slide_show/images', verbose_name='Background image')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Create at')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Update at')),
                ('action_url', models.URLField(verbose_name='Action url')),
            ],
        ),
    ]
