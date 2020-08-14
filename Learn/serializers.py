
from rest_framework import serializers
from .models import UserGroup, Role, User


class RoleSerializer(serializers.Serializer):
    """
    角色序列化类
    """
    id = serializers.IntegerField()
    title = serializers.CharField()


class UserInfoSerializer(serializers.Serializer):
    """
    用户信息序列化类
    """
    # source指定用于填充user_type的字段
    # user_type = serializers.IntegerField(source='user_type')
    usertype = serializers.IntegerField(source='get_user_type_display')  # 不用加括号，源码中会执行
    username = serializers.CharField()
    password = serializers.CharField()

    gp = serializers.CharField(source='usergroup.title')

    # 用户关联的所有角色，ManyToMany字段
    # 1.
    # roles = serializers.CharField(source='roles.all')  # 只能获取角色对象，不能获取到对象的具体信息
    # 2.
    rls = serializers.SerializerMethodField()  # 自定义函数用于显示

    def get_rls(self, row):
        """
        定义名字为 get_+字段名（rls）的方法，用于自定义显示
        :param row: 当前行的对象
        :return:
        """
        # 当前行获取rls的所有值
        role_obj_list = row.rls.all()
        res = []

        for role in role_obj_list:
            res.append({'id': role.id, 'title': role.title})

        return res


class UserInfoSerializer2(serializers.ModelSerializer):
    """
    用户信息序列化类
    """
    usertype = serializers.CharField(source='get_user_type_display')

    rls = serializers.SerializerMethodField()

    def get_rls(self, row):
        """
        定义名字为 get_+字段名（rls）的方法，用于自定义显示
        :param row: 当前行的对象
        :return:
        """
        role_obj_list = row.roles.all()
        res = []

        for role in role_obj_list:
            res.append({'id': role.id, 'title': role.title})

        return res

    class Meta:
        model = User
        # fields = '__all__'
        # 可以将上方定义的usertype当做字段写入列表中用于显示
        fields = ['id', 'username', 'password', 'usertype', 'group', 'rls']
        # 给列表中的 group字段加额外的参数，让 group 字段显示为组名
        extra_kwargs = {'group': 'value'}