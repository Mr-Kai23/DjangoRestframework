import time
from rest_framework.throttling import BaseThrottle, SimpleRateThrottle  # 阀值控制
from collections import defaultdict

VISIT_RECORD = defaultdict(list)


# 对匿名用户的控制
class VisitThrottle(BaseThrottle):
    """
    访问频率控制（节流）
    """
    def __init__(self):
        self.history = None  # 访问记录

    def allow_request(self, request, view):
        """
        允许请求访问阀值
        每分钟只允许固定用户访问三次
        :param request:
        :param view:
        :return:
        """
        # 访问用户IP
        # remote_addr = request.META.get('REMOTE_ADDR')
        remote_addr = self.get_ident(request)  # 获取标识（IP）
        curtime = time.time()

        # 如果没有访问记录
        # 创建第一个访问记录，将记录放进访问记录列表中（值为列表的字典）
        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr].append(curtime)

            return True

        # 获取访问记录列表
        self.history = VISIT_RECORD.get(remote_addr)

        # 当访问记录中有值，并且最早的访问记录在一分钟之前
        # 将最早的记录去除
        while self.history and self.history[0] < curtime - 60:
            self.history.pop(0)

        # 当访问记录小于三次，则可以访问
        # 且将当前访问记录加入记录列表中
        if len(self.history) < 3:
            self.history.insert(-1, curtime)

            return True

    def wait(self):
        """
        需等待多久才能访问
        :return:
        """
        ctime = time.time()

        return 60-(ctime-self.history[0])


# 基于内置的访问频率类对匿名用户的控制
class VisitThrottle2(SimpleRateThrottle):
    """
    访问评率控制
    """
    # 访问频率的键值
    scope = '用户（IP）'

    def get_cache_key(self, request, view):

        return self.get_ident(request)


# 对登录用户的控制
class UserThrottle(SimpleRateThrottle):
    """
    访问评率控制
    """
    scope = '登录用户（IP）'

    def get_cache_key(self, request, view):

        return self.get_ident(request)




