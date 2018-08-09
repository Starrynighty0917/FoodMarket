import datetime
from time import timezone

from rest_framework import serializers

from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer


class UserFavSerializers(serializers.ModelSerializer):
    """
    这是用户点击收藏和删除收藏时要用到的序列化
    普通的序列化，这里只取收藏ID和商品ID，user的信息是隐藏的
    """
    # 为了取出当前用户的默认类,方便收藏对象的实例化,自动填充user
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        # 前端只是传进来了goods的id,为了方便取消收藏，需要序列化id的值
        fields = ("user", "goods",)


class UserFavDetailSerializers(serializers.ModelSerializer):
    """
    这是用户操作里面用户收藏的物品
    用户中心的个人收藏 得到当前用户的收藏 这里使用了商品的序列化,使得商品显示更加详细，方便前端显示商品信息
    """
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ("goods", "id")


class UserLeavingMessageSerializers(serializers.ModelSerializer):
    # 来自动填充user
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(
        read_only=True,
        format="%Y-%m-%d %H:%M:%S"
    )

    class Meta:
        model = UserLeavingMessage
        # 这个id是为了删除留言所需要的
        fields = ("user", "message_type", "subject", "message", "file", "id", "add_time")


class UserAddressSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(
        read_only=True,
        format="%Y-%m-%d %H:%M:%S"
    )

    class Meta:
        model = UserAddress
        fields = ("user", "province", "city", "district", "address", "signer_name", "signer_mobile", "add_time", "id")



