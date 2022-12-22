## 前言

程序内嵌了建表语句，这里的看看就行，我Python基础课的大作业，拿出来丢脸的



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

