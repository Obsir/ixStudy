"""ixStudy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from app01 import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^index/$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^article/(\d+)$', views.article, name='article'),
    url(r'^article_edit/(\d+)$', views.article_edit, name='article_edit'),
    url(r'^backend/$', views.backend, name='backend'),
    url(r'^article_list/$', views.article_list, name='article_list'),
    url(r'^article_add/$', views.article_add, name='article_add'),
    # url(r'^user_list/$', views.user_list, name='user_list'),
    url(r'^category_list/$', views.category_list, name='category_list'),
    url(r'^category_add/$', views.category_change, name='category_add'),
    url(r'^category_edit/(\d+)$', views.category_change, name='category_edit'),
    url(r'^comment/$', views.comment, name='comment'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^series_list/$', views.series_list, name='series_list'),
    url(r'^series_add/$', views.series_change, name='series_add'),
    url(r'^series_edit/(\d+)$', views.series_change, name='series_edit'),
    url(r'^point/$', views.point, name='point'),
]
