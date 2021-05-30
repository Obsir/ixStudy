from django import forms
from django.core.exceptions import ValidationError
import re
from app01 import models
import hashlib
from PIL import Image


class BootStrapForm(forms.ModelForm):
    """
    bootstrap样式
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 自定义操作
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class ArticleDetailForm(forms.ModelForm):
    class Meta:
        model = models.ArticleDetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 自定义操作


class CategoryForm(BootStrapForm):
    class Meta:
        model = models.Category
        fields = '__all__'


class ArticleForm(BootStrapForm):
    class Meta:
        model = models.Article
        fields = "__all__"
        exclude = ['detail']

    # def __init__(self, request, *args, **kwargs):
    #     # 获取到用户传来的request参数，不要往父类传递
    #     super().__init__(*args, **kwargs)
    #     # 自定义操作
    #     for field in self.fields.values():
    #         field.widget.attrs["class"] = "form-control"
    #
    #     # 修改choices的参数
    #     self.fields['author'].choices = [(request.user_obj.pk, request.user_obj.username)]
    def __init__(self, *args, **kwargs):
        # 获取到用户传来的request参数，不要往父类传递
        super().__init__(*args, **kwargs)
        # 修改choices的参数
        self.fields['author'].choices = [(self.instance.author.pk, self.instance.author.username)]


class RegForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
        # 自定义操作
        self.fields['company'].choices[0] = ('', '选择公司')
        self.fields['company'].choices = self.fields['company'].choices  # 迷惑操作？

    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)

    re_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "confirm_password",
                                          "placeholder": "再次输入密码",
                                          "oncontextmenu": "return false",
                                          "onpaste": "return false"}),
        label='确认密码', min_length=6)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "password",
                                          "placeholder": "输入密码",
                                          "oncontextmenu": "return false",
                                          "onpaste": "return false"}),
        error_messages={'required': '必填项'}, label='密码', min_length=6)

    class Meta:
        model = models.User
        # fields = ['username', 'password', ]
        fields = '__all__'
        exclude = ['last_time', 'is_activate']
        # labels = {
        #     'username': '用户名'
        # }
        widgets = {
            'username': forms.TextInput(attrs={
                "class": "username",
                "placeholder": "您的用户名",
                "autocomplete": "off"
            }),
            'position': forms.TextInput(attrs={
                "placeholder": "请输入职位",
                "autocomplete": "off"
            }),
            'phone': forms.TextInput(attrs={
                "placeholder": "请输入手机号码",
            }),
        }
        error_messages = {
            'username': {
                'required': '必填项'
            },
            'password': {
                'required': '必填项'
            }
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if re.match(r'^1[3-9]\d{9}$', phone):
            return phone
        raise ValidationError('手机号格式不正确')

    def clean(self):
        self._validate_unique = True
        password = self.cleaned_data.get('password', '')
        re_password = self.cleaned_data.get('re_password')
        if password == re_password:
            md5 = hashlib.md5()
            md5.update(password.encode('utf-8'))
            self.cleaned_data['password'] = md5.hexdigest()
            return self.cleaned_data
        self.add_error('re_password', '两次密码不一致')
        raise ValidationError('两次密码不一致')

    def save(self, commit=True):
        user = super(RegForm, self).save(commit=False)
        user.save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        if x:
            avatar = Image.open(user.avatar)
            avatar = avatar.crop((x, y, w + x, h + y))
            avatar.save(user.avatar.path)

        return user
