import time
from rest_framework.throttling import BaseThrottle  # 阀值控制
from collections import defaultdict

VISIT_RECORD = defaultdict(list)


class VisitThrottle(BaseThrottle):
    """
    允许访问阀值类
    """
    def __init__(self):
        self.history = None  # 访问记录

    def allow_request(self, request, view):
        """
        允许请求访问阀值
        :param request:
        :param view:
        :return:
        """
        remote_addr = request.META.get('REMOTE_ADDR')
        curtime = time.time()

        # 如果没有访问记录
        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr].append(curtime)

            return True

        self.history = request.META.get(remote_addr)

        # 当访问记录中有值，并且最早的访问记录在一分钟前
        while self.history and self.history[0] < curtime - 60:
            self.history.pop(0)

        # 当访问记录小于三次，则可以访问
        # 且将当前访问加入
        if len(self.history) < 3:
            self.history.appennd(curtime)

            return True

    def wait(self):
        """
        需等待多久才能访问
        :return:
        """





