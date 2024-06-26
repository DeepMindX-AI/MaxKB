# coding=utf-8
"""
    @project: AIFun
    @Author：JackyFan
    @file： app_exception.py
    @date：2024/04/18
    @desc:
"""
from rest_framework import status


class AppApiException(Exception):
    """
    项目内异常
    """
    status_code = status.HTTP_200_OK

    def __init__(self, code, message):
        self.code = code
        self.message = message


class NotFound404(AppApiException):
    """
       未认证(未登录)异常
       """
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, code, message):
        self.code = code
        self.message = message


class AppAuthenticationFailed(AppApiException):
    """
    未认证(未登录)异常
    """
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, code, message):
        self.code = code
        self.message = message


class AppUnauthorizedFailed(AppApiException):
    """
    未授权(没有权限)异常
    """
    status_code = status.HTTP_403_FORBIDDEN

    def __init__(self, code, message):
        self.code = code
        self.message = message


class AppEmbedIdentityFailed(AppApiException):
    """
    嵌入cookie异常
    """
    status_code = 460

    def __init__(self, code, message):
        self.code = code
        self.message = message


class AppChatNumOutOfBoundsFailed(AppApiException):
    """
      访问次数超过今日访问量
    """
    status_code = 461

    def __init__(self, code, message):
        self.code = code
        self.message = message
