#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/22 - 11:23
# @Author  : GuRain
# @File    : forum.py
# @Description : 论坛主程序

import random
import string
from PythonForum.my_utils import text_check, mysql_operate

# 当前账号
NOW_ACCOUNT: str = None


def register(flag: bool = True, text: str = "注册"):
    """
    用户注册
    :return: None
    """
    print(f"=========={text}==========")
    # 验证用户名
    while True:
        user_name = input("请输入用户名[中文、英文、数字但不包括下划线且长度大于1]:")
        if text_check.check_user_name(user_name):
            break
        else:
            print("用户名不合法!请重新输入!")
            continue
    # 验证账号
    while True:
        account = input("请输入账号[字母开头，允许4-16字节，允许字母数字下划线]:")
        if text_check.check_account(account):
            if not mysql_operate.check_user_is_exist(account):
                break
            else:
                print("账号已存在!请重新输入!")
        else:
            print("账号不合法!请重新输入!")
            continue
    # 验证密码
    while True:
        pass_word = input("请输入密码[以字母开头，长度在4~16之间，只能包含字母、数字和下划线]:")
        if text_check.check_pass_word(pass_word):
            break
        else:
            print("密码不合法!请重新输入!")
            continue
    if flag:
        # 进行验证
        checking_code(mysql_operate.get_system_config(True)["REGISTER_CODE_SETTING"])
    # 插入数据
    mysql_operate.insert_user_table(user_name, account, pass_word)
    print("注册成功!")


def sign_in():
    """
    登录账号,普通用户登录成功则返回True,管理员禁止登录,登录则返回False
    :return: 登录结果
    """
    print("==========登录==========")
    while True:
        # 输入账号
        while True:
            account = input("请输入账号:")
            if text_check.check_account(account):
                # 判断是否为管理员
                admin_account, admin_pass_word = mysql_operate.get_admin()
                if admin_account == account:
                    print("管理员账号禁止登录!")
                    return False
                if mysql_operate.check_user_is_exist(account):
                    break
                else:
                    print("账号不存在!")
            else:
                print("账号不合法!请重新输入!")
                continue
        # 输入密码
        while True:
            pass_word = input("请输入密码:")
            if text_check.check_pass_word(pass_word):
                break
            else:
                print("密码不合法!请重新输入!")
                continue
        # 进行验证
        checking_code(mysql_operate.get_system_config(True)["SIGN_IN_CODE_SETTING"])
        # 验证密码
        if pass_word == mysql_operate.get_pass_word_by_account(account):
            global NOW_ACCOUNT
            NOW_ACCOUNT = account
            print("登录成功!")
            return True
        else:
            print("密码错误!请重新登入!")


def show_information(flag: bool = True):
    """
    查看看人信息
    :param flag: 是否展示标题,默认展示
    :return: None
    """
    global NOW_ACCOUNT
    user_id, user_name, account, pass_word, gender, age = mysql_operate.get_information_by_account(NOW_ACCOUNT)
    if flag:
        print("==========个人信息==========")
        print(f"用户名:{user_name}")
        print(f"账号:{account}")
        print(f"性别:{gender}")
        print(f"年龄:{age}")
    else:
        print(f"用户名:{user_name}")
        print(f"账号:{account}")
        print(f"性别:{gender}")
        print(f"年龄:{age}\n")


def change_information():
    """
    修改个人信息
    :return:
    """
    global NOW_ACCOUNT
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
    mysql_operate.change_information_by_account(NOW_ACCOUNT, user_name, f"'{gender}'", age)
    print("修改成功!")


def change_pass_word():
    """
    修改密码
    :return:
    """
    global NOW_ACCOUNT
    print("==========修改密码==========")
    # 验证密码
    while True:
        pass_word = input("请输入原先密码:")
        if text_check.check_pass_word(pass_word):
            # 验证密码
            if pass_word == mysql_operate.get_pass_word_by_account(NOW_ACCOUNT):
                new_pass_word = input("请输入新密码[以字母开头，长度在6~18之间，只能包含字母、数字和下划线]:")
                mysql_operate.change_pass_word_by_account(NOW_ACCOUNT, new_pass_word)
                print("修改成功!")
                break
            else:
                print("密码错误!请重新输入!")
        else:
            print("密码不合法!请重新输入!")
            continue


def checking_code(flag):
    while True:
        if flag == 'n':
            break
        code_number = mysql_operate.get_system_config(True)["CHECK_CODE_NUMBER"]
        code = get_check_code(code_number)
        input_code = input(f"请输入验证码[{code}]：")
        if code == input_code:
            print("验证成功！")
            break
        else:
            print("验证码错误，请重新输入！")


