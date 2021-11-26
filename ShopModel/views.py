import os

from django.core import serializers
from django.http import JsonResponse
from ShopModel.models import *
from shop import settings


# 用户登录
def user_login(request):
    if request.method == 'POST':
        u_id = int(request.POST.get('u_id'))
        password = str(request.POST.get('u_password'))
        users = User.objects.filter(pk=u_id)
        if not users:
            return JsonResponse({"message": '用户名不存在'})
        if users.first().u_password == password:
            result = {"message": 'success', "data": serializers.serialize('python', users)}
            return JsonResponse(result)
        else:
            return JsonResponse({"message": 'id或密码错误'})
    return JsonResponse({"message": 'wrong'})


# 用户注册
def user_register(request):
    if request.method == 'POST':
        username = str(request.POST.get('u_username'))
        password = str(request.POST.get('u_password'))
        password_confirm = str(request.POST.get('u_password_confirm'))
        address = str(request.POST.get('u_address'))
        tel = str(request.POST.get('u_tel'))
        users = User.objects.filter(u_name=username)
        if users:
            return JsonResponse({"message": '用户名已存在'})
        if password == password_confirm:
            new_user = User.objects.create(u_name=username, u_password=password, u_tel=tel, u_addr=address)
            new_user.save()
            users = User.objects.filter(u_name=username)
            result = {"message": 'success', "data": serializers.serialize('python', users)}
            return JsonResponse(result)
        else:
            return JsonResponse({"message": '两次密码输入不一致'})
    return JsonResponse({"message": 'wrong'})


# 商家登录
def store_login(request):
    if request.method == 'POST':
        s_id = int(request.POST.get('s_id'))
        password = str(request.POST.get('s_password'))
        stores = Store.objects.filter(pk=s_id)
        if not stores:
            return JsonResponse({"message": '店铺名不存在'})
        if stores.first().s_password == password:
            result = {"message": 'success', "data": serializers.serialize('python', stores)}
            return JsonResponse(result)
        else:
            return JsonResponse({"message": 'id或密码错误'})
    return JsonResponse({"message": 'wrong'})


# 商家注册
def store_register(request):
    if request.method == 'POST':
        username = str(request.POST.get('s_username'))
        password = str(request.POST.get('s_password'))
        password_confirm = str(request.POST.get('s_password_confirm'))
        address = str(request.POST.get('s_address'))
        tel = str(request.POST.get('s_tel'))
        stores = Store.objects.filter(s_name=username)
        if stores:
            return JsonResponse({"message": '店铺名已存在'})
        if password == password_confirm:
            new_store = Store.objects.create(s_name=username, s_password=password, s_tel=tel, s_addr=address)
            new_store.save()
            stores = Store.objects.filter(s_name=username)
            result = {"message": 'success', "data": serializers.serialize('python', stores)}
            return JsonResponse(result)
        else:
            return JsonResponse({"message": '两次密码输入不一致'})


# 搜索商品
def search(request):
    if request.method == 'POST':
        # print(request.POST.get('keyword'))
        keyword = str(request.POST.get('keyword'))
        price_sort = int(request.POST.get('price_sort'))  # 1降序 0升序 -1无
        sale_sort = int(request.POST.get('sale_sort'))  # 1降序 0升序 -1无
        low = float(request.POST.get('low'))  # 小于零表示无下限
        high = float(request.POST.get('high'))  # 小于零表示无上限
        print(keyword)
        g_ids = Goods.objects.filter(g_name__icontains=keyword).values('g_id')
        if not g_ids:
            return JsonResponse({"message": "暂无相关商品"})
        g_id_list = []
        for x in g_ids:
            g_id_list.append(int(x['g_id']))
        s_good = StoreHouse.objects.filter(g_id__in=g_id_list)
        if price_sort == 0:
            s_good = s_good.order_by('price')
        elif price_sort == 1:
            s_good = s_good.order_by('-price')

        if sale_sort == 0:
            s_good = s_good.order_by('sales')
        elif sale_sort == 1:
            s_good = s_good.order_by('-sales')

        if low >= 0:
            s_good = s_good.filter(price__gte=low)
        if high >= 0:
            s_good = s_good.filter(price__lte=high)

        if not s_good:
            return JsonResponse({"message": "暂无相关商品"})

        result = {"message": "success", "data": []}
        for x in s_good:
            try:
                good = Goods.objects.get(pk=x.g_id_id)
                store = Store.objects.get(pk=x.s_id_id)
            except:
                return JsonResponse({"message": "商品有误"})
            good = {"g_name": good.g_name, "g_id": x.g_id_id, "kind": good.kind, "price": x.price, "amount": x.amount,
                    "img": x.img.name, "info": x.info, "sales": x.sales, "store_name": store.s_name, "s_id": x.s_id_id}
            result['data'].append(good)
        return JsonResponse(result)
        '''goods = Goods.objects.filter(g_name__icontains=keyword)
        if not goods:
            return JsonResponse({"message": "暂无相关商品"})
        result = {"message": "success", "data": []}
        for good in goods:
            name = good.g_name
            kind = good.kind
            g_id = good.g_id
            stores = StoreHouse.objects.filter(g_id_id=g_id)
            for store in stores:
                store_name = Store.objects.get(s_id=store.s_id_id).s_name
                good = {"g_name": name, "kind": kind, "good": serializers.serialize('python', [store]),
                        "store_name": store_name}
                result['data'].append(good)
        return JsonResponse(result)'''
    return JsonResponse({"message": "请求方式错误"})


