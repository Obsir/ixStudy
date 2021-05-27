from django.shortcuts import render, redirect
from app01 import models
from django import forms
from django.core.exceptions import ValidationError
import re
import hashlib


class RegForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
        # 自定义操作
        self.fields['company'].choices[0] = ('', '选择公司')
        self.fields['company'].choices = self.fields['company'].choices  # 迷惑操作？

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
        exclude = ['last_time']
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


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 加密
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        user_obj = models.User.objects.filter(username=username, password=md5.hexdigest(), is_activate=True).first()
        if user_obj:
            # 登陆成功
            # 保存登录状态 用户名
            request.session['is_login'] = True
            request.session['username'] = user_obj.username

            url = request.GET.get('url')
            if url:
                return redirect(url)
            return redirect('index')
        error = "用户名或密码错误"
    return render(request, 'login.html', locals())


def logout(request):
    request.session.delete()
    return redirect('index')


def index(request):
    # 查询所有文章
    all_articles = models.Article.objects.all()
    is_login = request.session.get('is_login')
    username = request.session.get('username')
    return render(request, 'index.html', {'all_articles': all_articles})


def article(request, pk):
    article_obj = models.Article.objects.get(pk=pk)
    return render(request, 'article.html', {'article_obj': article_obj})


def backend(request):
    return render(request, 'dashboard.html')


def register(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            # form_obj.cleaned_data.pop('re_password')
            # models.User.objects.create(**form_obj.cleaned_data)
            instance = form_obj.save(commit=False)
            instance.is_activate = True
            instance.save()
            return redirect('login')
    return render(request, 'register.html', {'form_obj': form_obj})
