from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Goods
User = get_user_model()
# Create your models here.


class ShoppingCart(models.Model):
    """
    购物车
    商品多次购买,只是记录件数增减
    购物车对于同一个商品,只能记录一条,当再次进行增加时,只是数量的增加
    """
    user = models.ForeignKey(User, verbose_name=u"用户", on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name=u"商品", on_delete=models.CASCADE)
    nums = models.IntegerField(default=0, verbose_name="购买数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        # 在购物车中，当新添一条商品时，如果已经存在，则验证不通过，商品数量覆盖原来的数量即可，如果不存在就创建新的商品到购物车中
        unique_together = ("user", "goods")

    def __str__(self):
        return "%s(%d)".format(self.goods.name, self.nums)


class OrderInfo(models.Model):
    """
    订单信息
    订单有订单信息还有支付宝交易信息
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED", "交易结束"),
        ("paying", "待支付"),
    )

    user = models.ForeignKey(User, verbose_name="用户名", on_delete=models.CASCADE)
    # 订单编号, 唯一
    order_sn = models.CharField(default="", max_length=50, blank=True, null=True, unique=True, verbose_name="订单编号")
    # 支付宝订单号和本订单进行关联, 唯一, 在支付之前交易单号可以为空
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="交易编号")
    # 订单金额
    order_mount = models.FloatField(default=0.0, verbose_name="订单金额")
    # 收件人地址
    address = models.CharField(max_length=100, verbose_name="收件人地址")
    # 收件人姓名
    signer_name = models.CharField(max_length=20, verbose_name="收件人姓名")
    # 收件人电话
    signer_mobile = models.CharField(max_length=11, verbose_name="收件人电话")
    # 订单状态
    pay_status = models.CharField(max_length=30, choices=ORDER_STATUS, default="paying", verbose_name="订单状态")
    # 支付时间
    pay_time = models.DateTimeField(default=datetime.now, verbose_name="支付时间")
    # 订单留言
    post_script = models.CharField(default="", max_length=100, verbose_name="订单留言")
    # 创建时间
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s %s" % (self.user.name, self.order_sn)


class OrderGoods(models.Model):
    """
    订单的商品详情
    购物车结算的时候，到达的订单页面
    """
    order = models.ForeignKey(OrderInfo, verbose_name="订单信息", related_name="goods", on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE)
    goods_num = models.IntegerField(default=0, verbose_name="商品数量")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)
