#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/22 - 11:31
# @Author  : GuRain
# @File    : mysql_operate.py
# @Description : 通过

from pymysql import Connection

__all__ = ["posting","show_post","change_information_by_account","get_user_id_by_account"
    ,"change_pass_word_by_account","inser_user_table"
    ,"delete_data_by_data_id","check_data_is_exit","check_user_is_exist","get_pass_word_by_account"]


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
CREATE_DATA_TABLE_SENTENCE ="""
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
# 执行建立用户表语句
cursor.execute(CREATE_USER_TABLE_SENTENCE)
# 执行建立数据表语句
cursor.execute(CREATE_DATA_TABLE_SENTENCE)

def posting(account,title,content):
    """
    发帖
    :param account: 账号
    :param title:  标题
    :param content:  内容
    :return:  None
    """
    user_id, user_name, account, pass_word, gender, age = get_information_by_account(account)
    cursor.execute(f"insert into {DATA_TABLE} values (null,'{title}','{user_name}',{user_id},'{content}',now());")

def show_post(account = None):
    if account==None:
        cursor.execute("select * from data_table")
        result = cursor.fetchall()
        if len(result) > 0:
            for post in result:
                print(f"帖子id:{post[0]}\n帖子标题:{post[1]}\n用户名:{post[2]}\n帖子内容:{post[4]}\n发帖时间:{post[5]}")
                print()
            return  True
        else:
            print("论坛内暂无帖子,快去发布吧!")
            return False
    else:
        user_id = get_user_id_by_account(account)
        cursor.execute(f"select * from data_table where post_user_id = {user_id}")
        result = cursor.fetchall()
        if len(result) > 0:
            for post in result:
                print(f"帖子id:{post[0]}\n帖子标题:{post[1]}\n用户名:{post[2]}\n帖子内容:{post[4]}\n发帖时间:{post[5]}")
                print()
            return True
        else:
            # 帖子不存在
            return False

def delete_data_by_data_id(data_id):
    """
    通过帖子id删除帖子
    :param data_id: 帖子id
    :return:成功返回True,失败返回False
    """
    if check_data_is_exit(data_id) :
        cursor.execute(f"delete  from data_table where data_id ={data_id}")
        return  True
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
        #查出其他结果,说明帖子
        return  True

def change_information_by_account(account,user_name,gender,age):
    """
    通过账号修改相关信息
    :param account: 账号
    :param user_name: 用户名
    :param gender: 性别
    :param age: 年龄
    :return: None
    """
    cursor.execute(f"update {USER_TABLE} set user_name='{user_name}',gender='{gender}',age={age} where account = '{account}'")

def change_pass_word_by_account(account,pass_word):
    """
    修改密码
    :param account: 账号
    :param pass_word: 密码
    :return: None
    """
    cursor.execute(f"update {USER_TABLE} set pass_word='{pass_word}' where account = '{account}'")

def get_information_by_account(account = "test"):
    """
    传入账号,返回全部信息
    :param account: 账号
    :return: 全部信息
    """
    cursor.execute(f"select * from {USER_TABLE} where account = '{account}'")
    result = cursor.fetchall()
    for i in result:
        return i[0],i[1],i[2],i[3],i[4],i[5]

def get_user_id_by_account(account):
    """
    通过账号查找用户id
    :param account: 账号
    :return: 查找成功返回用户id,查找不成功,返回-1
    """
    cursor.execute(f"select user_id from {USER_TABLE} where account = '{account}'")
    result =  cursor.fetchall()
    if len(result) == 1:
       return result[0][0]
    else:
       return  -1

def inser_user_table(user_name,account,pass_word,gender = '男'  ,age = 'null'):
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
        #查出其他结果,说明存在用户
        return  True

def get_pass_word_by_account(account:str):
    """
    输入账号,查询数据库,返回密码
    :param account: 账号
    :return: 密码
    :rtype:str
    """
    cursor.execute(f"select pass_word from {USER_TABLE} where account = '{account}'")
    result:tuple =  cursor.fetchall()
    return result[0][0]

if __name__ == '__main__':
    # inser_user_table("测试","a12","123")
    # print(check_user_is_exist("test"))
    # get_pass_word_by_account("test")
    # print(get_information_by_account("test"))
    # show_post("test")
    cursor.close()
    conn.close()
