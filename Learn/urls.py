from django.conf.urls import url
from Learn import views, user_views

urlpatterns = [

    url(r'^api/v1/auth/$', user_views.snippet_list, name='snippet-list'),

]