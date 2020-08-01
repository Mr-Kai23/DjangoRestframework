from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from Learn.models import User, Token


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


class TokenAuthentication(BaseAuthentication):
    """
    用户登录验证
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

        token = request._request.GET.get('token', None)
        token_obj = Token.objects.filter(token=token)

        if not token_obj:
            raise AuthenticationFailed('用户没有登陆！')

        # 返回请求用户，token对象
        return (token_obj.user, token_obj)

    def authenticate_header(self, request):
        """
        认证失败时，返回的响应头信息
        :param request:
        :return:
        """
        return 'Basic realm="%s"' % self.www_authenticate_realm


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

    def post(self, request, *args, **kwargs):

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


class OrderView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('')
