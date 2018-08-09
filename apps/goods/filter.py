from goods.models import Goods
import django_filters
from django.db.models import Q


class GoodsFilter(django_filters.rest_framework.FilterSet):
    pricemax = django_filters.NumberFilter(name='shop_price', lookup_expr='lt')
    pricemin = django_filters.NumberFilter(name='shop_price', lookup_expr='gt')
    top_category = django_filters.NumberFilter(method='top_category_filter')

    # 这里查询的是queryset中类别的外键parent_category的id
    # 首先查自己的分类id中有没有等于value查询结果，再看父类id有没有等于value的，这样可以查出id不属于本类但是id是父类的产品
    def top_category_filter(self, queryset, name ,value):
        a = queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value)
                               |Q(category__parent_category__parent_category_id=value)
        )
        return a

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot']
