import socket
from threading import Thread
import math

import chat_mysql

# 维护一个在线用户的连接列表 用于群发消息
online_connection = list()
# 存储socket连接和用户的对应关系
connection_user = dict()
# 存储加入系统聊天室的用户
join_user = ""
# 发送用户加入聊天室系统提示标记
flag = 0
# 存储聊天对象标记
chat_user = ""

# 发送带长度的字符串函数
def send_string_with_length(_conn, content):
    # 发送内容的长度
    _conn.sendall(bytes(content, encoding = "utf-8").__len__().to_bytes(4, byteorder="big"))
    # 发送内容
    _conn.sendall(bytes(content, encoding = "utf-8"))

# 发送在线用户数的函数
def send_number(_conn, number):
    _conn.sendall(int(number).to_bytes(4, byteorder="big"))

# 获取变长字符串的函数
def recv_all_string(connection):
    # 获取消息长度
    length = int.from_bytes(connection.recv(4), byteorder="big")
    # utf-8编码中汉字占3字节 英文占1字节
    b_size = 3 * 1024
    times = math.ceil(length / b_size)
    content = ""
    for i in range(times):
        if i == times - 1:
            seg_b = connection.recv(length % b_size)
        else:
            seg_b = connection.recv(b_size)
        content += str(seg_b, encoding="utf-8")
    return content

# 检查用户名密码是否正确的函数
def check_user(user_name, password):
    # 调用数据库模块检查用户名和密码
    return chat_mysql.LogInformation.login_check(user_name, password)

# 添加用户函数
def add_user(user_name, password, file_name):
    # 调用数据库模块中的函数添加用户
    # 添加用户成功返回0 已有用户返回1 其他错误返回2
    if chat_mysql.LogInformation.select_user_name(user_name) == "1":
        return "1"
    elif chat_mysql.LogInformation.create_new_user(user_name, password, file_name) == "0":
        return "0"
    else:
        return "2"

# 处理刷新列表请求的函数
def handle_online_list():
    # 给所有在线用户发送消息
    for con in online_connection:
        # 发送刷新用户列表标记
        send_string_with_length(con, "#!onlinelist#!")
        # 发送列表人数
        send_number(con, online_connection.__len__())
        # 发送用户名
        for c in online_connection:
            send_string_with_length(con, connection_user[c])
    return True

# 处理登录请求函数
def handle_login(connection, address):

    # 声明存储加入聊天室的用户
    global join_user
    # 声明用户加入聊天室的标记
    global flag

    # 调用函数接收客户端发送的用户名和密码
    user_name = recv_all_string(connection)
    password = recv_all_string(connection)
    # 调用函数检查用户名和密码
    check_result = check_user(user_name, password)
    # 如果检查结果为True 向客户端发送登陆成功标记
    if check_result == True:
        # 向客户端发送登陆通过标记
        connection.sendall(bytes("1", "utf-8"))
        # 把用户和连接号加入字典
        # key - 连接号  value - 用户名
        connection_user[connection] = user_name
        # 存储加入系统聊天室的用户
        join_user = user_name
        # 设置标记为真 用于向所有客户端发送用户加入聊天的信息
        flag = 1
        # 把当前连接的用户添加到在线用户的链接列表 用于群发消息
        online_connection.append(connection)
        # 调用刷新在线用户列表的函数
        handle_online_list()
        # 调用发送用户加入聊天室信息的函数
        handle_message(connection, address)
    else:
        # 向客户端发送登陆失败标记
        connection.sendall(bytes("0", "utf-8"))
    return True

# 处理注册请求函数
def handle_register(connection, address):
    # 调用函数接收客户端发送的用户名和密码
    user_name = recv_all_string(connection)
    password = recv_all_string(connection)
    file_name = recv_all_string(connection)
    # 调用添加用户函数add_user返回值作为发送给客户端的标记
    # 添加用户成功返回0 已有用户返回1 其他错误返回2
    connection.sendall(bytes(add_user(user_name, password, file_name), "utf-8"))
    return True

