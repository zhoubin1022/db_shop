from django.db import models


class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    u_name = models.CharField(max_length=15)
    u_password = models.CharField(max_length=20)
    u_tel = models.CharField(max_length=11)
    u_addr = models.TextField(max_length=100)
    u_icon = models.ImageField(upload_to="photos", default="default_photo.png")
    money = models.FloatField(default=0.0)


class Store(models.Model):
    s_id = models.AutoField(primary_key=True)
    s_name = models.CharField(max_length=15)
    s_password = models.CharField(max_length=20)
    s_tel = models.CharField(max_length=11)
    s_addr = models.TextField(max_length=100)
    s_icon = models.ImageField(upload_to="photos", default="photos/default_photo.png")
    sales = models.FloatField(default=0.0)


class Goods(models.Model):
    g_id = models.AutoField(primary_key=True)
    g_name = models.CharField(max_length=20)
    kind = models.CharField(max_length=10)


class StoreHouse(models.Model):
    s_id = models.ForeignKey('Store', on_delete=models.CASCADE)
    g_id = models.ForeignKey('Goods', on_delete=models.CASCADE)
    price = models.FloatField(default=0.0)
    amount = models.IntegerField(default=0)
    img = models.ImageField(upload_to="image", default="image/default_goods.png")
    info = models.TextField(max_length=100)
    sales = models.IntegerField(default=0)


class Cart(models.Model):
    u_id = models.ForeignKey('User', on_delete=models.CASCADE)
    s_id = models.ForeignKey('Store', on_delete=models.CASCADE)
    g_id = models.ForeignKey('Goods', on_delete=models.CASCADE)
    amount = models.IntegerField()


class Record(models.Model):
    u_id = models.ForeignKey('User', on_delete=models.CASCADE)
    s_id = models.ForeignKey('Store', on_delete=models.CASCADE)
    g_id = models.ForeignKey('Goods', on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True, null=True)
    pay = models.FloatField(default=0.0)


class Comment(models.Model):
    u_id = models.ForeignKey('User', on_delete=models.CASCADE)
    s_id = models.ForeignKey('Store', on_delete=models.CASCADE)
    g_id = models.ForeignKey('Goods', on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)


class Favorite(models.Model):
    u_id = models.ForeignKey('User', on_delete=models.CASCADE)
    s_id = models.ForeignKey('Store', on_delete=models.CASCADE)
