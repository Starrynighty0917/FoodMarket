from django.shortcuts import render
from django.views.generic import ListView
from goods.models import Goods


# Create your views here.
class GoodsListView(ListView):
    def get(self, request, *args, **kwargs):
        goods = Goods.objects.all()[:10]
        # goods_list = []
        # for good in goods:
        #     good_dict = {}
        #     good_dict["name"] = good.name
        #     good_dict["category"] = good.category.name
        #     good_dict["shop_price"] = good.shop_price
        #     goods_list.append(good_dict)
        import json
        from django.http import HttpResponse
        from django.core.serializers import serialize

        json_data = serialize("json", goods)
        # json_data = json.loads(json_data)
        return HttpResponse(json_data, content_type="application")

        # json_data = json.dumps(goods_list)
        # return HttpResponse(json_data, content_type="application/json")
