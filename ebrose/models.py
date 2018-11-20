from django.db import models

# Create your models here.

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

    poetry = models.ForeignKey("Poetry", verbose_name="诗词名", on_delete=models.SET_DEFAULT, default="空")
    text = models.TextField("句")

    def __str__(self):
        return self.text
    

class Author(models.Model):
    '''作者
    '''
    name = models.CharField("姓名", max_length=100)

    def __str__(self):
        return self.name