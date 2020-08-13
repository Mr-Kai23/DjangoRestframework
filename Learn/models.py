from django.db import models


# Create your models here.
class User(models.Model):
    USER_TYPE = (
        (1, '普通用户'),
        (2, 'VIP'),
        (3, 'SVIP')
    )
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=25)
    user_type = models.SmallIntegerField(choices=USER_TYPE)

    group = models.ForeignKey('UserGroup', on_delete=models.CASCADE)
    roles = models.ManyToManyField('Role')

    class Meta:
        db_table = 'User'


class Token(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    token = models.CharField(max_length=50)

    class Meta:
        db_table = 'token'


class UserGroup(models.Model):
    title = models.CharField(max_length=32)

    class Meta:
        db_table = 'user_group'


class Role(models.Model):
    title = models.CharField(max_length=32)

    class Meta:
        db_table = 'role'



