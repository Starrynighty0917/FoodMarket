from datetime import datetime, timedelta

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from users.models import VerifyCode
from FoodMarket.settings import REGIX_MOBILE
import re


User = get_user_model()


class MobileVarifySerializer(serializers.Serializer):
    """
    手机验证
    因为在用户注册时，只是发送了电话号码，然后发送给后端请求短信，所以这里做的是手机号码的验证
    """
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        做手机号码的验证
        1 首先是手机是否已经存在
        2 手机是否满足手机号码的正则匹配
        3 验证码发送频率保证为60s
        """
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")
        if not re.search(REGIX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")
        # 首先记录一分钟之前的时间
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        # 如果这个手机号码和验证码在一分钟之内添加进数据库了，证明现在还不能再次发送，必须等到满了一分钟才行
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile):
            raise serializers.ValidationError("验证码发送未满一分钟，请稍后再试")
        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    """
    用户序列化类
    其中重要的功能是注册用户，
    write_only=True是为了防止此字段参与序列化，传送给前端
    """
    code = serializers.CharField(
                                 write_only=True, required=True, min_length=4, max_length=4, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "max_length": "验证码最多为4位",
                                     "min_length": "验证码最少位4位"
                                 })
    password = serializers.CharField(required=True, label="密码", write_only=True,
                                     style={
                                        'input_type': "password"
                                     })
    username = serializers.CharField(required=True, allow_blank=False, label="用户名")
    mobile = serializers.CharField(required=False, allow_blank=True, label="电话号码", read_only=True)


    def validate_code(self, code):
        """
        主要使用了code检查，在数据库看code是否过期，比如在一分钟之内点了注册按钮并通过，就注册成功，如果code的add时间小于一分钟之前的时间，
        也就是过了验证期，则需要用户重新申请发送验证码，映射URL：/users/,前端发送来的数据：
        username:that.mobile ,
        code:that.code,
        password:that.password,
        initial_data指的前端传过来的数据
        :param code:
        :return:
        """
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_code = verify_records[0].add_time
            # 取出前2分钟的时间，和这条记录加入的时间作比较
            two_mins_ago = datetime.now() - timedelta(minutes=10)
            if last_code < two_mins_ago:
                raise serializers.ValidationError("验证码过期")
            if verify_records[0].code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate_username(self, username):
        user_possible = User.objects.filter(mobile=username)
        if user_possible:
            raise serializers.ValidationError("用户已经存在")
        return username

    def validate(self, attrs):
        """
        attrs指的每个字段validate之后的总字段dict
        :param attrs:
        :return:
        """
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    def create(self, validated_data):
        # instance是User创建的实例
        instance = User(**validated_data)
        instance.set_password(validated_data["password"])
        instance.save()
        return instance

    class Meta:
        """
        因为前端是这样传过来的数据
        username:that.mobile ,
        code:that.code,
        password:that.password,
        所以序列化时，username实际指的是传过来的mobile
        """
        model = User
        fields = ("username", "code", "mobile", "password")


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "birthday", "gender", "mobile", "email")






