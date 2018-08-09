from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializers, UserFavDetailSerializers
from .serializers import UserLeavingMessageSerializers, UserAddressSerializers
from .permissions import IsOwnerOrReadOnly


class UserFavViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    """
    list:
        获取用户中心的收藏列表
    retrieve:
        主要用于前端在验证登录用户是否收藏的状态这件物品getFav，所以只需要普通的序列化得到商品的ID和收藏的ID
    create:
        收藏商品
    destroy:
        取消收藏
    和购物车的模式一样，只有在用户中浏览收藏记录或者浏览购物车详情的时候，需要把收藏的东西或者购买的商品的详情序列化出来，
    方便渲染这些信息（url方便用户跳转、名字、图片之类的），只有在加入收藏和加入购物车的时候，只需要序列化收藏物品的id和商品的id就可以了，知道这个id
    就方便数据的增删改操作了
    """

    serializer_class = UserFavSerializers
    # SessionAuthentication为后端请求的接口 这两个配置了就是通过浏览器添加session或者在head里面添加token
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # 设置了这个
    lookup_field = "goods_id"

    def get_queryset(self):
        """
        有了这个之后这个视图只能获得当前用户的收藏信息,所以就不需要判断当前操作的模型是不是对应的用户了（IsOwnerOrReadOnly）
        :return:
        """
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            # 普通的序列化，这里只取收藏ID和商品ID，user的信息是隐藏的 这里的retrieve只要good_id就可以了，这样就能查看是否这个用户
            # 收藏了这个商品
            return UserFavSerializers
        elif self.action == "list":
            # 用户中心的个人收藏 得到当前用户的收藏 这里使用了商品的序列化
            return UserFavDetailSerializers
        elif self.action == "create":
            # IsAuthenticated验证是否已经登录 IsOwnerOrReadOnly验证删除时，当前用户
            # 删除的是自己的记录（通过userfav/pk来删除id为pk的记录）
            return UserFavSerializers
        elif self.action == "destroy":
            return UserFavSerializers
        else:
            return UserFavSerializers


class UserLeavingMessageViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    """
        list:
            得到该登录用户所有留言信息
        create:
            创建留言
        destroy:
            删除留言
    """
    serializer_class = UserLeavingMessageSerializers
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class UserAddressViewSet(viewsets.ModelViewSet):
    """
        list:
            得到该登录用户所有地址信息
        create:
            创建收货地址
        destroy:
            删除收货地址
        update:
            更新收货地址
    """
    serializer_class = UserAddressSerializers
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        """
        限制获得当前用户的查询集
        :return:
        """
        return UserAddress.objects.filter(user=self.request.user)




