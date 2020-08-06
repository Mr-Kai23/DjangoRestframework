
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer


class UserListView(generics.ListAPIView):
    """
    列出所有的user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    """
     检索snippet示例。
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer