from django.conf.urls import url
from snippets import views, user_views, api_views
from rest_framework.urlpatterns import format_suffix_patterns

# urlpatterns = [
#
#
#
# ]

urlpatterns = [

    url(r'^api/v1/$', api_views.api_root),

    url(r'^api/v1/user/$', user_views.UserListView.as_view(), name='user-list'),
    url(r'^api/v1/user/detail/(?P<pk>[1-9]+)/$', user_views.UserDetailView.as_view(), name='user-detail'),

    # url(r'^api/v1/list/$', views.snippet_list, name='snippet-list'),
    # url(r'^api/v1/detail/(?P<pk>[1-9]+)/$', views.snippet_detail, name='snippet-detail'),

    # url(r'^api/v1/list/$', views.SnippetsListView.as_view(), name='snippet-list'),
    # url(r'^api/v1/detail/(?P<pk>[1-9]+)/$', views.SnippetsDetailView.as_view(), name='snippet-detail'),

    url(r'^api/v1/list/$', views.SnippetsListView1.as_view(), name='snippet-list'),
    url(r'^api/v1/detail/(?P<pk>[1-9]+)/$', views.SnippetsDetailView1.as_view(), name='snippet-detail'),

    url(r'^api/v1/snippets/(?P<pk>[1-9]+)/highlight/$', views.SnippetsHighlightView.as_view(), name='snippet-highlight'),

    # url(r'^api/v1/list/$', views.SnippetsListView1=2.as_view(), name='snippet-list'),
    # url(r'^api/v1/detail/(?P<pk>[1-9]+)/$', views.SnippetsDetailView2.as_view(), name='snippet-detail'),

]

# 路由后缀配置
urlpatterns = format_suffix_patterns(urlpatterns)