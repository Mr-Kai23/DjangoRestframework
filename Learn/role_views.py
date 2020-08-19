
import json
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Role
from .serializers import RoleSerializer


class RoleView(APIView):
    """
    角色视图
    """
    def get(self, request, *args, **kwargs):

        # 方法一：
        # values()获取成字典形式，再将数据json.dumps()返回
        # json.dumps()只能处理python的基本类型数据，不能直接处理queryset
        roles = Role.objects.all().values('id', 'title')

        # ensure_ascii=False，关闭自动将中文转码
        res = json.dumps(list(roles), ensure_ascii=False)

        # 方法二：
        serializer = RoleSerializer(instance=roles, many=True)
        # serializer.data是一个有序字典
        res1 = json.dumps(serializer.data, ensure_ascii=False)

        # 用 Response 不需要json.dumps()，因为 Response 中封装了序列化方法
        # return Response(serializer.data, status=status.HTTP_200_OK)

        return HttpResponse(res1)


# =================================================================
# 分页视图
# =================================================================
from .serializers import RoleSerializer, RoleSerializer2
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class MyPageNumberPagination(PageNumberPagination):
    """
    自定义分页配置类
    重写一些配置项
    分页，看第n页，每页显示n条数据
    """
    page_size = 2  # 每页数据数量
    page_size_query_param = 'size'  # 路由中分页可传的参数，表示可以传一个size的参数，每个页面的数据量
    max_page_size = 8  # 最大每页数据数量

    page_query_param = 'page'  # 传入的页码参数


class MyLimitOffsetPagination(LimitOffsetPagination):
    """
    自定义分页配置类
    重写一些配置项
    分页，在n个位置，向后查看n条数据
    """
    default_limit = 2  # 每页数据数量
    limit_query_param = 'limit'  # 每个页面的限定数据量参数
    max_limit = 8  # 最大每页数据数量

    offset_query_param = 'offset'  # 传入的起始数据的索引参数


class MyCursorPagination(CursorPagination):
    """
    自定义加密分页类
    重写一些配置项
    分页，加密分页，上一页下一页
    """
    cursor_query_param = 'cursor'  # 分页页码加密查询参数
    page_size = 2  # 单页显示数据数量
    ordering = 'id'  # 定义默认排序字段
    max_page_size = 8  # 最大每页数据数量

    page_size_query_param = 'size'  # 单页显示数据数量查询参数


class Pager1View(APIView):
    """
    分页视图
    """
    def get(self, request, *args, **kwargs):

        roles = Role.objects.all()

        # 分页实例
        # 1.
        # pagination = PageNumberPagination()  # page参数：页码，size参数：单页数据量
        # pagination = MyPageNumberPagination()
        # 2.
        pagination = LimitOffsetPagination()  # offset参数：起始数据的索引，limit参数：单页面限定展示的数据量
        # pagination = MyLimitOffsetPagination()
        # 3.
        # pagination = CursorPagination()
        # pagination = MyCursorPagination()

        # 传入 queryset 、 请求 对象 和 视图对象（也就是当前视图对象，self）(可写可不写)
        pager_roles = pagination.paginate_queryset(queryset=roles, request=request, view=self)

        # 序列化分页后的数据
        # serializer = RoleSerializer(instance=pager_roles, many=True)
        serializer = RoleSerializer2(instance=pager_roles, many=True)

        # return Response(data=serializer.data)

        # 返回分页自动生成的响应,第1、2种可以适用两种返回形式，第3种分页，只适合以下返回形式
        return pagination.get_paginated_response(data=serializer.data)

