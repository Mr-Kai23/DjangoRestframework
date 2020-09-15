
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserGroup
from .serializers import GroupSerializer, GroupSerializer2


class GroupView(APIView):
    """
    分组视图
    """
    def get(self, request, *args, **kwargs):
        """
        获取分组信息
        :param request: 请求对象
        :param args: 不定项参数
        :param kwargs: 关键字参数，可以获取路由中定义关键字参数
        :return:
        """
        pk = kwargs.get('pk', None)

        group = UserGroup.objects.filter(pk=pk).first()

        serializer = GroupSerializer(instance=group)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        创建数据
        :param request: 请求对象
        :param args: 不定项参数
        :param kwargs: 关键字参数，可以获取路由中定义关键字参数
        :return:
        """
        serializer = GroupSerializer(data=request.data)

        if serializer.is_valid():  # 钩子函数的入口
            serializer.save()

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
