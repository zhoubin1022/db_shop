# Generated by Django 3.2.7 on 2021-11-18 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopModel', '0002_auto_20211117_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.CharField(max_length=100),
        ),
    ]
