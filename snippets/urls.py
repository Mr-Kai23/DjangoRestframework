from django.conf.urls import url
from snippets import views

urlpatterns = [

    url(r'^list/$', views.snippet_list, name='snippet-list'),
    url(r'^detail/(?P<pk>[1-9]+)/$', views.snippet_detail, name='snippet-detail')

]