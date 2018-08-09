from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from DjangoUeditor.models import UEditorField
# Create your models here.


class GoodsCategory(models.Model):
    """
    商品类别
    """
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
        (3, "三级类目"),
    )

    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    desc = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    # 当商品类型为第一类时,没有父类,所以可以为空,   related_name="sub_cat"在查询的时候能用到
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父级商品类型", related_name="sub_cat",
                                        help_text="父级商品类型", on_delete=models.CASCADE)
    # 当商品类型放在tab上面进行展示的时候,要上使用True or False进行记录
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """
    品牌信息
    每个商品类型都有几个品牌
    品牌有商家名字,商家品牌照片
    """
    category = models.ForeignKey(GoodsCategory, related_name='brands', null=True, blank=True, verbose_name="商品类目",
                                 on_delete=models.CASCADE)
    name = models.CharField(default="", max_length=30, verbose_name="品牌名", help_text="品牌名")
    desc = models.TextField(default="", max_length=200, verbose_name="品牌描述", help_text="品牌描述")
    image = models.ImageField(max_length=200, upload_to="brand/images/")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "品牌"
        verbose_name_plural = verbose_name
        db_table = "goods_goodsbrand"

    def __str__(self):
        return self.name


class Goods(models.Model):
    """
    商品
    """
    category = models.ForeignKey(GoodsCategory, default='', verbose_name="商品类目", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="商品名")
    # 商品编号,用于取货,拿货之类的
    goods_sn = models.CharField(max_length=50, default="", verbose_name="商品唯一货号")
    # 商品主页描述文字
    goods_brief = models.TextField(max_length=500, verbose_name="商品简短描述")
    # 富文本,用来描述商品的具体信息 宽度和高度用于后台展示时使用
    goods_desc = UEditorField(imagePath="goods/images/", filePath="goods/files/", width=1000, height=300,
                              verbose_name="内容")
    # 点击次数
    click_num = models.IntegerField(default=0, verbose_name="点击次数")
    # 收藏次数
    fav_num = models.IntegerField(default=0, verbose_name="收藏数")
    # 销量
    sold_num = models.IntegerField(default=0, verbose_name="商品销量")
    # 商品库存
    goods_num = models.IntegerField(default=0, verbose_name="库存数")
    # 原价/市场价
    market_price = models.FloatField(default=0.0, null=True, blank=True, verbose_name="市场价格")
    # 现价/折扣价
    shop_price = models.FloatField(default=0.0, verbose_name="本店价格")
    # 是否免运费
    ship_free = models.BooleanField(default=True, verbose_name="是否承担运费")
    # 首页商品显示图片
    goods_front_image = models.ImageField(upload_to="", null=True, blank=True, verbose_name="商品封面图")

    # 是否为上新产品
    is_new = models.BooleanField(default=False, verbose_name="是否为上新产品")
    # 是否为热卖商品
    is_hot = models.BooleanField(default=False, verbose_name="是否为热销产品 ")
    # 每个表都需要的字段,创建时间
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    """
    商品详情页轮播图片
    但凡涉及到一对多都要使用外键,外键的意思是,自己的一个关键字是别的表的主键
    goods指的是这张图片属于哪一个商品的图，related_name是方便在goods类中序列化时，可以将本model序列化进去
    """
    goods = models.ForeignKey(Goods, verbose_name="商品", related_name="images", on_delete=models.CASCADE)
    # 因为在数据导入时,自动有image的绝对路径了,所以不需要写goods/images/
    image = models.ImageField(upload_to="", verbose_name="图片", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    """
    轮播的商品
    """
    goods = models.ForeignKey(Goods, verbose_name="轮播图货物", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="banner", verbose_name="轮播图片")
    # 轮播图的顺序,1则为第一张图
    index = models.IntegerField(default=1, verbose_name="轮播图片序号")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '轮播商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name
