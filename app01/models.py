from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    position = models.CharField(max_length=32)
    company = models.CharField(max_length=32, choices=(('0', '北京总公司'), ('1', '大连分公司'), ('2', '西安分公司')))
    phone = models.CharField(max_length=11)
    last_time = models.DateTimeField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    # auto_now无论是你添加还是修改对象，时间为你添加或者修改的时间。
    # auto_now_add为添加时的时间，更新对象时不会有变动。

