
from rest_framework import serializers
# 序列化验证处理类


class PasswordValidator(object):

    def __init__(self, base):
        self.base = base

    def __call__(self, value, *args, **kwargs):
        """
        数据一提交过来，就会执行__call__方法
        :param value: 提交过来的值
        :param args:
        :param kwargs:
        :return:
        """

        if not value.startswith(self.base):
            message = 'This field must be %s' % self.base

            raise serializers.ValidationError(message)
