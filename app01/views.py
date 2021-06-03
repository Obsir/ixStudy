from django.shortcuts import render, redirect
from app01 import models
from app01.forms import RegForm, ArticleForm, ArticleDetailForm, CategoryForm, SeriesForm
import hashlib
from utils.pagination import Pagination
from django.db.models import Q
from django.http.response import JsonResponse
from django.utils import timezone


# 模糊搜索
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
            url = request.GET.get('url')
            if url:
                return redirect(url)
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
    comment_objs = article_obj.comment_set.filter(parent=None)
    return render(request, 'article.html', {'article_obj': article_obj, 'comment_objs': comment_objs})


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
            url = request.GET.get('url')
            if url:
                return redirect(url)
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
            url = request.GET.get('url')
            if url:
                return redirect(url)
            return redirect('category_list')
    title = '编辑板块' if pk else '新增分类'
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})


# users = [{"name": 'Obser-{}'.format(i), 'password': '123'} for i in range(1, 446)]
# def user_list(request):
#     page = Pagination(request, len(users))
#     return render(request, 'user_list.html',
#                   {'users': users[page.start: page.end], 'page_html': page.page_html})

def comment(request):
    del_comment_id = request.POST.get('del_comment_id', None)
    if del_comment_id:
        models.Comment.objects.filter(pk=del_comment_id).delete()
        return JsonResponse({'status': True})
    comment_obj = models.Comment.objects.create(**request.POST.dict())
    return JsonResponse(
        {'status': True, 'time': timezone.localtime(comment_obj.time).strftime('%Y-%m-%d %H:%M:%S'),
         'comment_id': comment_obj.pk})


def series_list(request):
    q = get_query(request, ['title'])
    all_series = models.Series.objects.filter(q)
    page = Pagination(request, all_series.count())
    return render(request, 'series_list.html',
                  {"all_series": all_series[page.start: page.end], "page_html": page.page_html})

def series_change(request, pk=None):
    series_obj = models.Series.objects.filter(pk=pk).first()
    form_obj = SeriesForm(instance=series_obj)
    if request.method == 'POST':
        form_obj = SeriesForm(request.POST, instance=series_obj)
        if form_obj.is_valid():
            # 新增系列对象
            form_obj.instance.save()
            series_obj = form_obj.instance
            # 保存系列和文章的多对多关系
            series_obj.articles.set(form_obj.cleaned_data.get('articles'))
            # 保存的系列和用户的多对多关系
            users = form_obj.cleaned_data.get('users')

            if not pk:
                # 新增
                obj_list = []
                for user in users:
                    obj_list.append(models.UserSeries(user_id=user.pk, series_id=series_obj.pk))
                if obj_list:
                    models.UserSeries.objects.bulk_create(obj_list)  # 批量插入
            else:
                # 编辑
                # 用户没有变更
                old_users = set(series_obj.users.all())
                new_users = set(users)
                # 新添加用户
                add_users = new_users - old_users
                if add_users:
                    obj_list = []
                    for user in add_users:
                        obj_list.append(models.UserSeries(user_id=user.pk, series_id=series_obj.pk))
                    if obj_list:
                        models.UserSeries.objects.bulk_create(obj_list)  # 批量插入
                # 删除用户
                del_users = old_users - new_users
                if del_users:
                    models.UserSeries.objects.filter(series_id=series_obj.pk, user_id__in=del_users).delete()

            url = request.GET.get('url')
            if url:
                return redirect(url)
            return redirect('series_list')
    title = '编辑系列' if pk else '新增系列'
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})