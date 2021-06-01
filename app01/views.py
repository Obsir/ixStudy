from django.shortcuts import render, redirect
from app01 import models
from app01.forms import RegForm, ArticleForm, ArticleDetailForm, CategoryForm
import hashlib
from utils.pagination import Pagination
from django.db.models import Q


def get_query(request, field_list):
    # 传入一个列表 ['title', 'detail__content']
    # 返回Q对象
    query = request.GET.get('query', '')

    q = Q()
    q.connector = 'OR'
    for field in field_list:
        q.children.append(Q(('{}__contains'.format(field), query)))
    return q


# 展示文章列表
def article_list(request):
    # all_articles = models.Article.objects.all()
    q = get_query(request, ['title', 'abstract'])
    all_articles = models.Article.objects.filter(author=request.user_obj).filter(q)
    page = Pagination(request, all_articles.count())
    return render(request, 'article_list.html',
                  {'all_articles': all_articles[page.start: page.end] if all_articles else None,
                   'page_html': page.page_html})


# 新增文章
def article_add(request):
    article_obj = models.Article(author=request.user_obj)
    form_obj = ArticleForm(instance=article_obj)
    article_detail_form_obj = ArticleDetailForm()
    if request.method == 'POST':
        form_obj = ArticleForm(request.POST, instance=article_obj)
        article_detail_form_obj = ArticleDetailForm(request.POST)
        if form_obj.is_valid() and article_detail_form_obj.is_valid():
            # detail = request.POST.get("detail")
            # detail_obj = models.ArticleDetail.objects.create(content=detail)
            detail_obj = article_detail_form_obj.save()
            form_obj.instance.detail_id = detail_obj.pk
            form_obj.save()

            return redirect('article_list')
    return render(request, 'article_add.html',
                  {'form_obj': form_obj, 'article_detail_form_obj': article_detail_form_obj})


# 编辑文章
def article_edit(request, pk):
    article_obj = models.Article.objects.filter(pk=pk).first()
    form_obj = ArticleForm(instance=article_obj)
    article_detail_form_obj = ArticleDetailForm(instance=article_obj.detail)
    if request.method == "POST":
        form_obj = ArticleForm(request.POST, instance=article_obj)
        article_detail_form_obj = ArticleDetailForm(request.POST, instance=article_obj.detail)
        if form_obj.is_valid() and article_detail_form_obj.is_valid():
            # form_obj.instance.detail.content = request.POST.get("detail")
            # form_obj.instance.detail.save()
            article_detail_form_obj.save()
            form_obj.save()
            return redirect('article_list')
    return render(request, 'article_edit.html',
                  {'form_obj': form_obj, 'article_detail_form_obj': article_detail_form_obj})


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 加密
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        user_obj = models.User.objects.filter(username=username, password=md5.hexdigest()).first()
        if user_obj:
            # 登陆成功
            # 保存登录状态 用户名
            request.session['is_login'] = True
            request.session['username'] = user_obj.username
            request.session['pk'] = user_obj.pk

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
    # is_login = request.session.get('is_login')
    # username = request.session.get('username')
    # user_obj = models.User.objects.filter(pk=request.session.get('pk')).first()
    page = Pagination(request, all_articles.count(), clazz="pagination", per_num=5)
    return render(request, 'index.html',
                  {'all_articles': all_articles[page.start: page.end], 'page_html': page.page_html})


def article(request, pk):
    article_obj = models.Article.objects.get(pk=pk)
    return render(request, 'article.html', {'article_obj': article_obj})


def backend(request):
    return render(request, 'dashboard.html')


def register(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST, request.FILES)
        if form_obj.is_valid():
            # form_obj.cleaned_data.pop('re_password')
            # models.User.objects.create(**form_obj.cleaned_data)
            form_obj.save()
            return redirect('login')
    return render(request, 'register.html', {'form_obj': form_obj})


def category_list(request):
    q = get_query(request, ['title'])
    all_categories = models.Category.objects.filter(q)
    page = Pagination(request, all_categories.count())
    return render(request, 'category_list.html',
                  {"all_categories": all_categories[page.start: page.end], "page_html": page.page_html})


def category_add(request):
    form_obj = CategoryForm()
    if request.method == 'POST':
        form_obj = CategoryForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('category_list')
    title = '新增板块'
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})


def category_edit(request, pk):
    category_obj = models.Category.objects.filter(pk=pk).first()
    form_obj = CategoryForm(instance=category_obj)
    if request.method == 'POST':
        form_obj = CategoryForm(request.POST, instance=category_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('category_list')
    title = '编辑板块'
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})


def category_change(request, pk=None):
    category_obj = models.Category.objects.filter(pk=pk).first()
    form_obj = CategoryForm(instance=category_obj)
    if request.method == 'POST':
        form_obj = CategoryForm(request.POST, instance=category_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('category_list')
    title = '编辑板块' if pk else '新增分类'
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})

# users = [{"name": 'Obser-{}'.format(i), 'password': '123'} for i in range(1, 446)]
# def user_list(request):
#     page = Pagination(request, len(users))
#     return render(request, 'user_list.html',
#                   {'users': users[page.start: page.end], 'page_html': page.page_html})
