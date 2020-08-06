from django.conf.urls import url
from snippets import views, user_views
from rest_framework.urlpatterns import format_suffix_patterns

# urlpatterns = [
#
#
#
# ]

urlpatterns = [

    url(r'^user/api/v1/$', user_views.UserListView.as_view(), name='user-list'),
    url(r'^user/detail/(?P<pk>[1-9]+)/api/v1/$', user_views.UserDetailView.as_view(), name='user-detail'),

    # url(r'^list/api/v1$', views.snippet_list, name='snippet-list'),
    # url(r'^detail/(?P<pk>[1-9]+)/api/v1$', views.snippet_detail, name='snippet-detail'),

    # url(r'^list/api/v1$', views.SnippetsListView.as_view(), name='snippet-list'),
    # url(r'^detail/(?P<pk>[1-9]+)/api/v1$', views.SnippetsDetailView.as_view(), name='snippet-detail'),

    url(r'^list/api/v1/$', views.SnippetsListView1.as_view(), name='snippet-list'),
    url(r'^detail/(?P<pk>[1-9]+)/api/v1/$', views.SnippetsDetailView1.as_view(), name='snippet-detail'),

    # url(r'^list/api/v1$', views.SnippetsListView1=2.as_view(), name='snippet-list'),
    # url(r'^detail/(?P<pk>[1-9]+)/api/v1$', views.SnippetsDetailView2.as_view(), name='snippet-detail'),

]

# 路由后缀配置
urlpatterns = format_suffix_patterns(urlpatterns)