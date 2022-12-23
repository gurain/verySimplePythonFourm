#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/22 - 11:31
# @Author  : GuRain
# @File    : mysql_operate.py
# @Description : 对mysql数据库进行相关操作
import pymysql
from pymysql import Connection

__all__ = ["posting", "get_all_post", "change_information_by_account", "get_user_id_by_account",
           "change_pass_word_by_account", "insert_user_table",
           "delete_data_by_data_id", "check_data_is_exit", "check_user_is_exist", "get_pass_word_by_account"]

HOST = 'localhost'
PORT = 3306
USER = 'root'
PASS_WORD = 'admin'
DATA_BASE = "python_forum"
USER_TABLE = "user_table"
DATA_TABLE = "data_table"
CREATE_USER_TABLE_SENTENCE = """
create table if not exists user_table  (
    user_id int primary key not null auto_increment comment 'id',
    user_name varchar(20) not null  comment '用户名',
    account varchar(20) not null unique comment '账号',
    pass_word varchar(20) not null comment  '密码',
    gender char(1)  comment '性别',
    age tinyint comment '年龄'
)
"""
CREATE_DATA_TABLE_SENTENCE = """
create table if not exists data_table (
  data_id int primary key not null auto_increment comment 'id号',
  title varchar(30) not null comment '标题',
  post_user_name varchar(20) not null  comment  '发帖人用户名',
  post_user_id int not null comment  '发帖人id号',
  content varchar(300) not null comment '内容',
  post_time datetime not null  comment '发布时间',
  constraint data_user_fk foreign key (post_user_id) references user_table(user_id)
)
"""
CREATE_SYSTEM_CONFIG_TABLE_SENTENCE = """
create table if not exists system_config(
    admin_account varchar(20) comment '管理员账号' default 'admin' ,
    admin_pass_word varchar(20) comment '管理员密码' default 'admin',
    admin_register_code_setting char(1)  comment '管理员登录验证码' default 'y',
    register_code_setting char(1) comment '注册验证码' default 'y',
    sign_in_code_setting char(1) comment '登录验证码' default 'y',
    delete_post_code_setting char(1) comment '删帖验证码' default 'y',
    check_code_number tinyint comment '验证码位数' default 4,
    admin_entry_word varchar(20) comment '管理员登录口令' default 'admin'
)
"""

# 连接数据库
conn = Connection(
    host=HOST,
    port=PORT,
    user=USER,
    password=PASS_WORD,
    autocommit=True,
    charset='utf8'
)
# 获取游标
cursor = conn.cursor()
# 选择数据库
conn.select_db(DATA_BASE)


def initialize_system():
    """
    初始化系统,成功返回True,失败返回False
    :return:
    """
    global cursor
    # 执行建立用户表语句
    cursor.execute(CREATE_USER_TABLE_SENTENCE)
    # 执行建立数据表语句
    cursor.execute(CREATE_DATA_TABLE_SENTENCE)
    # 执行建立系统表和插入相关信息语句
    cursor.execute(CREATE_SYSTEM_CONFIG_TABLE_SENTENCE)
    try:
        # 初始化用户表
        cursor.execute("insert into user_table values (1,'admin','admin','admin',null,null)")
        # 初始化系统配置表
        row = cursor.execute("select * from system_config")
        if row == 0:
            cursor.execute("insert into system_config values ()")
        # 操作成功
        return True
    except pymysql.err.IntegrityError:
        pass


def get_admin():
    """
    获取管理员信息
    :return: 管理员账号和密码
    """
    cursor.execute("select admin_account,admin_pass_word from system_config")
    result = cursor.fetchall()
    return result[0][0], result[0][1]


def get_system_config(flag: bool == True):
    """
    默认获取全部系统配置并封装到一个字典上返回,传入False将返回元组
    :param flag:
    :return:
    """
    cursor.execute("select * from system_config")
    result = cursor.fetchall()
    if flag:
        config_dict = {}
        # 管理员账号
        config_dict["ADMIN_ACCOUNT"] = result[0][0]
        # 管理员密码
        config_dict["ADMIN_PASS_WORD"] = result[0][1]
        # 管理员登录验证码设置
        config_dict["ADMIN_REGISTER_CODE_SETTING"] = result[0][2]
        # 登录验证码设置
        config_dict["REGISTER_CODE_SETTING"] = result[0][3]
        # 注册验证码设置
        config_dict["SIGN_IN_CODE_SETTING"] = result[0][4]
        # 删除验证码设置
        config_dict["DELETE_POST_CODE_SETTING"] = result[0][5]
        # 验证码位数
        config_dict["CHECK_CODE_NUMBER"] = result[0][6]
        # 管理员登录密码
        config_dict["ADMIN_ENTRY_WORD"] = result[0][7]
        # 返回系统配置字典
        return config_dict
    else:
        return result


def posting(account, title, content):
    """
    发帖
    :param account: 账号
    :param title:  标题
    :param content:  内容
    :return:  None
    """
    user_id, user_name, account, pass_word, gender, age = get_information_by_account(account)
    cursor.execute(f"insert into {DATA_TABLE} values (null,'{title}','{user_name}',{user_id},'{content}',now())")


def get_all_user():
    """
    获取全部用户，并返回元组
    :return:
    """
    cursor.execute(f"select * from {USER_TABLE}")
    result = cursor.fetchall()
    return result


