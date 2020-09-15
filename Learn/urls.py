from django.conf.urls import url, include
from rest_framework import routers
from Learn import views, user_views, role_views, group_views


# =================================================================
# 路由组件
# 自动生成路由
# =================================================================
# 继承了GenericViewSet有关视图的视图类可以自动生成路由
# 根据视图名称自动生成路由
# 生成的路由也能在参数中直接加格式化表示，1：为ID
# http://127.0.0.1:8000/api/v1/group/1.json
router = routers.DefaultRouter()
# users为路由前缀
router.register(r'users', role_views.View2View)


urlpatterns = [

    # url(r'^api/user/$', user_views.UserView.as_view(), name='user-list'),

    url(r'^api/(?P<version>[v1|v2]+)/user/$', user_views.UserView.as_view(), name='user-list'),
    url(r'^api/(?P<version>[v1|v2]+)/parse/$', views.ParseView.as_view(), name='parse'),
    url(r'^api/(?P<version>[v1|v2]+)/roles/$', role_views.RoleView.as_view(), name='roles-list'),
    url(r'^api/(?P<version>[v1|v2]+)/userinfo/$', user_views.UserInfoView.as_view(), name='userinfo-list'),
    url(r'^api/(?P<version>[v1|v2]+)/group/(?P<pk>\d+)/$', group_views.GroupView.as_view(), name='group-list'),

    # 可以在路由上加格式化对结果进行格式化
    # http://127.0.0.1:8000/api/v1/group/1.json
    url(r'^api/(?P<version>[v1|v2]+)/group/(?P<pk>\d+)\.(?P<format>\w+)/$', group_views.GroupView.as_view(), name='group-list'),

    url(r'^api/(?P<version>[v1|v2]+)/pager1/$', role_views.Pager1View.as_view(), name='pager1-list'),

    # 视图组件
    url(r'^api/(?P<version>[v1|v2]+)/view1/$', role_views.View1View.as_view(), name='view1-list'),
    # 将get方法映射为list方法
    url(r'^api/(?P<version>[v1|v2]+)/view2/$', role_views.View2View.as_view({'get': 'list'}), name='view2-list'),

    # 所有url前缀
    # 或自动生成跟视图函数中请求方法相应的路由
    url(r'api/(?P<version>[v1|v2]+)/', include(router.urls)),

    # 渲染器组件
    url(r'^api/(?P<version>[v1|v2]+)/render/$', role_views.RenderView.as_view(), name='render')

]