# 添加商品
def addGood(request):
    if request.method == 'POST':
        g_name = str(request.POST.get('g_name'))
        s_id = int(request.POST.get('s_id'))
        kind = str(request.POST.get('kind'))
        price = float(request.POST.get('price'))
        amount = int(request.POST.get('amount'))
        # img = request.POST.get('img')
        # print(img)
        img = request.FILES['img']
        info = request.POST.get('info')

        goods = Goods.objects.filter(g_name=g_name)
        g_id = -1
        if not goods:
            goods = Goods(g_name=g_name, kind=kind)
            goods.save()
            g_id = Goods.objects.get(g_name=g_name).g_id
        else:
            g_id = goods.first().g_id
        good = StoreHouse.objects.filter(g_id_id=g_id, s_id_id=s_id)
        if good:
            return JsonResponse({"message": '该商品已存在'})
        if img:  # 判断该照片之前是否接受过
            file_info, suffix = os.path.splitext(img.name)
            if suffix.upper() not in ['.JPG', '.JPEG', '.PNG']:
                return JsonResponse({"message": '图片格式不正确，只接受jpg、jpeg、png格式的图片'})
            path = os.path.join(settings.BASE_DIR, 'media')
            path = os.path.join(path, 'image')
            path = os.path.join(path, img.name)
            if os.path.exists(path):
                os.remove(path)
        new_good = StoreHouse(s_id_id=s_id, g_id_id=g_id, price=price, amount=amount, img=img, info=info)
        new_good.save()
        return JsonResponse({"message": "success",
                             "data": serializers.serialize('python',
                                                           StoreHouse.objects.filter(s_id_id=s_id, g_id_id=g_id))})
    return JsonResponse({"message": "请求方式错误"})


# 添加商品到购物车
def addToCart(request):
    if request.method == 'POST':
        u_id = int(request.POST.get('u_id'))
        s_id = int(request.POST.get('s_id'))
        g_id = int(request.POST.get('g_id'))
        amount = int(request.POST.get('amount'))
        if Cart.objects.filter(u_id_id=u_id, s_id_id=s_id, g_id_id=g_id):
            return JsonResponse({"message": "你在该商店还有同一商品的订单未支付，请在支付后再次加入订单！"})
        cart = Cart(u_id_id=u_id, s_id_id=s_id, g_id_id=g_id, amount=amount)
        cart.save()
        return JsonResponse({"message": "success", "data": {"u_id": cart.u_id_id, "s_id": cart.s_id_id,
                                                            "g_id": cart.g_id_id, "amount": cart.amount,
                                                            "c_id": cart.pk}})


# 将订单从购物车移除
def deleteFromCart(request):
    if request.method == 'POST':
        c_id = int(request.POST.get('c_id'))
        cart = Cart.objects.filter(pk=c_id)
        if not cart:
            return JsonResponse({"message": "该订单不存在"})
        cart.delete()
        return JsonResponse({"message": "success"})
    return JsonResponse({"message": "请求方式错误"})


# 收藏店铺
def starStore(request):
    if request.method == 'POST':
        u_id = int(request.POST.get('u_id'))
        s_id = int(request.POST.get('s_id'))
        print(u_id, s_id)
        if Favorite.objects.filter(u_id_id=u_id, s_id_id=s_id):
            return JsonResponse({"message": "已收藏"})
        new_favorite = Favorite(u_id_id=u_id, s_id_id=s_id)
        new_favorite.save()
        return JsonResponse({"message": "success"})
    return JsonResponse({"message": "wrong"})


