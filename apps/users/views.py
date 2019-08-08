from django.shortcuts import render

# Create your views here.

from django import db
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import View


class RegisterView(View):
    """
    执行注册逻辑
    """
    def get(self, request):
        pass

    def post(self, request):
        pass


class ActiveView(View):
    """
    激活用户
    """
    def get(self, request, token):
        pass


class LoginView(View):
    """
    返回登录界面
    """
    def get(self, request):
        pass

    def post(self, request):
        pass

class LogoutView(View):
    """
    登出功能
    """

    def get(self, request):
        pass

