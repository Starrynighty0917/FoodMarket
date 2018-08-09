from rest_framework import serializers
from goods.models import Goods, GoodsCategory, GoodsImage
import re
from FoodMarket.settings import BASE_DIR


# class GoodsSerializer(serializers.Serializer):
    # name = serializers.CharField(required=True, max_length=190)
    # goods_desc = serializers.CharField(max_length=190)
    # 点击次数
    # click_num = serializers.IntegerField(default=0)


class GoodsCategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        # fields = ("name",)
        fields = "__all__"


class GoodsCategorySerializer2(serializers.ModelSerializer):
    sub_cat = GoodsCategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        # fields = ("name",)
        fields = "__all__"


class GoodsCategorySerializer(serializers.ModelSerializer):
    sub_cat = GoodsCategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        # fields = ("name",)
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    category = GoodsCategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"