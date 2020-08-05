from django.conf.urls import url
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns

# urlpatterns = [
#
#     url(r'^list/api/v1$', views.snippet_list, name='snippet-list'),
#     url(r'^detail/(?P<pk>[1-9]+)/api/v1$', views.snippet_detail, name='snippet-detail')
#
# ]

urlpatterns = [

    url(r'^list/api/v1$', views.SnippetsListView.as_view(), name='snippet-list'),
    url(r'^detail/(?P<pk>[1-9]+)/api/v1$', views.SnippetsDetailView.as_view(), name='snippet-detail')

]

# 路由后缀配置
urlpatterns = format_suffix_patterns(urlpatterns)