def post(flag: bool = True):
    """
    发帖
    :return:
    """
    if flag:
        print("==========发帖==========")
        # 输入标题
        while True:
            title = input("请输入标题[0到30字]:")
            if text_check.check_title(title):
                break
            else:
                print("标题不合法!请重新输入!")
                continue
        # 输入内容
        while True:
            content = input("请输入内容[0到300字]:")
            if text_check.check_content(content):
                break
            else:
                print("标题不合法!请重新输入!")
                continue
        global NOW_ACCOUNT
        mysql_operate.posting(NOW_ACCOUNT, title, content)
        print("发帖成功!")
    else:
        print("==========新增帖子==========")
        # 输入标题
        while True:
            title = input("请输入标题[0到30字]:")
            if text_check.check_title(title):
                break
            else:
                print("标题不合法!请重新输入!")
                continue
        # 输入内容
        while True:
            content = input("请输入内容[0到300字]:")
            if text_check.check_content(content):
                break
            else:
                print("标题不合法!请重新输入!")
                continue
        mysql_operate.posting("admin", title, content)
        print("新增成功!")


def show_all_post(flag: bool = True):
    """
    查看全部帖子
    :return: None
    """
    result = mysql_operate.get_all_post()
    if flag:
        print("==========全部帖子==========")
    if len(result) > 0:
        for i in result:
            print(f"帖子id:{i[0]}\n帖子标题:{i[1]}\n用户名:{i[2]}\n帖子内容:{i[4]}\n发帖时间:{i[5]}\n")
    else:
        print("论坛内暂无帖子!")
        return False


def delete_my_post():
    """
    删除我的帖子
    :return:
    """
    global NOW_ACCOUNT
    print("==========删除帖子==========")
    # 展示当前账户下的帖子
    show_my_post(False)
    while True:
        if len(mysql_operate.get_all_post(NOW_ACCOUNT)) > 0:
            data_id = input("请输入你需要删除的帖子id:")
            # 检验输入的data_id是否合法
            if text_check.check_data_id(data_id):
                # 获取当前账户的全部帖子
                my_post_tuple = mysql_operate.get_all_post(NOW_ACCOUNT)
                # 检查删除的是否为当前账户的帖子
                for i in my_post_tuple:
                    if int(data_id) == i[0]:
                        # 删除id,是否成功
                        if mysql_operate.delete_data_by_data_id(data_id):
                            checking_code(mysql_operate.get_system_config(True)["DELETE_POST_CODE_SETTING"])
                            print(f"{data_id}号帖子删除成功!")
                            return
                print("帖子id不存在,请重新输入!")
                continue
            else:
                print("帖子id不合法!请重新输入!")
                continue
        else:
            break


def show_my_post(flag: bool = True):
    """
    展示我的帖子
    :param flag: 是否展示标题，传入False则不展示，默认展示
    :return:
    """
    global NOW_ACCOUNT
    result = mysql_operate.get_all_post(NOW_ACCOUNT)
    if flag:
        print("==========我的帖子==========")
    if len(result) > 0:
        for i in result:
            print(
                f"帖子id:{i[0]}\n帖子标题:{i[1]}\n用户名:{i[2]}\n帖子内容:{i[4]}\n发帖时间:{i[5]}\n")
    else:
        print("你还没有发过帖子呢,快去发布吧!")


def forum_center():
    """
    论坛中心
    :return: None
    """
    while True:
        print("==========论坛中心==========")
        print("1.查看个人信息\t5.查看我的帖子")
        print("2.修改个人信息\t6.查看全部帖子")
        print("3.修改我的密码\t7.删除我的帖子")
        print("4.发布新的帖子\t8.退回首页")
        command = input("请输入您的指令:")
        if command == "1":
            show_information()
        elif command == "2":
            change_information()
        elif command == "3":
            change_pass_word()
        elif command == "4":
            post(True)
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


def get_check_code(num: int = 4):
    """
    获取特定位数的验证码,并返回，默认是四位数
    :param num:验证码位数
    :return:验证码
    """
    # 词库
    word_stock = string.ascii_letters + string.digits
    code = ""
    for i in range(num):
        # 获取随机数
        rand_num = random.randint(0, len(word_stock))
        # 拼接获得的随机字符
        code += word_stock[rand_num - 1]
    return code


