from django.urls import path, include
from rest_framework import routers
from quickstart import views
from django.conf.urls import url


# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    # path('', include(router.urls)),
    # path('api-auth', include('rest_framework.urls', namespace='rest_framework'))
    url(r'^api/v2/user/(?P<pk>\d+)/$', views.UserViewSet.as_view({'get': 'list'}), name='')
]