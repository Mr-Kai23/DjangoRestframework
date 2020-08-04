from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from django.http import HttpResponse
import json

# Create your views here.


# 对用户Token的验证
# 认证类最好（必须）继承BaseAuthentication
class TokenAuthentication(BaseAuthentication):
    """
    用户认证：
    认证用户是否登录

    """

    www_authenticate_realm = 'api'

    def authenticate(self, request):
        """
        执行认证类的authenticate()方法
            # 1.如果抛出异常，执行自身的_not_authenticated()
            # 2.如果返回元组
            # 3.返回None，我不管，下一个认证来处理
        如果都返回None则，返回匿名用户
            给user和auth赋默认值，user:匿名用户， auth

        扩展：
        在BasicAuthentication认证中，
        如果不允许匿名用户，可以抛出 AuthenticationFailed 异常
        此时浏览器会提供用户认证机制，弹出 用户名和密码框，然后把数据加密后传到服务器
        :param request:
        :return:
        """

        # 验证用户是否登录
        # 也可以获取用户数据去数据库匹配验证
        token = request._request.GET.get('token', None)

        if not token:
            raise AuthenticationFailed('用户没有登录！')

        return ('用户', token)  # 将用户和token的元组返回，或返回None

    def authenticate_header(self, request):
        """
        认证失败时，返回的响应头信息
        :param request:
        :return:
        """
        return 'Basic realm="%s"' % self.www_authenticate_realm


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