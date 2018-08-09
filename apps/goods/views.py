# class base view
import re
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins, generics
from rest_framework import viewsets
from goods.models import Goods, GoodsCategory, GoodsImage
from goods.serializers import GoodsSerializer, GoodsCategorySerializer, GoodsImageSerializer

from goods.MyPageNumberPagination import LargeResultsSetPagination
from FoodMarket.settings import UEDITOR_PREFIX

from goods.filter import GoodsFilter


# mixins.ListModelMixin, generics.GenericAPIView本来是继承这两个的,后来在generics里面有ListAPIView(mixins.ListModelMixin,
#                   GenericAPIView)非常方便了, ListModelMixmin主要有list方法,generics的APIview主要是为queryset创建视图
class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    List all goods
    """
    queryset = Goods.objects.all()
    len(queryset)
    serializer_class = GoodsSerializer
    pagination_class = LargeResultsSetPagination
    # pagination_class = PageNumberPagination
    # authentication_classes = (TokenAuthentication, )
    # 过滤器后端
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 自定义过滤器类
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('goods_num', 'shop_price')
    # def get(self, request, format=None):
    #     goods = Goods.objects.all()[:10]
    #     goods_serializer = GoodsSerializer(goods, many=True)
    #     return Response(goods_serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        goods_dict = serializer.data
        # 将富文本信息提取出来用正则把访问 图片资源的前缀匹配上去
        goods_dict["goods_desc"] = re.sub(r'src=".*?/', 'src="'+UEDITOR_PREFIX+"/", goods_dict["goods_desc"])
        return Response(goods_dict)


class GoodsCategoryViewSet(mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """
    只要继承了RetrieveModelMixin,就可以获取某一类数据的单个ID数据,比如category中id为361的http://127.0.0.1:8000/categorys/361/
    如果没有这个RetrieveModelMixin那么就没办法实现访问单个实例
    这个视图主要是返回head组件中的全部分类，不过是按层级展示的，所以queryset是查找的一级类目
    """
    queryset = GoodsCategory.objects.filter(category_type = 1)
    serializer_class = GoodsCategorySerializer

    # 实现访问单个的category
    def retrieve(self, request, pk=None):
        queryset = GoodsCategory.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        serializer = GoodsCategorySerializer(category)
        return Response(serializer.data)


class GoodsImageViewSet(viewsets.ModelViewSet):
    queryset = GoodsImage
    serializer_class = GoodsImageSerializer