# 处理消息发送请求函数
def handle_message(connection, address):
    
    # 声明存储加入聊天室的用户
    global join_user
    # 声明用户加入聊天室的标记
    global flag

    # 如果等于1 发送加入聊天信息给所有客户端
    if flag == 1:
        for c in online_connection:
            # 发送消息标记
            send_string_with_length(c, "#!message#!")
            # 发送聊天对象标记 对象为群聊
            send_string_with_length(c, "group_chat")
            # 发送加入聊天室的用户名
            send_string_with_length(c, connection_user[connection])
            # 发送加入聊天室的信息
            send_string_with_length(c, "* [SYSTEM MESSAGE] " + connection_user[connection] + " joins the chat room")

    # 否则调用函数获取聊天对象和内容
    else:
        # 调用函数接收客户端发送的聊天对象和内容
        chat_user = recv_all_string(connection)
        content = recv_all_string(connection)
        # 如果内容是exit标记 则有用户退出聊天室
        if content == "exit":
            # 给所有在线用户发送用户退出聊天室信息
            for c in online_connection:
                # 发送消息标记
                send_string_with_length(c, "#!message#!")
                # 发送聊天对象标记 对象为群聊
                send_string_with_length(c, "group_chat")
                # 发送离开聊天室的用户名
                send_string_with_length(c, connection_user[connection])
                # 发送加入聊天室的信息
                send_string_with_length(c, "* [SYSTEM MESSAGE] " + connection_user[connection] + " has left the chat room")
        
        # 否则查看聊天对象
        else:
            # 如果聊天对象是群聊
            if chat_user == "[Public chat]":
                # 发送给所有在线客户端
                for c in online_connection:
                    # 发送消息标记
                    send_string_with_length(c, "#!message#!")
                    # 发送聊天对象标记 对象为群聊
                    send_string_with_length(c, "group_chat")
                    # 发送消息发出者的用户名
                    send_string_with_length(c, connection_user[connection])
                    # 发送消息
                    send_string_with_length(c, content)
            
            # 否则聊天对象是私聊
            else:
                # 寻找聊天对象
                for c in online_connection:
                    # 从字典中查找到对象
                    if connection_user[c] == chat_user:
                        # 发送消息标记
                        send_string_with_length(c, "#!message#!")
                        # 发送聊天对象标记 对象为私聊
                        send_string_with_length(c, "private_chat")
                        # 发送消息发出者的用户名
                        send_string_with_length(c, connection_user[connection])
                        # 发送消息
                        send_string_with_length(c, content)
                        # 给自己发送消息
                        send_string_with_length(connection, "#!message#!")
                        send_string_with_length(connection, "private_chat")
                        send_string_with_length(connection, connection_user[connection])
                        send_string_with_length(connection, content)

    # 把加入聊天标记置为0
    flag = 0
    return True

# 处理请求线程的执行函数
def handle(connection, address):
    try:
        while True:
            # 接收客户端发送的请求类型
            request_type = str(connection.recv(1024).decode())
            # 是否继续处理标记
            no_go = True

            # 登录请求
            if request_type == "1":
                print("Start processing login request...")
                # 调用函数处理请求
                no_go = handle_login(connection, address)
            # 注册请求
            elif request_type == "2":
                print("Start processing sign up request...")
                no_go = handle_register(connection, address)
            # 发送消息请求
            elif request_type == "3":
                print("Start processing send message request")
                no_go = handle_message(connection, address)
            # 刷新用户列表请求
            elif request_type == "4":
                print("Start processing refurbish user list request")
                no_go = handle_online_list()
            if not no_go:
                break
    
    except Exception as err:
        print(str(address) + " connection failed, ready to disconnect: " + str(err))
    finally:
        try:
            connection.close()
            online_connection.remove(connection)
            connection.pop(connection)
        except:
            print(str(address) + "disconnection failed")

# 入口
if __name__ == "__main__":
    try:
        # 创建接收客户端连接的socket
        server = socket.socket()
        # 绑定主机及端口号
        CHAT_IP = socket.gethostbyname(socket.gethostname())
        CHAT_PORT = 1112
        SERVER = (CHAT_IP, CHAT_PORT)
        server.bind(SERVER)
        # 最大挂起数
        server.listen(10)
        print("Server initialized, staring monitorization...")
        while True:
            # 接受客户端的连接并创建子线程处理相应内容
            connection, address = server.accept()
            Thread(target=handle, args=(connection, address)).start()
    except Exception as err:
        print("Server error: " + str(err))