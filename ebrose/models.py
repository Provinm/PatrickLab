from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wechat_name = models.CharField('微信昵称', max_length=100, default="匿名用户")
    openid = models.CharField('用户标识', max_length=100, blank=True, null=True)
    cookie = models.CharField('用户认证标识', max_length=100, blank=True, null=True)
    GENDER = (
        (1, '男'),
        (2, '女'),
        (0, '未知')
    )
    gender = models.IntegerField('性别', choices=GENDER, default=0)
    city = models.CharField('城市', max_length=100, blank=True, null=True)
    province = models.CharField('省份', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.wechat_name

class Poetry(models.Model):
    '''诗词内容
    '''
    author = models.ForeignKey("Author", verbose_name="作者", on_delete=models.SET_DEFAULT, 
                               default="佚名")
    paragraphs = models.TextField("正文")
    dynasty = models.CharField("朝代", max_length=20, default=" ")
    title = models.CharField("标题", max_length=100, default=" ")
    rhythmic = models.CharField("词牌名", max_length=100, default=" ")

    CONTENT_TYPE = (
        ("S", "诗"),
        ("C", "词"),
        ("J", "经"),
        ("O", "其他"))
    _type = models.CharField("类型", max_length=100, default="S", choices=CONTENT_TYPE)
    created_time = models.DateTimeField("创建时间", auto_now_add=True)
    is_active = models.BooleanField("是否有效", default=True)
    refer_count = models.IntegerField("被引用次数", default=0)

    def __str__(self):
        return self.title

class Sentence(models.Model):
    '''每一句诗词
    '''

    poetry = models.ForeignKey("Poetry", verbose_name="诗词名", related_name="sentence", on_delete=models.CASCADE)
    text = models.TextField("句")

    def __str__(self):
        return self.text
    

class Author(models.Model):
    '''作者
    '''
    name = models.CharField("姓名", max_length=100)

    def __str__(self):
        return self.name