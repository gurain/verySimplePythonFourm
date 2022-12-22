#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/22 - 11:23
# @Author  : GuRain
# @File    : forum.py
# @Description : 论坛主程序

from PythonForum.my_utils import text_check, mysql_operate

# 当前账号
NOW_ACCOUNT= None


def register():
    """
    用户注册
    :return: None
    """
    print("==========注册==========")
    # 验证用户名
    while True:
        user_name = input("请输入用户名[中文、英文、数字但不包括下划线且长度大于1]:")
        if  text_check.check_user_name(user_name):
            break
        else:
            print("用户名不合法!请重新输入!")
            continue
    # 验证账号
    while True:
        account = input("请输入账号[字母开头，允许4-16字节，允许字母数字下划线]:")
        if  text_check.check_account(account):
            if  not mysql_operate.check_user_is_exist(account):
                break
            else:
                print("账号已存在!请重新输入!")
        else:
            print("账号不合法!请重新输入!")
            continue
    # 验证密码
    while True:
        pass_word = input("请输入密码[以字母开头，长度在4~16之间，只能包含字母、数字和下划线]:")
        if  text_check.check_pass_word(pass_word):
            break
        else:
            print("密码不合法!请重新输入!")
            continue
    # 插入数据
    mysql_operate.inser_user_table(user_name,account,pass_word)

def sign_in():
    """
    登录
    :return: None
    """
    print("==========登录==========")
    while True:
        # 输入账号
        while True:
            account = input("请输入账号:")
            if text_check.check_account(account):
                if mysql_operate.check_user_is_exist(account):
                    break
                else:
                    print("账号不存在!")
            else:
                print("账号不合法!请重新输入!")
                continue
        # 输入密码
        while True:
            pass_word = input("请输入密码")
            if text_check.check_pass_word(pass_word):
                break
            else:
                print("密码不合法!请重新输入!")
                continue
        # 验证密码
        if pass_word == mysql_operate.get_pass_word_by_account(account):
            global NOW_ACCOUNT
            NOW_ACCOUNT=account
            print("登录成功!")
            break
        else:
            print("密码错误!请重新登入!")

def show_information(flag:bool = True):
    """
    查看看人信息
    :param flag: 是否展示标题,默认展示
    :return: None
    """
    user_id,user_name,account,pass_word,gender,age =  mysql_operate.get_information_by_account(NOW_ACCOUNT)
    if flag == True:
        print("==========个人信息==========")
        print(f"用户名:{user_name}")
        print(f"账号:{account}")
        print(f"性别:{gender}")
        print(f"年龄:{age}")
    else:
        print(f"id:{id}")
        print(f"用户名:{user_name}")
        print(f"账号:{account}")
        print(f"性别:{gender}")
        print(f"年龄:{age}")

def change_information():
    """
    修改个人信息
    :return:
    """
    print("==========修改信息==========")
    # 展示个人信息
    show_information(False)
    # 用户名
    while True:
        user_name = input("请输入用户名[中文、英文、数字但不包括下划线且长度大于1]:")
        if text_check.check_user_name(user_name):
            break
        else:
            print("用户名不合法!请重新输入!")
            continue
    # 性别
    while True:
        gender = input("请输入性别(男/女):")
        if text_check.check_gender(gender):
            break
        else:
            print("性别不合法!请重新输入!")
            continue
    # 年龄
    while True:
        age = input("请输入年龄(年龄需要大于0且小于120):")
        if text_check.check_age(age):
            break
        else:
            print("年龄不合法!请重新输入!")
            continue
    # 修改用户名、性别、年龄
    mysql_operate.change_information_by_account(NOW_ACCOUNT,user_name,gender,age)
    print("修改成功!")

def change_pass_word():
    """
    修改密码
    :return:
    """
    print("==========修改密码==========")
    # 验证密码
    while True:
        pass_word = input("请输入原先密码:")
        if  text_check.check_pass_word(pass_word):
            # 验证密码
            if pass_word == mysql_operate.get_pass_word_by_account(NOW_ACCOUNT):
                new_pass_word = input("请输入新密码[以字母开头，长度在6~18之间，只能包含字母、数字和下划线]:")
                mysql_operate.change_pass_word_by_account(NOW_ACCOUNT,new_pass_word)
                print("修改成功!")
                break
            else:
                print("密码错误!请重新输入!")
        else:
            print("密码不合法!请重新输入!")
            continue

def post():
    """
    发帖
    :return:
    """
    print("==========发帖==========")
    # 输入标题
    while True:
        title = input("请输入标题[0到30字]:")
        if text_check.check_title(title):
            break
        else:
            print("标题不合法!请重新输入!")
            continue
    while True:
        content = input("请输入内容[0到300字]:")
        if text_check.check_content(content):
            break
        else:
            print("标题不合法!请重新输入!")
            continue
    mysql_operate.posting(NOW_ACCOUNT,title,content)
    print("发帖成功!")

def show_all_post():
    """
    查看全部帖子
    :return: None
    """
    print("==========全部帖子==========")
    mysql_operate.show_post()

def delete_my_post():
    """
    删除我的帖子
    :return:
    """
    while True:
        print("==========删除帖子==========")
        # 展示当前账户下的帖子
        if  mysql_operate.show_post(NOW_ACCOUNT):
            data_id =  input("请输入你需要删除的帖子id:")
            # 检验输入的data_id是否合法
            if text_check.check_data_id(data_id):
                # 删除id,是否成功
                if mysql_operate.delete_data_by_data_id(data_id):
                    print(f"{data_id}号帖子删除成功")
                    break
                else:
                    print(f"{data_id}号帖子不存在,请重新输入")
                    continue
            else:
                print("帖子id不合法!请重新输入!")
                continue
        else:
            print("你还没有发过帖子呢,快去发布吧!")
            break

def show_my_post():
    """
    展示我的帖子
    :return:
    """
    print("==========我的帖子==========")
    if not mysql_operate.show_post(NOW_ACCOUNT):
       print("你还没有发过帖子呢,快去发布吧!")

def forum_center():
    """
    论坛中心
    :return: None
    """
    while True:
        print("==========论坛中心==========")
        print("1.查看个人信息")
        print("2.修改个人信息")
        print("3.修改我的密码")
        print("4.发布新的帖子")
        print("5.查看我的帖子")
        print("6.查看全部帖子")
        print("7.删除我的帖子")
        print("8.退回首页")
        command = input("请输入您的指令:")
        if command == "1":
            show_information()
        elif command == "2":
            change_information()
        elif command == "3":
           change_pass_word()
        elif command == "4":
            post()
        elif command == "5":
            show_my_post()
        elif command == "6":
            show_all_post()
        elif command == "7":
            delete_my_post()
        elif command == "8":
            return
        else:
            print("指令错误,请重新输入!")

def main():
    """
    首页
    :return: None
    """
    while True:
        print("==========首页==========")
        print("1.登入")
        print("2.注册")
        print("3.退出")
        command = input("请输入您的指令:")
        if command == "1":
            sign_in()
            forum_center()
            pass
        elif command == "2":
            register()
        elif command == "3":
            exit()
        else:
            print("指令错误,请重新输入!")


if __name__ == '__main__':
    main()
