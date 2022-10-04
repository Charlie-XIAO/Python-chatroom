# 数据库准备工作
# 先在终端中创建python_chat数据库
# mysql -u root -p 输入mysql root密码
# create database python_chat;
# 然后运行此程序在其中建表user_information
# 如果建表发生错误 或需要删除表中的内容 应当先删除数据库再重新进行准备
# drop database python_chat;

import pymysql

# 关联数据库
connection = pymysql.connect(host="localhost", user="root", password="Charlie8888", db="python_chat")
# 得到执行SQL语句的光标对象
cursor = connection.cursor()
# 要执行的SQL语句
sql = """

    create table user_information
     (
      user_name varchar (20),
      
      password varchar (20),
      
      data BLOB
    )

"""
# 执行SQL语句
cursor.execute(sql)
# 关闭光标对象
cursor.close()