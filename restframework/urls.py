"""restframework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
# from rest_framework import serializers, routers, viewsets
# from django.contrib.auth.models import User


# # 序列化程序定义API表示形式
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'is_staff']
#
#
# # ViewSet 定义视图行为
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# 路由器提供了一种自动确定URL conf的简便方法
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)


# 使用自动URL路由连接我们的API
# 此外，我们包括可浏览API的登录URL
urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^', include(router.urls)),
    # 可浏览API的登录和注销视图
    # path('api-auth/', include('rest_framework.urls')),
    path('snippets/', include('snippets.urls')),
    path('quickstart/', include('quickstart.urls')),
    path('learn/', include('Learn.urls'))
]
