from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
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