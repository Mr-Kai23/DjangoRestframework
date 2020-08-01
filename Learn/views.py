from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpResponse
import json

# Create your views here.


# 对用户Token的验证
class TokenAuthentication:
    """
    认证可以返回三种类型的值
    """
    def authenticate(self, request):

        # 验证用户是否登录
        # 也可以获取用户数据去数据库匹配验证
        token = request._request.GET.get('token', None)

        if not token:
            raise AuthenticationFailed('用户没有登录！')

        return ('name', None)  # 可以将数据库的数据返回，比如用户名等

    def authenticate_header(self, val):
        pass


# APIView 继承的 View
class StudentViews(APIView):

    # 全局使用验证：
    # 验证类列表写在配置文件中，名为 REST_FRAMEWORK 的字典中的键为
    # DEFAULT_AUTHENTICATION_CLASSES 的值（值为列表）中，这类设置会给全局视图类加上验证，
    # 如果某个类不需要验证，在类中定义一个 authentication_classes = [] 空列表
    # 局部使用验证：
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        # # 源码阅读从dispatch()开始，将原始request丰富了新的属性，在属性中进行了用户验证
        self.dispatch()
        # print(request.user)  # 验证后返回的 name
        res = {
            'code': 1000,
            'msg': ''
        }

        return HttpResponse(json.dumps(res), status=201)

    def post(self, request):

        return HttpResponse('创建Student')

    def put(self, request):

        return HttpResponse('修改Student')

    def delete(self, request):

        return HttpResponse('删除Student')