def set_system_config(title: str, command: int, operate_object: str):
    """
    提供两种模式，一种是设置位数，第二种是设置是否开启
    :param title: 显示的标题
    :param command: 1为设置位数模式，二为开关模式
    :param operate_object: 操作对象
    :return:
    """
    print(f"=========={title}=========")
    if command == 1:
        while True:
            num = mysql_operate.get_system_config(True)["CHECK_CODE_NUMBER"]
            new_num = input(f"当前验证码位数为：{num}\n请输入你需要修改的位数[大于0且小于等于127]：")
            if text_check.check_code_number(new_num):
                mysql_operate.set_system_config(operate_object, new_num)
                print(f"成功修改位数为：{new_num}")
                break
            else:
                print("验证码位数不合法，请重新输入！")
    elif command == 2:
        while True:
            command = input(
                f"当前状态为：{mysql_operate.get_system_config(True)[operate_object.upper()]}\n请输入是否开启验证码[y/n]：：")
            if command == 'y':
                mysql_operate.set_system_config(operate_object, command)
                print(f"开启成功！")
                break
            elif command == 'n':
                mysql_operate.set_system_config(operate_object, command)
                print(f"关闭成功！")
                break
            else:
                print("指令不合法，请重新输入！")


def check_code_setting():
    """
    验证码设置页面
    :return: None
    """
    while True:
        print("==========验证码设置==========")
        print("1.用户注册设置\t4.管理员登录设置")
        print("2.用户登录设置\t5.验证码位数设置")
        print("3.用户删帖设置\t6.返回控制台")
        command = input("请输入您的指令:")
        if command == "1":
            set_system_config("用户注册验证码开关", 2, "register_code_setting")
        elif command == "2":
            set_system_config("用户登录验证码开关", 2, "sign_in_code_setting")
        elif command == "3":
            set_system_config("用户删帖验证码开关", 2, "delete_post_code_setting")
        elif command == "4":
            set_system_config("管理员登录验证码开关", 2, "admin_register_code_setting")
        elif command == "5":
            set_system_config("验证码位数设置", 1, "check_code_number")
        elif command == "6":
            break
        else:
            print("指令不合法，请重新输入！")


def show_all_user(flag: bool = True):
    """
    查看全部用户
    :return:
    """
    if flag:
        print("==========全部用户==========")
    user_tuple = mysql_operate.get_all_user()
    if len(user_tuple) > 0:
        for i in user_tuple:
            print(f"用户id:{i[0]}\n用户名:{i[1]}\n账号:{i[2]}\n用户密码:{i[3]}\n用户性别:{i[4]}\n用户年龄:{i[5]}\n")
    else:
        print("论坛内暂无用户!")


def change_entry_word():
    """
    修改登入口令
    :return:
    """
    while True:
        admin_entry_word = mysql_operate.get_system_config(True)["ADMIN_ENTRY_WORD"]
        print(f"当前登入口令为:{admin_entry_word}")
        new_admin_entry_word = input("请输入新口令:")
        if text_check.check_admin_entry_word(new_admin_entry_word):
            mysql_operate.set_system_config("admin_entry_word", new_admin_entry_word)
            print("修改成功!")
            break
        else:
            print("登录口令不合法,请重新输入!")


def show_all_system_config():
    """
    查看全部的系统配置
    :return:
    """
    print("==========全部系统配置==========")
    system_config = mysql_operate.get_system_config(False)
    for i in system_config:
        print(f"管理账号:{i[0]}\t管理密码:{i[1]}\t管理登录口令:{i[7]}")
        print(
            f"管理员登录验证码:{i[2]}\t用户注册登录验证码:{i[3]}\t用户登录验证码:{i[4]}\t用户删帖验证码:{i[5]}\t验证码位数:{i[6]}")


def delete_user():
    """
    删除用户
    :return:
    """
    print("==========删除用户==========")
    show_all_user(False)
    while True:
        try:
            user_id = int(input("请输入你需要删除的用户id:"))
            if user_id == 1:
                print("管理员禁止删除!")
                break
            account = mysql_operate.get_account_by_user_id(user_id)
            if mysql_operate.check_user_is_exist(account):
                mysql_operate.delete_user_by_user_id(user_id)
                print("删除成功!")
                break
            else:
                print("用户不存在,请重新输入!")
        except ValueError:
            print("数据不合法,请重新输入!")


def delete_post():
    """
    删除帖子
    :return:
    """
    print("==========删除帖子==========")
    flag = show_all_post(False)
    if flag is False:
        return
    while True:
        try:
            data_id = int(input("请输入你需要删除的帖子id:"))
            if mysql_operate.check_data_is_exit(data_id):
                mysql_operate.delete_data_by_data_id(data_id)
                print("删除成功!")
                break
            else:
                print("帖子不存在,请重新输入!")
        except:
            print("数据不合法,请重新输入!")


