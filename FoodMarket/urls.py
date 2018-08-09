"""FoodMarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from FoodMarket.settings import MEDIA_ROOT
from django.views.static import serve
from goods.views import GoodsListViewSet, GoodsCategoryViewSet, GoodsImageViewSet
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewSet, UserLeavingMessageViewSet, UserAddressViewSet
from trade.views import ShoppingCartViewSet, ShoppingCartDeleteAll, OrderInfoViewSet

router = DefaultRouter()
router.register(r'goods', GoodsListViewSet)
router.register(r'categorys', GoodsCategoryViewSet)
router.register(r'code', SmsCodeViewSet, base_name="code")
router.register(r'users', UserViewSet, base_name="users")
router.register(r'goodsimage', GoodsImageViewSet, base_name="goodsimage")
router.register(r'userfavs', UserFavViewSet, base_name="userfavs")
router.register(r'messages', UserLeavingMessageViewSet, base_name="messages")
router.register(r'address', UserAddressViewSet, base_name="address")
router.register(r'shopcarts', ShoppingCartViewSet, base_name="shopcarts")
router.register(r'orders', OrderInfoViewSet, base_name="orders")


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # url(r'goods/', GoodsListView.as_view(), name="good_list"),
    # 生成drf(django-rest-framework)文档的配置
    url(r'^docs/', include_docs_urls(title='FoodMarket')),
    # 如果您打算使用可浏览的API，您可能还需要添加REST框架的登录和注销视图。
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^', include(router.urls)),
    # 这是github上面的jwttoken创建的URL
    url(r'^login/', obtain_jwt_token),
    # 这是restframework自带的TokenAuthentication的创建token的URL
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^shopcartsclear/$', ShoppingCartDeleteAll.as_view()),

]

