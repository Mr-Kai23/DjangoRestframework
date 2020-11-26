from django.urls import path, include
from rest_framework import routers
from quickstart import views
from django.conf.urls import url

# 路由组件，自动生成路由
# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    # 方法一：使用路由组件自动生成路由
    # 配合路由组件一起反向生成路由
    # path('', include(router.urls)),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    # 方法二：配置路由
    # 配置路由，将get方法映射到视图中list方法
    url(r'^api/v2/user/(?P<pk>\d+)/$', views.UserViewSet.as_view({'get': 'list'}), name='')
]