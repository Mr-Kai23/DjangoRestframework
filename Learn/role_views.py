
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