def change_admin_account_and_pass_word():
    print("==========修改管理员账号密码==========")
    while True:
        admin_account = input("请输入新的管理员账号:")
        if text_check.check_account(admin_account):
            admin_pass_word = input("请输管理员密码:")
            if text_check.check_pass_word(admin_pass_word):
                mysql_operate.set_system_config("admin_account", admin_account)
                mysql_operate.set_system_config("admin_pass_word", admin_pass_word)
                print("账号密码修改成功!")
                break
            else:
                print("新密码不合法!请重新输入!")
        else:
            print("新账号不合法!请重新输入!")


def admin_control_center():
    """
    管理员控制中心
    :return:
    """
    while True:
        print("==========后台管理==========")
        print("1.增加用户\t5.查看全部用户\t9.修改管理员账号密码\t13.返回首页")
        print("2.删除用户\t6.查看全部帖子\t10.查看全部系统配置")
        print("3.增加帖子\t7.修改登录口令\t11.下载全部用户数据")
        print("4.删除帖子\t8.验证码设置\t12.下载全部帖子数据")
        command = input("请输入您的指令:")
        if command == "1":
            register(False, "新增用户")
        elif command == "2":
            delete_user()
        elif command == "3":
            post(False)
        elif command == "4":
            delete_post()
        elif command == "5":
            show_all_user()
        elif command == "6":
            show_all_post()
        elif command == "7":
            change_entry_word()
        elif command == "8":
            check_code_setting()
        elif command == "9":
            change_admin_account_and_pass_word()
        elif command == "10":
            show_all_system_config()
        elif command == "11":
            download_user_data()
        elif command == "12":
            download_post_data()
        elif command == "13":
            break
        else:
            print("指令错误,请重新输入!")


def admin_sign_in():
    """
   管理员登录
   :return:
   """
    # 获取管理员账号和密码
    admin_account = mysql_operate.get_system_config(True)["ADMIN_ACCOUNT"]
    admin_pass_word = mysql_operate.get_system_config(True)["ADMIN_PASS_WORD"]
    print("==========管理员登陆==========")
    # 输入管理员账号
    while True:
        account = input("请输入管理员账号:")
        if text_check.check_account(account):
            if account == admin_account:
                break
            else:
                print("账号不正确!")
        else:
            print("账号不合法!请重新输入!")
            continue
    # 输入管理员密码
    while True:
        pass_word = input("请输入管理员密码:")
        if text_check.check_pass_word(pass_word):
            if pass_word == admin_pass_word:
                break
            else:
                print("密码不正确!")
        else:
            print("账号不合法!请重新输入!")
            continue
    checking_code(mysql_operate.get_system_config(True)["ADMIN_REGISTER_CODE_SETTING"])
    print(f"{admin_account}管理员，登录成功!")


def main():
    """
    首页
    :return: None
    """
    while True:
        admin_entry_word = mysql_operate.get_system_config(True)["ADMIN_ENTRY_WORD"]
        print("==========首页==========")
        print("1.登入")
        print("2.注册")
        print("3.退出")
        command = input("请输入您的指令:")
        if command == "1":
            flag = sign_in()
            if flag:
                forum_center()
        elif command == "2":
            register()
        elif command == "3":
            exit()
        elif command == admin_entry_word:
            admin_sign_in()
            admin_control_center()
        else:
            print("指令错误,请重新输入!")


def download_post_data():
    """
    下载帖子数据
    :return:
    """
    print("==========下载帖子数据==========")
    file_name = input("请输入你需要保存的文件名(存在同名文件将会覆盖):")
    while True:
        if text_check.check_file_name(file_name):
            with open(file_name + ".txt", mode='w', encoding="UTF-8") as f:
                f.write("帖子id,标题,发布者,发布者id,内容,发布时间\n")
                post_tuple = mysql_operate.get_all_post()
                for i in post_tuple:
                    f.write(f"{i[0]},{i[1]},{i[2]},{i[3]},{i[4]},{i[5]}\n")
                print("下载成功!")
                break
        else:
            print("文件名不合法,请重新输入!")


def download_user_data():
    print("==========下载用户数据==========")
    file_name = input("请输入你需要保存的文件名(存在同名文件将会覆盖):")
    while True:
        if text_check.check_file_name(file_name):
            with open(file_name + ".txt", mode='w', encoding="UTF-8") as f:
                f.write("用户id,用户名,账号,用户密码,性别,年龄\n")
                post_tuple = mysql_operate.get_all_user()
                for i in post_tuple:
                    f.write(f"{i[0]},{i[1]},{i[2]},{i[3]},{i[4]},{i[5]}\n")
                print("下载成功!")
                break
        else:
            print("文件名不合法,请重新输入!")


if __name__ == '__main__':
    # 初始化系统
    mysql_operate.initialize_system()
    # 运行主程序
    main()
