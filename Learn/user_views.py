from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
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
        self.dispatch()
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


class OrderView(APIView):
    """
    订单视图
    """

    # SVIP权限
    permission_classes = [SVIPPermission]
    throttle_classes = [VisitThrottle]

    def get(self, request, *args, **kwargs):
        return HttpResponse('')
