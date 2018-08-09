
import os
import sys

pwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(pwd+"../")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FoodMarket.settings")

import django
django.setup()

from goods.models import Goods, GoodsCategory, GoodsImage
from db_tools.data.product_data import row_data

for import_good_data in row_data:
    db_good = Goods()
    db_good.name = import_good_data["name"]
    # 首页图片路径保存为字符串即可
    db_good.goods_front_image = import_good_data["images"][0] if import_good_data["images"] else ''
    db_good.market_price = float(int(import_good_data["market_price"].replace("￥", "").replace("元", "")))
    db_good.shop_price = float(int(import_good_data["sale_price"].replace("￥", "").replace("元", "")))
    db_good.goods_brief = import_good_data["desc"] if import_good_data["desc"] is not None else ""
    db_good.goods_desc = import_good_data["goods_desc"] if import_good_data["goods_desc"] is not None else ""

    # 取出最后一个根茎类字符串就可以了
    category_name = import_good_data["categorys"][-1]
    # 为什么使用filter不使用get因为使用django的get方法是从数据库的取得一个匹配的结果，返回一个对象，如果记录不存在的话，它会报错,
    # 而且记录多于两条也会报错,而使用filter会返回结果的一个数组,当没有查询到结果时返回空数组。
    goods_category = GoodsCategory.objects.filter(name=category_name)
    if goods_category:
        db_good.category = goods_category[0]
    db_good.save()

    # 把每个图片保存为对象
    if import_good_data["images"]:
        for image in import_good_data["images"]:
            goods_image = GoodsImage()
            goods_image.image = image
            goods_image.goods = db_good
            goods_image.save()

