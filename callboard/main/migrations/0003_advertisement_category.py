# Generated by Django 5.1.3 on 2024-11-08 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_advertisement_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='category',
            field=models.ManyToManyField(through='main.AdvertisementCategory', to='main.category'),
        ),
    ]
