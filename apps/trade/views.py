import datetime

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from user_operation.permissions import IsOwnerOrReadOnly
from .serializers import ShoppingCartSerializer, ShoppingCartDetialSerializer, \
                            OrderInfoSerializer, OrderInfoDetailSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
        list:
            得到该登录用户购物车的信息
        create:
            将商品加入购物车
            前端传过来的参数：{
                goods: this.productId, // 商品id
                nums: this.buyNum, // 购买数量
            }
        destroy:
            删除购物车的商品
        update:
            更新购物车商品的数量
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = "goods_id"
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        """
        限制获得当前用户的查询集
        :return:
        """
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """
        当action为list要getShopCarts获得购物车所有的商品的时候，就是跳转shopcart组件的时候了，这时候需要对goods字段进行详细的展示
        所以需要序列化商品字段
        :return:
        """
        if self.action == "list":
            return ShoppingCartDetialSerializer
        else:
            return ShoppingCartSerializer




class ShoppingCartDeleteAll(DestroyAPIView):
    """
    删除购物车的所有商品
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = ShoppingCartDetialSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderInfoViewSet(ListModelMixin, DestroyModelMixin, CreateModelMixin, RetrieveModelMixin,
                       viewsets.GenericViewSet):

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = OrderInfoSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save()
        shopcart = ShoppingCart.objects.filter(user=self.request.user)
        for goods in shopcart:
            order_goods = OrderGoods()
            order_goods.order = order
            order_goods.goods = goods.goods
            order_goods.goods_num = goods.nums
            order_goods.save()
        shopcart.delete()
        return order

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderInfoDetailSerializer
        else:
            return OrderInfoSerializer




