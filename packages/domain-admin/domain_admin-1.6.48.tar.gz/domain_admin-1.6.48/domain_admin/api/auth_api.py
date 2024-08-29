# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division
from flask import request

from domain_admin.service import auth_service
from domain_admin.utils.flask_ext.app_exception import AppException


def login():
    """
    用户登录
    :return:
    """
    username = request.json['username']
    password = request.json['password']

    token = auth_service.login(username, password)

    return {'token': token}


def register():
    """
    用户注册
    :return:
    """
    raise AppException('暂未开放')

    username = request.json['username']
    password = request.json['password']
    password_repeat = request.json['password_repeat']

    auth_service.register(username, password, password_repeat)


def send_code():
    """
    发送验证码
    :return:
    """
    username = request.json['username']

    # auth_service.register()
