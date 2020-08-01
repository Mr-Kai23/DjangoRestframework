from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from Learn.models import User, Token


def md5(user):
    import hashlib
    import time

    ctime = str(time.time())

    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime))

    return m.haxdigest()


class TokenAuthentication:
    """
    用户登录验证
    """
    def authenticate(self, request):

        token = request._request.GET.get('token', None)
        token_obj = Token.objects.filter(token=token)

        if not token_obj:
            raise AuthenticationFailed('用户没有登陆！')

        # 返回请求用户，token对象
        return (token_obj.user, token_obj)

    def authenticate_header(self):
        pass


class AuthView(APIView):

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
