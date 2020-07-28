from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
import json

# Create your views here.

# 对用户Token的验证
class TokenAuthentication:
    def



# APIView 继承的 View
class StudentViews(APIView):

    def get(self, request):
        # # 源码阅读从dispatch()开始，将原始request丰富了新的属性，在属性中进行了用户验证
        self.dispatch()

        res = {
            'code': 1000,
            'msg': ''
        }

        return HttpResponse(json.dumps(res), status=201)

    def post(self, request):

        return HttpResponse('创建Student')

    def put(self, request):

        return HttpResponse('修改Student')

    def delete(self, request):

        return HttpResponse('删除Student')