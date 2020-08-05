
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from Learn.models import Token


# 对用户Token的验证
# 认证类最好（必须）继承BaseAuthentication
# class TokenAuthentication(BaseAuthentication):
#     """
#     用户认证：
#     认证用户是否登录
#
#     """
#
#     www_authenticate_realm = 'api'
#
#     def authenticate(self, request):
#         """
#         执行认证类的authenticate()方法
#             # 1.如果抛出异常，执行自身的_not_authenticated()
#             # 2.如果返回元组
#             # 3.返回None，我不管，下一个认证来处理
#         如果都返回None则，返回匿名用户
#             给user和auth赋默认值，user:匿名用户， auth
#
#         扩展：
#         在BasicAuthentication认证中，
#         如果不允许匿名用户，可以抛出 AuthenticationFailed 异常
#         此时浏览器会提供用户认证机制，弹出 用户名和密码框，然后把数据加密后传到服务器
#         :param request:
#         :return:
#         """
#
#         # 验证用户是否登录
#         # 也可以获取用户数据去数据库匹配验证
#         token = request._request.GET.get('token', None)
#
#         if not token:
#             raise AuthenticationFailed('用户没有登录！')
#
#         return ('用户', token)  # 将用户和token的元组返回，或返回None
#
#     def authenticate_header(self, request):
#         """
#         认证失败时，返回的响应头信息
#         :param request:
#         :return:
#         """
#         return 'Basic realm="%s"' % self.www_authenticate_realm


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