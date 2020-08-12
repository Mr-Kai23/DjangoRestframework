from django.conf.urls import url
from snippets import views, user_views, api_views
from rest_framework.urlpatterns import format_suffix_patterns

# urlpatterns = [
#
#
#
# ]

urlpatterns = [

    url(r'^$', api_views.api_root),

    url(r'^user/$', user_views.UserListView.as_view(), name='user-list'),
    url(r'^user/detail/(?P<pk>[1-9]+)/$', user_views.UserDetailView.as_view(), name='user-detail'),

    # 1.
    # url(r'^list/$', views.snippet_list, name='snippet-list'),
    # url(r'^detail/(?P<pk>[1-9]+)/$', views.snippet_detail, name='snippet-detail'),

    # 2.
    url(r'^list/$', views.snippet_list1, name='snippet-list'),
    url(r'^detail/(?P<pk>[1-9]+)/$', views.snippet_detail1, name='snippet-detail'),

    # 3.
    # url(r'^list/$', views.SnippetsListView.as_view(), name='snippet-list'),
    # url(r'^detail/(?P<pk>[1-9]+)/$', views.SnippetsDetailView.as_view(), name='snippet-detail'),

    # 4.
    # url(r'^list/$', views.SnippetsListView1.as_view(), name='snippet-list'),
    # url(r'^detail/(?P<pk>[1-9]+)/$', views.SnippetsDetailView1.as_view(), name='snippet-detail'),

    url(r'^snippets/(?P<pk>[1-9]+)/highlight/$', views.SnippetsHighlightView.as_view(), name='snippet-highlight'),

    # 5.
    # url(r'^list/$', views.SnippetsListView1=2.as_view(), name='snippet-list'),
    # url(r'^detail/(?P<pk>[1-9]+)/$', views.SnippetsDetailView2.as_view(), name='snippet-detail'),

]

# 路由后缀配置
urlpatterns = format_suffix_patterns(urlpatterns)