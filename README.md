## 前言

forum.py为主程序，mysql_operate.py负责数据库操作，text_check.py负责检查输入的文本，程序开始会初始化，这里的建表语句看看就行，**数据库名是python_forum，这个可能需要自己手动建立一下**，我以后有其他解决方法可能会改善下（可能我以后都不管这个项目了哈哈，这个项目写了我两天，挺累的）。

这个系统很多思路都是基于我前一个java小论坛的项目，但同时也可以看到有需要优化的地方，有不足之处也欢迎大家指出（当然我也知道没人看我的项目的哈哈）！

我Python基础课的大作业，拿出来丢脸的。我知道自己写的挺烂的，但也算是个较为完善的小程序了，斗胆拿出来放在github上，算是记录自己的代码生涯吧！

写于2022年12月24日 晚 00:39:48



**v1.0版本**：

1. 基本完善用户发帖、删帖、修改信息等功能

2. 大致框架实现



**v2.0版本：**

1. 再原先版本的基础上优化了部分代码的复用度

2. 再系统中添加了管理员
3. 修复部分BUG
4. 添加系统初始化功能，彻底省去建表



## 用户表

- 用户id：user_id

- 用户名：user_name
- 账号：account
- 密码：pass_word
- 性别：gender
- 年龄：age

```mysql
create table if not exists user_table  (
    user_id int primary key not null auto_increment comment 'id',
    user_name varchar(20) not null  comment '用户名',
    account varchar(20) not null unique comment '账号',
    pass_word varchar(20) not null comment  '密码',
    gender char(1)  comment '性别',
    age tinyint comment '年龄'
)

insert into user_table values (1,'admin','admin','admin',null,null);
```



## 数据表

- 数据id：data_id
- 标题：title
- 发帖人用户名：post_user_name
- 发帖人id号：post__user_id
- 内容：content
- 发布时间：post_time

```mysql
create table if not exists data_table (
  data_id int primary key not null auto_increment comment 'id号',
  title varchar(30) not null comment '标题',
  post_user_name varchar(20) not null  comment  '发帖人用户名',
  post_user_id int not null comment  '发帖人id号',
  content varchar(300) not null comment '内容',
  post_time datetime not null  comment '发布时间',
  constraint data_user_fk foreign key (post_user_id) references user_table(user_id)
)
```



## 系统配置

- 管理员账号
- 管理员密码
- 验证码位数
- 管理员登录验证码开关情况
- 注册验证码开关情况
- 删帖验证码开关情况
- 验证码位数
- 管理员登录口令

```mysql
create table if not exists system_config(
    admin_account varchar(20) comment '管理员账号' default 'admin' ,
    admin_pass_word varchar(20) comment '管理员密码' default 'admin',
    admin_register_code_setting char(1)  comment '管理员登录验证码' default 'y',
    register_code_setting char(1) comment '注册验证码' default 'y',
    sign_in_code_setting char(1) comment '登录验证码' default 'y',
    delete_post_code_setting char(1) comment '删帖验证码' default 'y',
    check_code_number tinyint comment '验证码位数' default 4,
    admin_entry_word varchar(20) comment '管理员登录口令' default 'admin'
);

insert into system_config values();
```

