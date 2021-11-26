"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from ShopModel import views
from shop.settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/login', views.user_login),
    path('user/register', views.user_register),
    path('user/rechange', views.rechange),
    path('store/login', views.store_login),
    path('store/register', views.store_register),
    path('store/addGood', views.addGood),
    path('store/getStoreGoods', views.getStoreGoods),
    path('store/addStoreGoods', views.addStoreGoods),
    path('goods/search', views.search),
    path('goods/goodInfo', views.goodInfo),
    path('store/star', views.starStore),
    path('store/unstar', views.unStarStore),
    path('store/starlist', views.starList),
    path('cart/add', views.addToCart),
    path('cart/delete', views.deleteFromCart),
    path('cart/getCart', views.getCart),
    path('buy/buyFromGoodInfo', views.buyFromGoodInfo),
    path('buy/buyFromCart', views.buyFromCart),
    path('getRecords', views.getRecords),
    path('getStoreRecord', views.getStoreRecord),
    path('comment', views.comment),
    path('getUserComments', views.getUserComments),
    path('getStoreComments', views.getStoreComments),
    re_path('^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT})
]
