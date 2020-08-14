from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Learn.models import User, Token
from utils.Authentications import TokenAuthentication
from utils.Permissions import SVIPPermission
from utils.Throttlings import VisitThrottle


def md5(user):
    """
    生成随机token
    :param user: 用户
    :return:
    """
    import hashlib
    import time

    ctime = str(time.time())

    # 利用用户和时间生成随机token
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime))

    return m.haxdigest()


class AuthView(APIView):
    """
    验证类
    增删改查用户验证信息
    """
    # 全局使用验证：
    # 验证类列表写在配置文件中，名为 REST_FRAMEWORK 的字典中的键为
    # DEFAULT_AUTHENTICATION_CLASSES 的值（值为列表）中，这类设置会给全局视图类加上验证，
    # 如果某个类不需要验证，在类中定义一个 authentication_classes = [] 空列表
    # 局部使用验证：
    # 验证类名列表，可自定义验证类，但必须加入到列表中才有效
    authentication_classes = [TokenAuthentication]
    throttle_classes = [VisitThrottle]

    def post(self, request, *args, **kwargs):

        # # 源码阅读从dispatch()开始，将原始request丰富了新的属性，在属性中进行了用户验证
        # self.dispatch()
        # print(request.user)  # 验证后返回的 name

        res = {
            'code': 1000,
            'msg': None
        }

        try:
            username = request._request.POST.get('username', None)
            pwd = request._request.POST.get('password', None)

            user = User.objects.get(username=username, password=pwd)

            if not user:
                res['code'] = 1001
                res['msg'] = '用户名或密码错误！'

            token = md5(user)

            Token.objects.update_or_create(user=user, defaults={'token': token})

            res['token'] = token

        except Exception as e:
            res['code'] = 1002
            res['msg'] = '请求异常'
            print(e)

        return JsonResponse(res)


from rest_framework.request import Request
from rest_framework.versioning import BaseVersioning, QueryParameterVersioning, URLPathVersioning


class ParamVersion(BaseVersioning):
    """
    自定义版本处理类
    """
    def determine_version(self, request, *args, **kwargs):

        version = request.query_params.get('version', None)

        return version


class UserView(APIView):
    """
    用户视图
    """

    # 自定义版本处理类的配置
    # versioning_class = ParamVersion

    # 已有的版本处理类
    # 从请求路由参数中获取版本 http://127.0.0.1:8800/learn/user/?version=v1
    # versioning_class = QueryParameterVersioning
    # 推荐使用从请求路由参数中获取版本 http://127.0.0.1:8800/learn/v1/user/
    versioning_class = URLPathVersioning

    def get(self, request, *args, **kwargs):
        # self.dispatch()
        # version = request._request.GET.get('version', None)
        # version = request.query_params.get('version', None)

        print(request.version)
        # 获取版本处理的对象
        print(request.versioning_scheme)

        # 根据视图名，反向生成url， request中可以获取到version参数，所有不用传version
        url = request.versioning_scheme.reverse(viewname='user-list', request=request)
        print(url)

        # 要加上version参数
        url2 = reverse(viewname='user-list', kwargs={'version': 1})
        print(url2)

        return HttpResponse('用户信息')

    def post(self, request, *args, **kwargs):
        print(request._request)
        from django.core.handlers.wsgi import WSGIRequest

        return HttpResponse('Post和Body')


from .serializers import UserInfoSerializer, UserInfoSerializer2
import json


class UserInfoView(APIView):
    """
    用户信息视图
    """
    # serializer.data: 源码入口

    def get(self, request, *args, **kwargs):

        users = User.objects.all()

        # 当序列化用了HyperlinkedIdentityField时，序列化时需要加上，context参数:传入请求对象
        # 当many=True时，源码内部将queryset交给 ListSerializer类 处理
        serializer = UserInfoSerializer2(instance=users, many=True, context={'request': request})
        # serializer = UserInfoSerializer(instance=users, many=True)

        #  # ensure_ascii=False，关闭自动将中文转码
        ret = json.dumps(serializer.data, ensure_ascii=False)

        # return HttpResponse(ret)
        return Response(serializer.data, status=status.HTTP_200_OK)