def get_all_post(account=None) -> tuple:
    """
    获取全部帖子,返回包帖子数据的元组,默认返回全部帖子数据,也可传入特定账号获取用户的帖子
    :return: 包含帖子数据的元组
    """
    if account is None:
        cursor.execute(f"select * from {DATA_TABLE}")
        result = cursor.fetchall()
        return result
    else:
        # 通过account获取user_id
        user_id = get_user_id_by_account(account)
        # 通过user_id获取全部帖子数据并返回
        cursor.execute(f"select * from {DATA_TABLE} where post_user_id = {user_id}")
        result = cursor.fetchall()
        return result


def delete_data_by_data_id(data_id):
    """
    通过帖子id删除帖子
    :param data_id: 帖子id
    :return:成功返回True,失败返回False
    """
    if check_data_is_exit(data_id):
        cursor.execute(f"delete  from {DATA_TABLE} where data_id ={data_id}")
        return True
    else:
        return False


def delete_user_by_user_id(user_id):
    """
    通过用户id删除用户
    :param user_id: 用户id
    :return:成功返回True,失败返回False
    """
    account = get_account_by_user_id(user_id)
    if check_user_is_exist(account):
        cursor.execute(f"delete  from {USER_TABLE} where user_id ={user_id}")
        return True
    else:
        return False


def check_data_is_exit(data_id):
    """
    查询帖子是否存在
    :param data_id: 帖子id
    :return: 帖子存在返回True,帖子不存在返回False
    """
    num = cursor.execute(f"select data_id from {DATA_TABLE} where data_id = '{data_id}'")
    if num == 0:
        # 结果为0,说明帖子不存在
        return False
    else:
        # 查出其他结果,说明帖子
        return True


def change_information_by_account(account, user_name, gender, age):
    """
    通过账号修改相关信息
    :param account: 账号
    :param user_name: 用户名
    :param gender: 性别
    :param age: 年龄
    :return: None
    """
    cursor.execute(
        f"update {USER_TABLE} set user_name='{user_name}',gender='{gender}',age={age} where account = '{account}'")


def change_pass_word_by_account(account, pass_word):
    """
    修改密码
    :param account: 账号
    :param pass_word: 密码
    :return: None
    """
    cursor.execute(f"update {USER_TABLE} set pass_word='{pass_word}' where account = '{account}'")


def get_information_by_account(account):
    """
    传入账号,返回全部信息
    :param account: 账号
    :return: 全部信息
    """
    cursor.execute(f"select * from {USER_TABLE} where account = '{account}'")
    result = cursor.fetchall()
    for i in result:
        return i[0], i[1], i[2], i[3], i[4], i[5]


def get_user_id_by_account(account):
    """
    通过账号查找用户id
    :param account: 账号
    :return: 查找成功返回用户id,查找不成功,返回-1
    """
    cursor.execute(f"select user_id from {USER_TABLE} where account = '{account}'")
    result = cursor.fetchall()
    if len(result) == 1:
        return result[0][0]
    else:
        return -1


def get_account_by_user_id(user_id):
    """
    通过用户id查找账号
    :param user_id: 用户id
    :return: 查找成功返回账号,查找不成功,返回-1
    """
    cursor.execute(f"select account from {USER_TABLE} where user_id = '{user_id}'")
    result = cursor.fetchall()
    if len(result) == 1:
        return result[0][0]
    else:
        return -1


def insert_user_table(user_name, account, pass_word, gender='男', age='null'):
    """
    插入用户信息
    :param user_name:用户名
    :param account: 账号
    :param pass_word: 密码
    :param gender: 性别
    :param age: 年龄
    :return: None
    """
    cursor.execute(f"insert into {USER_TABLE} values (null,'{user_name}','{account}','{pass_word}','{gender}',{age})")


def check_user_is_exist(account):
    """
    传入用户名,并查询用户是否存在
    :param account:  账号
    :return: 存在返回True,不存在返回False
    """
    # 查询用户,并返回影响的行数
    num = cursor.execute(f"select account from {USER_TABLE} where account = '{account}'")
    if num == 0:
        # 结果为0,说明用户不存在
        return False
    else:
        # 查出其他结果,说明存在用户
        return True


def get_pass_word_by_account(account: str):
    """
    输入账号,查询数据库,返回密码
    :param account: 账号
    :return: 密码
    :rtype:str
    """
    cursor.execute(f"select pass_word from {USER_TABLE} where account = '{account}'")
    result: tuple = cursor.fetchall()
    return result[0][0]


def set_system_config(operate_object: str, values: str):
    """
    修改系统配置"
    :param operate_object: 需要修改的配置
    :param values: 需要修改的指
    :return: 
    """""
    if operate_object == "admin_account":
        cursor.execute(f"update {USER_TABLE} set account = '{values}' where  user_id = 1;")
        cursor.execute(f"update system_config set {operate_object} = '{values}'")
    elif operate_object == "admin_pass_word":
        cursor.execute(f"update {USER_TABLE} set pass_word = '{values}' where  user_id = 1;")
        cursor.execute(f"update system_config set {operate_object} = '{values}'")
    else:
        cursor.execute(f"update system_config set {operate_object} = '{values}'")


if __name__ == '__main__':
    # insert_user_table("测试","a12","123")
    # print(check_user_is_exist("test"))
    # get_pass_word_by_account("test")
    # print(get_information_by_account("test"))
    # print(get_all_post("asdsadas"))
    # print(get_admin())
    # set_check_code_number(2)
    # print(get_system_config(True))
    cursor.close()
    conn.close()
