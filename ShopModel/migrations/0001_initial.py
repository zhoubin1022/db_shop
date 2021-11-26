# Generated by Django 3.2.7 on 2021-11-06 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('g_id', models.AutoField(primary_key=True, serialize=False)),
                ('g_name', models.CharField(max_length=20)),
                ('kind', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('s_id', models.AutoField(primary_key=True, serialize=False)),
                ('s_name', models.CharField(max_length=15)),
                ('s_password', models.CharField(max_length=20)),
                ('s_tel', models.CharField(max_length=11)),
                ('s_addr', models.TextField(max_length=100)),
                ('s_icon', models.ImageField(default='default_photo.png', upload_to='photos')),
                ('sales', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('u_id', models.AutoField(primary_key=True, serialize=False)),
                ('u_name', models.CharField(max_length=15)),
                ('u_password', models.CharField(max_length=20)),
                ('u_tel', models.CharField(max_length=11)),
                ('u_addr', models.TextField(max_length=100)),
                ('u_icon', models.ImageField(default='default_photo.png', upload_to='photos')),
                ('money', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='StoreHouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0.0)),
                ('amount', models.IntegerField(default=0)),
                ('img', models.ImageField(default='default_goods.png', upload_to='image')),
                ('info', models.TextField(max_length=100)),
                ('sales', models.IntegerField(default=0)),
                ('g_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopModel.goods')),
                ('s_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopModel.store')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('g_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopModel.goods')),
                ('s_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopModel.store')),
                ('u_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopModel.user')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopModel.store')),
                ('u_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopModel.user')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('g_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopModel.goods')),
                ('s_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopModel.store')),
                ('u_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopModel.user')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('g_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopModel.goods')),
                ('s_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopModel.store')),
                ('u_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopModel.user')),
            ],
        ),
    ]
