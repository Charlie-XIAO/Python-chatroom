import pymysql
import sys

class LogInformation:

    # 检查用户登录
    def login_check(user_name, password):
        # 关联数据库
        db = pymysql.connect(host="localhost", user="root", password="Charlie8888", db="python_chat")
        # 得到执行SQL语句的光标对象
        cursor = db.cursor()
        # 要执行的SQL语句
        # 按ID查找
        sql = "SELECT * FROM user_information where user_name = '%s' " % (user_name)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 接受所有符合的对象
            results = cursor.fetchone()
            # 断开数据库连接
            db.close()
            # 密码正确返回True
            return password == results[1]
        except:
            return False
    
    # 创建新用户
    def create_new_user(user_name, password, file_name):
        # 关联数据库
        db = pymysql.connect(host="localhost", user="root", password="Charlie8888", db="python_chat")
        # 得到执行SQL语句的光标对象
        cursor = db.cursor()
        # 读取头像
        fp = open(file_name, "rb")
        img = fp.read()
        # 要执行的SQL语句
        # 插入用户数据
        sql = "INSERT INTO user_information VALUES  (%s,%s,%s);"
        args = (user_name, password, img)
        try:
            # 执行SQL语句
            cursor.execute(sql, args)
            # 提交
            db.commit()
            # 断开数据库连接
            db.close()
            print("Insertion successful")
            return "0"
        except Exception as err:
            print("Database error: ", err)
            # 发生错误时回滚
            db.rollback()
            # 断开数据库连接
            db.close()
    
    # 检查用户名是否已经存在
    def select_user_name(user_name):
        # 关联数据库
        db = pymysql.connect(host="localhost", user="root", password="Charlie8888", db="python_chat")
        # 得到执行SQL语句的光标对象
        cursor = db.cursor()
        # 要执行的SQL语句
        # 插入用户数据
        sql = "SELECT * FROM user_information where user_name = '%s' " % (user_name)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 接受所有符合的对象
            results = cursor.fetchone()
            # 1代表已有用户 0代表可以注册
            if results is not None:
                # 关闭数据库
                db.close()
                return "1"
            else:
                db.close()
                return "0"
        except Exception as err:
            print("Database error: ", err)
            # 断开数据库连接
            db.close()
    
    # 查找头像 用于聊天界面显示头像
    def fing_face(user_name):
        try:
            # 关联数据库
            connection = pymysql.connect(host="localhost", user="root", password="Charlie8888", db="python_chat")
            # 得到执行SQL语句的光标对象
            cursor = connection.cursor()
            # 要执行的SQL语句
            # 按用户名查找
            sql = "SELECT * FROM user_information where user_name = '%s' " % (user_name)
            # 执行SQL语句
            cursor.execute(sql)
            # 写入头像数据
            fout = open("profiles/user_profile.png", "wb")
            fout.write(cursor.fetchone()[2])
            fout.close()
            # 关闭光标对象
            cursor.close()
            # 断开数据库连接
            connection.close()
        except pymysql.Error as err:
            print("Error %d: %s" % (err.args[0], err.args[1]))
            sys.exit(1)