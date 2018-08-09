from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import mixins, viewsets
import random

from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.utils import jwt_encode_handler
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from FoodMarket.settings import APIKEY
from users.serializers import MobileVarifySerializer
from utils.yunpian import SmsYunPian
from users.models import VerifyCode
from users.serializers import UserRegSerializer, UserDetailSerializer


User = get_user_model()





class CustomBackend(ModelBackend):
    """
    自定义用户认证类
    在setting中配置了AUTHENTICATION_BACKENDS
    因为用户不仅可以使用用户名进行登录，还可以使用手机号码登录，而django自带的认证系统只是验证用户名和密码，所以自创一个认证后台方便手机号验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            return None


class SmsCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信处理类
    用户在注册页面输入手机号码之后，点击获取验证码，前台触发seedMessage按钮，调用api接口向后台（url:/code/）请求验证码数据
    1 使用MobileVarifySerializer对手机号码进行验证
    2 验证不通过抛出异常，通过则通过utils中的SmsYunPian来向验证通过的手机发送验证码
    成功发送短信码后要将这些信息存储起来
    """
    serializer_class = MobileVarifySerializer

    # 自定义拿来生成四位验证码的
    def get_valify_code(self):
        final_code = ""
        for i in range(4):
            final_code += str(random.randint(0,9))
        return final_code

    def create(self, request, *args, **kwargs):
        # 检查电话号码验证是否成功，不成功raise_exception=true
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 从序列化实例中取出已经验证过的数据
        mobile = serializer.validated_data['mobile']
        # 检查成功后，随机生成四位短信验证码
        code = self.get_valify_code()
        # 使用SmsYunPian发送短信给验证通过的mobile
        yun_pian = SmsYunPian(APIKEY)
        # 发送后返回的JSON字符串数据,当发回的code字段等于0，证明发送成功，msg字段也为发送成功，部位0时，msg字段会有相应提示
        response_data = yun_pian.send_mess(code, mobile)
        if response_data["code"] != 0:
            return Response({
                "mobile" : response_data["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            ms = VerifyCode(mobile=mobile, code=code)
            ms.save()
            return Response({
                "mobile" : mobile
            }, status=status.HTTP_201_CREATED)


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    create:
        注册用户
    update:
        修改用户个人中心的信息
    retrieve:
        获取用户个人中心的信息
    """
    queryset = User.objects.all()
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)

    def create(self, request, *args, **kwargs):
        # 从前端序列化后验证是否合理
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 这里需要得到model user,来生成token所以取出来了
        user = self.perform_create(serializer)
        # 这里是为了把生成的name和token加入到序列化字段中所以把它取出来形成一个dict对象
        serializer_dict = serializer.data
        # 使用user来返回token，因为之前生成token是在登录的时候生成返回，这里注册后要实现用户立马能够登录就需要我们自己生成token和name返回给前端
        payload = jwt_payload_handler(user)
        serializer_dict["token"] = jwt_encode_handler(payload)
        serializer_dict["name"] = user.name if user.name else user.username
        headers = self.get_success_headers(serializer.data)
        return Response(serializer_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    # 为RetrieveModelMixin做准备
    def get_object(self):
        return self.request.user

    def get_permissions(self):
        """
        部分更新时是patch
        :return:
        """
        if self.action == "retrieve":
            return [IsAuthenticated()]
        elif self.action == "create":
            return []
        elif self.action == "update":
            self.serializer_class = UserDetailSerializer
            return [IsAuthenticated()]
        else:
            return []

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer
        elif self.action == "update":
            return UserDetailSerializer
        else:
            return UserDetailSerializer








