from django.conf.urls import url
from Learn import views, user_views

urlpatterns = [

    # url(r'^api/user/$', user_views.UserView.as_view(), name='user-list'),

    url(r'^api/(?P<version>[v1|v2]+)/user/$', user_views.UserView.as_view(), name='user-list'),
    url(r'^api/(?P<version>[v1|v2]+)/parse/$', views.ParseView.as_view(), name='parse'),

]