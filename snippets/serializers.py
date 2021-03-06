
# 开发我们的Web API的第一件事是为我们的Web API提供一种将代码片段
# 实例序列化和反序列化为诸如json之类的表示形式的方式
# 可以通过声明与Django forms非常相似的序列化器（serializers）来实现
from rest_framework import serializers
from django.contrib.auth.models import User
# 序列化为 JSON格式（字节串）
from rest_framework.renderers import JSONRenderer
# 要通过 BytesIO 将 JSON格式（字节串）包装，才能用JSONParser解析
from rest_framework.parsers import JSONParser
from snippets.models import Snippets, LANGUAGE_CHOICES, STYLE_CHOICES

# 可以通过打印序列化器类实例的结构(representation)查看它的所有字段

# SnippetSerializer 和 SnippetSerializer2的作用是一样的


# 序列化一个实例，data属性是一个 Dict;
# 序列化一个queryset，data属性是一个 OrderedDict
class SnippetSerializer(serializers.Serializer):
    """
    定义序列化类，用来序列化对应的 Model 实例
    也可以通过使用ModelSerializer类来节省时间
    serializer的field不仅在进行数据验证时起着至关重要的作用，
    在将数据进行序列化后返回也发挥着重要作用
    """

    # 1.定义了序列化 / 反序列化的字段
    # 序列化器类与Django Form类非常相似，并在各种字段中包含类似的验证标志
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    # 字段标志还可以控制serializer在某些情况下如何显示，比如渲染HTML的时候
    # {'base_template': 'textarea.html'}等同于在Django Form类中使用widget=widgets.Textarea
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    # create()和update()方法定义了在调用serializer.save()时如何创建和修改完整的实例
    # post 请求会执行增加方法
    def create(self, validated_data):
        """
        根据提供的验证过的数据创建并返回一个新的`Snippet`实例。
        """
        return Snippets.objects.create(**validated_data)

    # patch/put 请求会执行的更新方法
    def update(self, instance, validated_data):
        """
        根据提供的验证过的数据更新和返回一个已经存在的`Snippet`实例。
        """

        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()

        return instance


# ModelSerializer类并不会做任何特别神奇的事情，它们只是创建序列化器类的快捷方式：
#   一组自动确定的字段。
#   默认简单实现的create()和update()方法
class SnippetSerializer2(serializers.ModelSerializer):
    """
    Snippets序列化类
    """

    class Meta:
        model = Snippets  # 关联的模型
        # 需要序列化的字段
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')


# 实体之间使用超链接方式。这样的话，我们需要修改我们的序列化程序来扩展HyperlinkedModelSerializer
# 而不是现有的ModelSerializer。
# HyperlinkedModelSerializer与ModelSerializer有以下区别：
#   默认情况下不包括id字段。
#   它包含一个url字段，使用HyperlinkedIdentityField。
#   关联关系使用HyperlinkedRelatedField，而不是PrimaryKeyRelatedField
class SnippetsSerializer3(serializers.HyperlinkedModelSerializer):
    """
    代码片段序列化
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    # 定义用户信息中highlight字段为超链接字段，关联到snippet-highlight视图，高亮显示
    # 因为我们已经包含了格式后缀的URL，例如'.json'，我们还需要在highlight字段上指出任何格式后缀的超链接，
    # 它应该使用'.html'后缀。
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippets
        fields = ('url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style')


class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化类
    """
    # 代码片段和创建它们的用户相关联
    # source参数控制哪个属性用于填充字段（相当于外键关联），并且可以指向序列化实例上的任何属性
    # 无类型的ReadOnlyField始终是只读的，只能用于序列化表示，不能用于在反序列化时更新模型实例
    # 可以在这里使用CharField(read_only=True)。
    # owner = serializers.CharField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    # 用户管关联到的代码片段
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippets.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')


class UserSerializer2(serializers.HyperlinkedModelSerializer):
    """
    用户序列化
    """
    # 定义用户信息中snippets字段为超链接字段，关联到snippet-detail视图
    # view_name:关联的视图
    snippets = serializers.HyperlinkedRelatedField(view_name='snippet-detail', many=True, read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets')
