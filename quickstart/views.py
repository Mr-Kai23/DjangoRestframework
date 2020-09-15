from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
from quickstart.serializers import UserSerializer, GroupSerializer
from rest_framework import viewsets
from rest_framework.response import Response

# Create your views here.


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     允许查看或编辑用户的API端点
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer


class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)

        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    """
    允许查看或编辑分组的API端点
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
