from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse

# Create your views here.


# APIView 继承的 View
class StudentViews(APIView):

    def get(self, request):

        res = {
            'code': 1000,
            'msg': ''
        }

        return HttpResponse()