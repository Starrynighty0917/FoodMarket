
import os
import sys
import django
# 单独使用django的model 也就是如何配置文件,可以直接连接数据库使用model导入数据

pwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(pwd+"../")
# 应用manage.py中的代码:将用到setting中的数据库的配置,因为我们要将category_data中的数据导入数据库
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FoodMarket.settings")


django.setup()

# 这个必须放在os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FoodMarket.settings")之后
# 因为当还没有把FoodMartket目录添加进来,也还没有把setting文件当做为django默认setting文件
from db_tools.data.category_data import row_data
from goods.models import GoodsCategory

for category1 in row_data:
    instance1 = GoodsCategory()
    instance1.name = category1["name"]
    instance1.code = category1["code"]
    instance1.category_type = 1
    instance1.save()

    for category2 in category1["sub_categorys"]:
        instance2 = GoodsCategory()
        instance2.name = category2["name"]
        instance2.code = category2["code"]
        instance2.parent_category = instance1
        instance2.category_type = 2
        instance2.save()

        for category3 in category2["sub_categorys"]:
            instance3 = GoodsCategory()
            instance3.name = category3["name"]
            instance3.code = category3["code"]
            instance3.parent_category = instance2
            instance3.category_type = 3
            instance3.save()
