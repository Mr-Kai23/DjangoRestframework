from rest_framework.views import APIView
from utils.Authentications import TokenAuthentication
from utils.Permissions import SVIPPermission
from django.http import HttpResponse
import json

# Create your views here.


# APIView 继承的 View
class StudentViews(APIView):

    # 全局使用验证：
    # 验证类列表写在配置文件中，名为 REST_FRAMEWORK 的字典中的键为
    # DEFAULT_AUTHENTICATION_CLASSES 的值（值为列表）中，这类设置会给全局视图类加上验证，
    # 如果某个类不需要验证，在类中定义一个 authentication_classes = [] 空列表
    # 局部使用验证：
    authentication_classes = [TokenAuthentication]
    permission_classes = [SVIPPermission]

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


from rest_framework.parsers import JSONParser, FormParser, FileUploadParser
from rest_framework.request import Request


class ParseView(APIView):
    """
    允许发送Json格式数据
      a.content-type；application/json
      b.{'name': 'alex', 'age': 25}
    """
    # 可以在settings中全局配置
    # JSONParser: 表示只能解析content-type；application/json
    # FormParser: 表示只能解析content-type；application/x-www-form-urlencoded
    # parser_classes = [JSONParser, FormParser]
    # 如果全局配置JSONParser, FormParser，单个视图要上传文件，可以单独定义parser_classes
    parser_classes = [FileUploadParser]

    def post(self, request, *args, **kwargs):

        # 只有获取请求中数据时才会去执行解析器
        print(request.data)

        return HttpResponse('请求数据')