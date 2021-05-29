from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, reverse
import re
from django.conf import settings
from app01 import models


class AuthMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        # 需要登录后访问地址 需要判断登录状态
        # 默认所有的地址都要登录才能访问
        # 设置一个白名单 不登录就能访问
        url = request.path_info

        # 校验登录状态
        is_login = request.session.get('is_login')
        if is_login:
            # 已经登录可以访问
            user_obj = models.User.objects.filter(pk=request.session.get('pk')).first()
            request.user_obj = user_obj
            return

        for reg in settings.WHITE_LIST:
            if re.match(reg, url):
                return

        # 没有登陆，需要登录
        return redirect("{}?url={}".format(reverse('login'), url))