# 取消收藏
def unStarStore(request):
    if request.method == 'POST':
        u_id = int(request.POST.get('u_id'))
        s_id = int(request.POST.get('s_id'))
        favorite = Favorite.objects.filter(u_id_id=u_id, s_id_id=s_id)
        if not favorite:
            return JsonResponse({"message": "暂未收藏"})
        favorite.delete()
        return JsonResponse({"message": "success"})
    return JsonResponse({"message": "wrong"})


# 收藏列表
def starList(request):
    if request.method == 'POST':
        result = {"message": "success", "data": []}
        u_id = int(request.POST.get('u_id'))
        favorite = Favorite.objects.filter(u_id_id=u_id)
        for x in favorite:
            s = Store.objects.get(pk=x.s_id_id)
            fav = {"s_id": s.pk, "s_name": s.s_name, "s_icon": s.s_icon.name}
            result['data'].append(fav)
        # result['data'] = serializers.serialize('python', result['data'])
        return JsonResponse(result)
    return JsonResponse({"message": "wrong"})


# 充值
def rechange(request):
    if request.method == 'POST':
        u_id = int(request.POST.get('u_id'))
        print(u_id)
        money = float(request.POST.get('money'))
        print(money)
        try:
            user = User.objects.get(pk=u_id)
        except:
            return JsonResponse({"message": "用户id错误"})
        user.money += money
        user.save()
        return JsonResponse({"message": "success", "data": serializers.serialize('python', [user])})
    return JsonResponse({"message": "请求方式错误"})


# 获取商品详情
def goodInfo(request):
    if request.method == 'POST':
        result = {"message": "success", "goodInfo": {}, "comment": [], "recommend": []}
        s_id = int(request.POST.get('s_id'))
        g_id = int(request.POST.get('g_id'))
        print(s_id, g_id)
        goods = StoreHouse.objects.filter(s_id_id=s_id, g_id_id=g_id)
        if not goods:
            return JsonResponse({"message": "未获取到商品信息"})
        good = goods.first()
        result['goodInfo'] = {"s_id": good.s_id_id, "g_id": good.g_id_id, "price": good.price,
                              "amount": good.amount, "img": good.img.name, "info": good.info,
                              "sales": good.sales, "g_name": Goods.objects.get(pk=good.g_id_id).g_name,
                              "s_name": Store.objects.get(pk=good.s_id_id).s_name}
        g_kind = Goods.objects.get(pk=g_id).kind
        goods = Goods.objects.filter(kind=g_kind)
        for good in goods:
            s_goods = StoreHouse.objects.filter(g_id_id=good.g_id)
            for s_good in s_goods:
                result['recommend'].append({"s_id": s_good.s_id_id, "g_id": s_good.g_id_id, "img": s_good.img.name,
                                            "g_name": Goods.objects.get(pk=s_good.g_id_id).g_name,
                                            "s_name": Store.objects.get(pk=s_good.s_id_id).s_name})
        comments = Comment.objects.filter(s_id_id=s_id, g_id_id=g_id).order_by('date')
        for x in comments:
            u_id = x.u_id_id
            one_comment = {"u_id": u_id, "u_name": User.objects.get(pk=u_id).u_name, "text": x.comment,
                           "date": x.date.strftime('%Y-%m-%d %H:%M:%S'), "img": User.objects.get(pk=u_id).u_icon.name}
            result['comment'].append(one_comment)
        return JsonResponse(result)
    return JsonResponse({"message": "请求方式错误"})


# 发布评论
def comment(request):
    if request.method == 'POST':
        u_id = int(request.POST.get('u_id'))
        s_id = int(request.POST.get('s_id'))
        g_id = int(request.POST.get('g_id'))
        user_comment = request.POST.get('user_comment')
        try:
            user = User.objects.get(pk=u_id)
        except:
            return JsonResponse({"message": "用户不存在"})
        try:
            goods = StoreHouse.objects.get(s_id_id=s_id, g_id_id=g_id)
        except:
            return JsonResponse({"message": "该商品不存在"})
        new_comment = Comment(u_id_id=u_id, s_id_id=s_id, g_id_id=g_id, comment=user_comment)
        new_comment.save()
        return JsonResponse({"message": "success", "data": {"u_id": u_id, "u_name": user.u_name, "text": user_comment,
                                                            "date": new_comment.date.strftime('%Y-%m-%d %H:%M:%S')}})
    return JsonResponse({"message": "请求方式错误"})


