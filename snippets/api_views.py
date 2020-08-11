
# 将使用一个常规的基于函数的视图和我们前面介绍的@api_view装饰器创建一个API入口点
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request, format=None):
    """
    api路径创建
    使用REST框架的reverse功能来返回完全限定的URL
    URL模式是通过方便的名称来标识的
    :param request:
    :param format:
    :return: 返回Json格式数据，键值为users和snippets,值为user-list与snippet-list的路由
    """

    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })