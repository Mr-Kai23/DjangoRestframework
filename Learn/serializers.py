
from rest_framework import serializers
from .models import UserGroup, Role, User

# 序列化功能：
# 1.序列化数据
# 2.对数据进行验证


# =============================================================
# 角色序列化类
# =============================================================
class RoleSerializer(serializers.Serializer):
    """
    角色序列化类
    定义想要序列化的字段
    """
    id = serializers.IntegerField()
    title = serializers.CharField()


class RoleSerializer2(serializers.ModelSerializer):
    """
    角色序列化类
    直接在元中定义所有字段
    """

    class Meta:

        model = Role
        fields = '__all__'


# ============================================================
# 用户信息序列化类
# ============================================================
class UserInfoSerializer(serializers.Serializer):
    """
    用户信息序列化类
    """
    # 有choice的字段，可以source指定用于填充user_type的内容
    # user_type = serializers.IntegerField(source='user_type')
    user_type = serializers.CharField(source='get_user_type_display')  # 不用加括号，源码中会执行
    username = serializers.CharField()
    password = serializers.CharField()

    # 外键， group.title中group为模型中的外键group字段
    group = serializers.CharField(source='group.title')

    # 用户关联的所有角色，ManyToMany字段
    # 1.
    # roles = serializers.CharField(source='roles.all')  # 只能获取角色对象，不能获取到对象的具体信息
    # 2. 用户信息中的roles字段
    roles = serializers.SerializerMethodField()  # 自定义函数用于显示

    def get_roles(self, row):
        """
        定义名字为 get_+字段名（roles）的方法，用于自定义显示
        :param row: 当前行的对象
        :return:
        """
        # 当前行获取roles(与模型中字段一致)的所有值
        role_obj_list = row.roles.all()
        res = []

        for role in role_obj_list:
            res.append({'id': role.id, 'title': role.title})

        return res


class UserInfoSerializer2(serializers.ModelSerializer):
    """
    用户信息序列化类
    """
    user_type = serializers.CharField(source='get_user_type_display')

    # 将group字段自定义为一个链接
    # view_name: 表示关联到视图group-list
    # lookup_field: 表示拿到数据，group_id:表示是外键group关联对象的id
    # lookup_url_kwarg: 定义的是url中的参数名
    group = serializers.HyperlinkedIdentityField(view_name='group-list', lookup_field='group_id', lookup_url_kwarg='pk')

    # group = serializers.SerializerMethodField()
    #
    # def get_group(self, row):
    #     """
    #
    #     :param row: 当前行的对象
    #     :return:
    #     """""
    #     obj = row.group
    #     ret = []
    #
    #     ret.append({'id': obj.id, 'title': obj.title})
    #
    #     return ret

    roles = serializers.SerializerMethodField()

    def get_roles(self, row):
        """
        定义名字为 get_+字段名（roles）的方法，用于自定义显示
        :param row: 当前行的对象
        :return:
        """
        role_obj_list = row.roles.all()
        ret = []

        for item in role_obj_list:
            ret.append({'id': item.id, 'title': item.title})

        return ret

    class Meta:
        model = User
        # fields = '__all__'
        # 可以将上方定义的user_type当做字段写入列表中用于显示
        fields = ['id', 'username', 'password', 'user_type', 'group', 'roles']
        # 给列表中的 group字段加额外的参数，让 group 字段显示为组名
        # extra_kwargs = {'group': 'value'}

        # 表示对外键拿数据的深度（连表操作），取值范围0~n， 建议：0~4层
        # depth = 0:表示只是展示出User表中的数据（默认）
        # depth = 1:表示不只展示出User表中的数据，还会去外键对应的表中拿出关联对象的所有数据
        # depth = 1


# =============================================================
# 用户组序列化类
# =============================================================
from .validators import PasswordValidator


class GroupSerializer(serializers.Serializer):
    """
    Serializer 分组序列化
    """
    # validators: 自定义验证规则
    title = serializers.CharField(error_messages={'required': '标题不能为空！'}, validators=[PasswordValidator('老男人')])  # 数据校验

    def validate_title(self, value):
        """
        可以自己定义验证方法，名字为 validate_+字段名
        :param value: 使用的时候实例化时，传入的数据
        :return: 验证处理后的数据或触发一个异常
        """
        # 1.返回验证后的值
        # return value

        # 2.触发异常，
        from rest_framework.exceptions import ValidationError

        raise ValidationError('验证有误')


class GroupSerializer2(serializers.ModelSerializer):
    """
    ModelSerializer 分组序列化
    """

    class Meta:
        model = UserGroup
        field = ['id', 'title']
        # fields = '__all__'