# 商品详情页购买商品
def buyFromGoodInfo(request):
    if request.method == 'POST':
        u_id = int(request.POST.get('u_id'))
        s_id = int(request.POST.get('s_id'))
        g_id = int(request.POST.get('g_id'))
        amount = int(request.POST.get('amount'))
        pay = float(request.POST.get('pay'))
        try:
            s_good = StoreHouse.objects.get(s_id_id=s_id, g_id_id=g_id)
            user = User.objects.get(pk=u_id)
            good = Goods.objects.get(pk=g_id)
            store = Store.objects.get(pk=s_id)
        except:
            return JsonResponse({"message": "传递的参数错误"})
        if s_good.amount < amount:
            return JsonResponse({"message": "该商品存量不足"})
        if user.money < pay:
            return JsonResponse({"message": "余额不足"})
        s_good.amount -= amount
        s_good.sales += amount
        s_good.save()
        user.money -= pay
        user.save()
        store.sales += pay
        store.save()
        new_record = Record(u_id_id=u_id, s_id_id=s_id, g_id_id=g_id, amount=amount, pay=pay)
        new_record.save()
        return JsonResponse({"message": "success", "data": serializers.serialize('python', [new_record])})
    return JsonResponse({"message": "请求方式错误"})


# 获取购买记录
def getRecords(request):
    if request.method == 'POST':
        result = {"message": "success", "data": []}
        u_id = int(request.POST.get('u_id'))
        records = Record.objects.filter(u_id_id=u_id)
        if not records:
            return JsonResponse({"message": "暂无购买记录"})
        for x in records:
            try:
                store = Store.objects.get(pk=x.s_id_id)
                good = Goods.objects.get(pk=x.g_id_id)
                s_good = StoreHouse.objects.get(s_id_id=x.s_id_id, g_id_id=x.g_id_id)
            except:
                return JsonResponse({"message": "记录存在问题"})
            record = {"pk": x.pk, "pay": x.pay, "date": x.date.strftime('%Y-%m-%d %H:%M:%S'), "amount": x.amount,
                      "s_name": store.s_name, "s_id": store.pk, "g_name": good.g_name, "g_id": good.pk,
                      "price": s_good.price, "img": s_good.img.name, "info": s_good.info}
            result['data'].append(record)
        return JsonResponse(result)
    return JsonResponse({"message": "请求方式错误"})


# 获取商家拥有的商品列表
def getStoreGoods(request):
    if request.method == 'POST':
        result = {"message": "success", "data": []}
        s_id = int(request.POST.get('s_id'))
        goods = StoreHouse.objects.filter(s_id_id=s_id)
        if not goods:
            return JsonResponse({"message": "暂无商品"})
        for x in goods:
            try:
                good = Goods.objects.get(pk=x.g_id_id)
            except:
                return JsonResponse({"message": "商品出错"})
            s_good = {"g_name": good.g_name, "kind": good.kind, "price": x.price, "g_id": x.g_id_id,
                      "amount": x.amount, "img": x.img.name, "info": x.info, "sales": x.sales}
            result['data'].append(s_good)
        return JsonResponse(result)
    return JsonResponse({"message": "请求方式错误"})


# 添加库存
def addStoreGoods(request):
    if request.method == 'POST':
        result = {"message": "success", "data": []}
        s_id = int(request.POST.get('s_id'))
        g_id = int(request.POST.get('g_id'))
        amount = int(request.POST.get('amount'))
        try:
            good = StoreHouse.objects.get(s_id_id=s_id, g_id_id=g_id)
        except:
            return JsonResponse({"message": "商品不存在"})
        good.amount += amount
        good.save()
        result['data'] = serializers.serialize('python', [good])
        return JsonResponse(result)
    return JsonResponse({"message": "请求方式错误"})


# 从购物车购买商品
def buyFromCart(request):
    if request.method == 'POST':
        res = request.POST.get('c_id')
        res = str(res).split(',')
        cart = []
        for x in res:
            cart.append(int(x))
        # cart = json.loads(res)
        print(cart)
        # print(cart)
        # return JsonResponse({"message": "test"})
        now_pay = round(0, 2)
        carts = []
        for i in cart:
            try:
                x = Cart.objects.get(pk=int(i))
                s_good = StoreHouse.objects.get(s_id_id=x.s_id_id, g_id_id=x.g_id_id)
            except:
                return JsonResponse({"message": "订单错误"})
            if s_good.amount < x.amount:
                return JsonResponse({"message": "有商品库存不够"})
            carts.append(x)
            now_pay += round(s_good.price*x.amount, 2)
            now_pay = round(now_pay, 2)
        for x in carts:
            store = Store.objects.get(pk=x.s_id_id)
            user = User.objects.get(pk=x.u_id_id)
            s_good = StoreHouse.objects.get(s_id_id=x.s_id_id, g_id_id=x.g_id_id)
            money = round(s_good.price*x.amount, 2)
            print(money)
            user.money -= money
            user.money = round(user.money, 2)
            user.save()
            store.sales += money
            store.sales = round(store.sales, 2)
            user.save()
            s_good.amount -= x.amount
            s_good.sales += x.amount
            s_good.save()
            new_record = Record(u_id_id=x.u_id_id, s_id_id=x.s_id_id, g_id_id=x.g_id_id,
                                amount=x.amount, pay=money)
            new_record.save()
            x.delete()
        return JsonResponse({"message": "success", "pay": now_pay})
    return JsonResponse({"message": "请求方式错误"})


