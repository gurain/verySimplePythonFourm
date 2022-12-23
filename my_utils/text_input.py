#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/23 - 9:41
# @Author  : GuRain
# @File    : text_input.py
# @Description :

from PythonForum.my_utils import mysql_operate, text_check


def intput_user_name():
    """
    获取用户名
    :return: 用户名
    """
    # 输入用户名
    while True:
        user_name = input("请输入用户名[中文、英文、数字但不包括下划线且长度大于1]:")
        if text_check.check_user_name(user_name):
            return user_name
        else:
            print("用户名不合法!请重新输入!")
            continue


def input_account():
    """
    获取账号
    :return:账号
    """
    # 输入账号
    while True:
        account = input("请输入账号[字母开头，允许4-16字节，允许字母数字下划线]:")
        if text_check.check_account(account):
            if not mysql_operate.check_user_is_exist(account):
                return account
            else:
                print("账号已存在!请重新输入!")
        else:
            print("账号不合法!请重新输入!")
            continue


def input_pass_word():
    """
    获取密码
    :return:
    """
    # 输入密码
    while True:
        pass_word = input("请输入密码[以字母开头，长度在4~16之间，只能包含字母、数字和下划线]:")
        if text_check.check_pass_word(pass_word):
            return pass_word
        else:
            print("密码不合法!请重新输入!")
            continue
