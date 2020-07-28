
# 开发我们的Web API的第一件事是为我们的Web API提供一种将代码片段
# 实例序列化和反序列化为诸如json之类的表示形式的方式
# 可以通过声明与Django forms非常相似的序列化器（serializers）来实现
from rest_framework import serializers
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
    # post 请求会执行
    def create(self, validated_data):
        """
        根据提供的验证过的数据创建并返回一个新的`Snippet`实例。
        """
        return Snippets.objects.create(**validated_data)

    # patch/put 请求会执行
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

    class Meta:
        model = Snippets  # 关联的模型
        # 需要序列化的字段
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')