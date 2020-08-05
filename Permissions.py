from rest_framework.permissions import BasePermission


class SVIPPermission(BasePermission):
    """
    SVIP权限
    """

    # 源码中 getattr(permission, 'message', None)获取权限类中的message属性
    # 自定义权限异常信息
    message = '只有SVIP可访问！'

    def has_permission(self, request, view):
        """
        是否有全新
        :param request: 请求
        :param view: 视图
        :return: 返回 True 或 False
        """

        # 当用户不为SVIP时，没有权限访问
        if request.user.user_type != 3:
            return False

        return True


class SomePermission(BasePermission):
    """
    其他权限
    """

    # 源码中 getattr(permission, 'message', None)获取权限类中的message属性
    # 自定义权限异常提示信息
    message = '提示信息！'

    def has_permission(self, request, view):
        """
        是否有全新
        :param request: 请求
        :param view: 视图
        :return: 返回 True 或 False
        """

        return True