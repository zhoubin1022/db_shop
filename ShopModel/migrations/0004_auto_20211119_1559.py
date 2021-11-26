# Generated by Django 3.2.7 on 2021-11-19 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopModel', '0003_alter_comment_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='record',
            name='pay',
            field=models.FloatField(default=0.0),
        ),
    ]