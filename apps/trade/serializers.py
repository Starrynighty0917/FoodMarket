import random
import time
from datetime import datetime

from rest_framework import serializers
from trade.models import ShoppingCart, OrderInfo, OrderGoods
from goods.models import Goods
from goods.serializers import GoodsSerializer


class ShoppingCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # goods = GoodsSerializer(many=True)
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all(), required=True)
    nums = serializers.IntegerField(required=True, min_value=1,
                                          error_messages={
                                              "min_value": "商品件数不能为0",
                                              "required": "商品数量必填"
                                          })

    def create(self, validated_data):
        user = self.context["request"].user
        goods = validated_data["goods"]
        exists = ShoppingCart.objects.filter(user=user, goods=goods)
        if exists:
            exists = exists[0]
            exists.nums += validated_data["nums"]
            exists.save()
        else:
            exists = ShoppingCart.objects.create(**validated_data)
        return exists

    def update(self, instance, validated_data):
        instance.nums = validated_data.get("nums", instance.nums)
        instance.save()
        return instance


class ShoppingCartDetialSerializer(serializers.ModelSerializer):
    """
    购物车结算页面的序列化
    """
    # 一个商品和用户构成联合唯一的关系
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = ("goods", "nums")


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderInfoDetailSerializer(serializers.ModelSerializer):
    orderGoods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = ("orderGoods", "order_sn", "pay_status", "id", "address", "signer_name", "signer_mobile")


class OrderInfoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(
        default=datetime.now(),
        format="%Y-%m-%d %H:%M:%S"
    )
    order_sn = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True
    )

    def get_order_sn(self):
        # 一般为下单时间+用户id+三位随机数
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        user_id = self.context["request"].user.id
        random_nums = random.randint(100, 999)
        return now+str(user_id)+str(random_nums)

    def validate(self, attrs):
        attrs["order_sn"] = self.get_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = ("user", "order_sn", "order_mount", "trade_no", "address", "signer_name", "signer_mobile",
                  "pay_status", "pay_time", "post_script", "add_time", "id")



