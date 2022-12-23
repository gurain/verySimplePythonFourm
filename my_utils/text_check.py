#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/22 - 12:54
# @Author  : GuRain
# @File    : text_check.py
# @Description : 利用正则表达式对特定文本进行检验

__all__ = ["check_data_id", "check_title",
           "check_user_name", "check_account", "check_age", "check_gender", "check_content", "check_pass_word"]

import re

def check_user_name(text: str):
    """
    检验用户是否合法
    :param text: 用户名
    :return: 不合法返回False , 合法返回True
    """
    if re.search("^[\u4E00-\u9FA5A-Za-z0-9]{2,20}$", text):
        return True
    else:
        return False

def check_account(text: str):
    """
    检验账号是否合法
    :param text: 账号
    :return: 不合法返回False , 合法返回True
    """
    if re.search("^[a-zA-Z][a-zA-Z0-9_]{3,15}$", text):
        return True
    else:
        return False

def check_pass_word(text: str):
    """
    检验密码是否合法：
    :param text: 密码
    :return: 不合法返回False , 合法返回True
    """
    if re.search("^[a-zA-Z]\\w{3,15}$", text):
        return True
    else:
        return False

def check_admin_entry_word(text: str):
    """
    检验管理员登录口林是否合法：
    :param text: 密码
    :return: 不合法返回False , 合法返回True
    """
    if re.search("^\\w{1,20}$", text):
        return True
    else:
        return False

def check_age(text: str):
    """
    检验年龄是否合法：
    :param text: 年龄
    :return: 不合法返回False , 合法返回True
    """
    try:
        num = int(text)
        if 0 <= num <= 120:
            return True
        else:
            return False
    except ValueError:
        return False

def check_code_number(text: str):
    """
    检验验证码是否合法：
    :param text: 验证码
    :return: 不合法返回False , 合法返回True
    """
    try:
        num = int(text)
        if 0 < num <= 127:
            return True
        else:
            return False
    except ValueError:
        return False

def check_gender(text: str):
    """
    检验性别是否合法：
    :param text: 性别
    :return: 不合法返回False , 合法返回True
    """
    if text == "男" or text == "女":
        return True
    else:
        return False

def check_title(text: str):
    """
    检验标题是否合法
    :param text: 标题
    :return: 不合法返回False , 合法返回True
    """
    if re.search("^.{0,30}$", text):
        return True
    else:
        return False

def check_content(text: str):
    """
    检验帖子内容是否黑发
    :param text: 帖子内容
    :return: 不合法返回False , 合法返回True
    """
    if re.search("^.{0,300}$", text):
        return True
    else:
        return False

def check_data_id(text: str):
    """
    检验帖子id是否合法
    :param text:帖子id
    :return: 合法返回True,不合法返回False
    """
    if re.search("^\\d+$", text):
        return True
    else:
        return False
