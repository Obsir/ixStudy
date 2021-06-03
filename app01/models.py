from django.db import models
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
import os, uuid
from imagekit.models import ProcessedImageField
import datetime

# Create your models here.
def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # 这里的id是User表的id
    return os.path.join('user', instance.username, "avatar", filename)


class User(models.Model):
    username = models.CharField(max_length=32, verbose_name='用户名', unique=True)
    password = models.CharField(max_length=32, verbose_name='密码')
    position = models.CharField(max_length=32, verbose_name='职位')
    company = models.CharField(max_length=32, verbose_name='公司',
                               choices=(('0', '北京总公司'), ('1', '大连分公司'), ('2', '西安分公司')))
    phone = models.CharField(max_length=11, verbose_name='手机号')
    last_time = models.DateTimeField(null=True, blank=True, verbose_name='上次登陆时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    # 用户是否注销
    is_activate = models.BooleanField(default=True)
    avatar = ProcessedImageField(upload_to=user_directory_path, default='img/avatar/default.jpg', verbose_name='头像',
                                 format='JPEG', options={'quality': 100})

    # auto_now无论是你添加还是修改对象，时间为你添加或者修改的时间。
    # auto_now_add为添加时的时间，更新对象时不会有变动。

    def __str__(self):
        return self.username


class Category(models.Model):
    """
    标题
    """
    title = models.CharField(max_length=64, verbose_name="板块标题")

    def __str__(self):
        return self.title


class Article(models.Model):
    """
    文章表：
        标题
        文章摘要
        发表时间
        作者
        板块
        创建时间
        更新时间
        删除状态
    """
    title = models.CharField(max_length=64, verbose_name='文章标题')
    abstract = models.CharField(max_length=256, verbose_name="文章摘要")
    author = models.ForeignKey('User', on_delete=models.DO_NOTHING, null=True, verbose_name="作者")
    category = models.ForeignKey('Category', verbose_name="板块", on_delete=models.DO_NOTHING, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    publish_status = models.BooleanField(default=False, choices=((False, '未发布'), (True, '发布')), verbose_name="发布状态")
    detail = models.OneToOneField('ArticleDetail', on_delete=models.DO_NOTHING)
    point = models.IntegerField(default=0, verbose_name="文章积分")
    duration = models.DurationField(default=datetime.timedelta(), verbose_name="推荐阅读时间")

    def show_publish_status(self):
        color_dict = {
            True: 'label-primary',
            False: 'label-danger'
        }
        return mark_safe('<span class="label {}">{}</span>'.format(color_dict[self.publish_status],
                                                                   self.get_publish_status_display()))

    def __str__(self):
        return self.title

class ArticleDetail(models.Model):
    """
    文章详情表
    """
    content = RichTextUploadingField(verbose_name="文章内容")

class Series(models.Model):
    """
    系列
    """
    title = models.CharField(max_length=32, verbose_name="系列名称")
    articles = models.ManyToManyField('Article', verbose_name='文章')
    users = models.ManyToManyField('User', verbose_name='用户', through='UserSeries', related_name='series')   # 创建第三张表, 自定义的第三张表


class UserSeries(models.Model):
    user = models.ForeignKey('User', verbose_name='用户')
    series = models.ForeignKey('Series', verbose_name='系列')
    points = models.IntegerField(default=0, verbose_name='当前分数')
    total_points = models.IntegerField(default=0, verbose_name='总分数')
    progress = models.CharField(max_length=32, default='0.00', verbose_name='进度')


class Comment(models.Model):
    """
    评论表：
        评论者
        评论内容
        评论的文章
        评论时间
        审核状态
    """
    author = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="评论者")
    article = models.ForeignKey('Article', on_delete=models.CASCADE, verbose_name="文章")
    content = models.TextField(verbose_name="评论内容")
    time = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    status = models.BooleanField(verbose_name="审核状态", default=True)

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='sons')  # 楼中楼
    reply_to = models.ForeignKey('User', blank=True, null=True, on_delete=models.CASCADE, related_name="replies")

    class Meta:
        ordering = ('-time',)

class PointDetail(models.Model):
    """
    积分表：
    """
    user = models.ForeignKey('User', verbose_name="用户")
    article = models.ForeignKey('Article', verbose_name="文章")
    point = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)