# 获取购物车列表
def getCart(request):
    if request.method == 'POST':
        result = {"message": "success", "data": []}
        u_id = int(request.POST.get('u_id'))
        carts = Cart.objects.filter(u_id_id=u_id)
        if not carts:
            return JsonResponse({"message": "购物车暂无内容"})
        for x in carts:
            s_id = x.s_id_id
            g_id = x.g_id_id
            s_good = StoreHouse.objects.get(s_id_id=s_id, g_id_id=g_id)
            cart = {"c_id": x.pk, "amount": x.amount, "s_name": Store.objects.get(pk=s_id).s_name,
                    "g_name": Goods.objects.get(pk=g_id).g_name,
                    "price": s_good.price, "img": s_good.img.name, "pay": round(s_good.price*x.amount, 2)}
            result['data'].append(cart)
        return JsonResponse(result)
    return JsonResponse({"message": "请求方式错误"})


# 获取用户的评论信息
def getUserComments(request):
    if request.method == 'POST':
        result = {"message": "success", "data": []}
        u_id = int(request.POST.get('u_id'))
        comments = Comment.objects.filter(u_id_id=u_id)
        if not comments:
            return JsonResponse({"message": "暂无评论信息"})
        for x in comments:
            s_id = x.s_id_id
            g_id = x.g_id_id
            one_comment = {"s_id": s_id, "s_name": Store.objects.get(pk=s_id).s_name, "text": x.comment,
                           "g_name": Goods.objects.get(pk=g_id).g_name, "kind": Goods.objects.get(pk=g_id).kind,
                           "date": x.date.strftime('%Y-%m-%d %H:%M:%S'),
                           "img": StoreHouse.objects.get(s_id_id=s_id, g_id_id=g_id).img.name}
            result['data'].append(one_comment)
        return JsonResponse(result)
    return JsonResponse({"message": "请求方式错误"})


# 获取商家收到的评论信息
def getStoreComments(request):
    if request.method == 'POST':
        result = {"message": "success", "data": []}
        s_id = int(request.POST.get('s_id'))
        comments = Comment.objects.filter(s_id_id=s_id)
        if not comments:
            return JsonResponse({"message": "暂无评论信息"})
        for x in comments:
            u_id = x.u_id_id
            g_id = x.g_id_id
            one_comment = {"u_id": u_id, "u_name": User.objects.get(pk=u_id).u_name,
                           "u_icon": User.objects.get(pk=u_id).u_icon.name, "text": x.comment,
                           "g_name": Goods.objects.get(pk=g_id).g_name, "kind": Goods.objects.get(pk=g_id).kind,
                           "date": x.date.strftime('%Y-%m-%d %H:%M:%S'),
                           "img": StoreHouse.objects.get(s_id_id=s_id, g_id_id=g_id).img.name}
            result['data'].append(one_comment)
        return JsonResponse(result)
    return JsonResponse({"message": "请求方式错误"})


# 商家销售记录
def getStoreRecord(request):
    if request.method == 'POST':
        result = {"message": "success", "data": []}
        s_id = int(request.POST.get('s_id'))
        records = Record.objects.filter(s_id_id=s_id)
        if not records:
            return JsonResponse({"message": "暂无销售记录"})
        for x in records:
            try:
                good = Goods.objects.get(pk=x.g_id_id)
                user = User.objects.get(pk=x.u_id_id)
                s_good = StoreHouse.objects.get(s_id_id=x.s_id_id, g_id_id=x.g_id_id)
            except:
                return JsonResponse({"message": "记录存在问题"})
            record = {"pk": x.pk, "pay": x.pay, "date": x.date.strftime('%Y-%m-%d %H:%M:%S'), "amount": x.amount,
                      "u_name": user.u_name, "u_id": user.pk, "u_icon": user.u_icon.name,
                      "g_name": good.g_name, "g_id": good.pk,
                      "price": s_good.price, "img": s_good.img.name, "info": s_good.info}
            result['data'].append(record)
        return JsonResponse(result)
    return JsonResponse({"message": "请求方式错误"})