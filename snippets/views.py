from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from snippets.models import Snippets
from snippets.serializers import SnippetSerializer, SnippetSerializer2
# Create your views here.


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# 1.数据直接返回json
@csrf_exempt
def snippet_list(request):
    """
    列出所有的code snippet，或创建一个新的snippet。
    """
    if request.method == 'GET':
        snippets = Snippets.objects.all()

        # 将 queryset 序列化后返回给用户，serializer.data是一个OrderedDict()
        # 将 单个实例 序列化后返回给用户，serializer.data是一个Dict()
        serializer = SnippetSerializer2(snippets, many=True)

        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        # JSON直接解析请求对象得到数据
        data = JSONParser().parse(request)
        # 将数据序列化，并验证
        serializer = SnippetSerializer2(data=data)

        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)

        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_detail(request, pk):
    """
    获取、删除或更新一个snippet实例
    :param request: 请求对象
    :param pk: id主键
    :return:
    """
    try:
        snippet = Snippets.objects.get(pk=pk)
    except Snippets.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer2(snippet)

        return JSONResponse(serializer.data, status=201)

    elif request.method == 'PUT':
        # 从请求中解析出数据进行修改
        data = JSONParser().parse(request)
        serializer = SnippetSerializer2(snippet, data=data)

        if serializer.is_valid():
            serializer.save()

            return JSONResponse(serializer.data)

        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()

        return HttpResponse(status=204)


# 2.数据返回显示在rest_framework后台框架页面中
@csrf_exempt
@api_view(['GET', 'POST'])  # api视图装饰器
def snippet_list1(request, format=None):
    """
    列出所有的code snippet，或创建一个新的snippet。
    """
    if request.method == 'GET':
        snippets = Snippets.objects.all()

        # 将 queryset 序列化后返回给用户，serializer.data是一个OrderedDict()
        # 将 单个实例 序列化后返回给用户，serializer.data是一个Dict()
        serializer = SnippetSerializer2(snippets, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        # JSON直接解析请求对象得到数据
        data = JSONParser().parse(request)
        # 将数据序列化，并验证
        serializer = SnippetSerializer2(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 为了充分利用我们的响应不再与单一内容类型连接，
# 我们可以为API路径添加对格式后缀的支持。
# 使用格式后缀给我们明确指定了给定格式的URL，
# 这意味着我们的API将能够处理诸如http://example.com/api/items/4.json之类的URL。
# 更新urls.py文件，给现有的URL后面添加一组format_suffix_patterns
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail1(request, pk, format=None):
    """
    获取、删除或更新一个snippet实例
    :param request: 请求对象
    :param pk: id主键
    :param format: 数据格式
    :return:
    """
    try:
        snippet = Snippets.objects.get(pk=pk)
    except Snippets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer2(snippet)

        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        # 从请求中解析出数据进行修改
        data = JSONParser().parse(request)
        serializer = SnippetSerializer2(snippet, data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.views import APIView


# 3.CBV继承APIView实现
class SnippetsListCreateView(APIView):
    """
    列出所有的snippets或者创建一个新的snippet。
    """
    # 获取所有信息
    def get(self, request, format=None):
        snippets = Snippets.objects.all()
        serializer = SnippetSerializer2(snippets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # 创建
    def post(self, request, format=None):
        # JSON直接解析请求对象得到数据
        data = JSONParser().parse(request)
        # 将数据序列化，并验证
        serializer = SnippetSerializer2(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetsDetailView(APIView):
    """
    检索，更新或删除一个snippet示例。
    """
    # 更具id获取到实例
    def get_object(self, pk):
        try:
            snippet = Snippets.objects.get(pk=pk)

            return snippet
        except Snippets.DoesNotExist:
            raise Http404

    # 单个实例的数据信息
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer2(snippet)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # 修改更新
    def put(self, request, pk, format=None):
        # data = JSONParser().parse(request)
        data = request.data
        snippet = self.get_object(pk)
        serializer = SnippetSerializer2(snippet, data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 删除
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)

        snippet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


# 4.CBV实现，直接继承多个实现单个具体功能的类
# ListModelMixin：展示
# CreateModelMixin：创建
from rest_framework import mixins, generics


# 继承前两个类后，必须继承第三个类
class SnippetsListView1(mixins.ListModelMixin, mixins.CreateModelMixin,
                        generics.GenericAPIView):
    """
    列出所有的snippets或者创建一个新的snippet。
    """

    # 变量名不能变
    queryset = Snippets.objects.all()
    serializer_class = SnippetSerializer2

    def get(self, request, *args, **kwargs):
        """
        获取所有实例数据
        :param request: 请求实例
        :param args:
        :param kwargs:
        :return:
        """

        # 调用例继承自ListModelMixin类中的list()方法获取
        return self.list(request, *args, **kwargs)  # 获取所有实例

    def post(self, request, *args, **kwargs):
        """
        创建新的实例数据
        :param request: 请求实例
        :param args:
        :param kwargs:
        :return:
        """

        # 调用例继承自CreateModelMixin类中的create()方法创建
        return self.create(request, *args, **kwargs)  # 创建新的实例


# RetrieveModelMixin：单个实例显示
# UpdateModelMixin：更新
# DestroyModelMixin：删除
class SnippetsDetailView1(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                          generics.GenericAPIView):
    """
    检索，更新或删除一个snippet示例。
    """
    queryset = Snippets.objects.all()
    serializer_class = SnippetSerializer2

    def get(self, request, *args, **kwargs):
        """
        获取单个实例数据
        :param request: 请求对象
        :param args:
        :param kwargs:
        :return:
        """

        # 调用例继承自RetrieveModelMixin类中的retrieve()方法获取
        return self.retrieve(request, *args, **kwargs)  # 获取单个实例

    def put(self, request, *args, **kwargs):
        """
        更新单个实例数据
        :param request: 请求对象
        :param args:
        :param kwargs:
        :return:
        """

        # 调用例继承自UpdateModelMixin类中的update()方法更新
        return self.update(request, *args, **kwargs)  # 更新

    def delete(self, request, *args, **kwargs):
        """
        删除单个实例数据
        :param request: 请求对象
        :param args:
        :param kwargs:
        :return:
        """

        # 调用例继承自DestroyModelMixin类中的destroy()方法删除
        return self.destroy(request, *args, **kwargs)  # 删除


# 5.CBV实现，直接继承单个实现多个具体功能的类
# ListCreateAPIView：展示和创建
class SnippetsListView2(generics.ListCreateAPIView):

    """
    列出所有的snippets或者创建一个新的snippet。
    """
    queryset = Snippets.objects.all()
    serializer_class = SnippetSerializer2

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# RetrieveUpdateDestroyAPIView：单个显示、更新和删除
class SnippetsDetailView2(generics.RetrieveUpdateDestroyAPIView):
    """
    检索，更新或删除一个snippet示例。
    """
    queryset = Snippets.objects.all()
    serializer_class = SnippetSerializer2


from rest_framework import renderers


class SnippetsHighlightView(generics.GenericAPIView):
    """
    代码高亮显示视图
    """
    queryset = Snippets.objects.all()

    # 用来渲染的类
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        # 通过queryset查找出实例
        snippet = self.get_object()

        # 不是返回对象实例，而是返回对象实例的高亮的属性
        return Response(snippet.highlighted)


