# 创建了socket 以及向服务器发送不同类型请求的实例方法
# 这些实例只是做相应的处理请求 并没有直接向服务器发送消息和接收消息 而是单独调用被封装的发送消息和接收消息的实例方法
# 可以实现可重用代码 不用每个请求中都重复输入这段代码 这样每一个处理实例中只需输入一句调用语句
# 注意此代码为客户端main中调用 单独运行无效果

import math
import socket

class ChatSocket:
    # 构造方法
    def __init__(self):
        print("Initializing tcp client...")
        # 创建连接服务器的socket
        self.client_socket = socket.socket()
        CHAT_IP = socket.gethostbyname(socket.gethostname())
        CHAT_PORT = 1112
        SERVER = (CHAT_IP, CHAT_PORT)
        self.client_socket.connect(SERVER)
    
    # 请求登陆类型
    def login_type(self, user_name, password):
        # 发送请求登陆标记给服务器
        self.client_socket.sendall(bytes("1", "utf-8"))
        # 依次调用实例方法向服务器发送用户名和密码
        self.send_string_with_length(user_name)
        self.send_string_with_length(password)
        # 调用实例方法获取服务器的返回值
        check_result = self.recv_string_by_length(1)
        # True代表登录请求通过 False代表登录请求失败
        return check_result
    
    # 请求注册类型
    def register_user(self, user_name, password, file_name):
        # 发送请求注册标记给服务器
        self.client_socket.sendall(bytes("2", "utf-8"))
        # 依次调用实例方法向服务器发送用户名 密码和头像路径
        self.send_string_with_length(user_name)
        self.send_string_with_length(password)
        self.send_string_with_length(file_name)
        # 调用实例方法获取服务器的返回值
        # "0"代表添加用户成功 "1"代表已有用户 "2"代表其他错误
        return self.recv_string_by_length(1)
    
    # 发送消息类型
    def send_message(self, message, chat_user):
        # 发送消息标记给服务器
        self.client_socket.sendall(bytes("3", "utf-8"))
        # 调用实例方法发送聊天对象 默认为群聊
        self.send_string_with_length(chat_user)
        # 调用此对象实例方法发送消息内容给服务器
        self.send_string_with_length(message)
    
    # 发送刷新用户列表类型
    def send_refurbish_mark(self):
        # 发送刷新用户列表标记给服务器
        self.client_socket.sendall(bytes("4", "utf-8"))
    
    # 封装发送与接受数据方法

    # 发送带长度的字符串
    def send_string_with_length(self, content):
        # 发送内容的长度
        self.client_socket.sendall(bytes(content, encoding="utf-8").__len__().to_bytes(4, byteorder="big"))
        # 发送内容
        self.client_socket.sendall(bytes(content, encoding="utf-8"))

    # 获取服务器传来的定长字符串
    def recv_string_by_length(self, len):
        return str(self.client_socket.recv(len), "utf-8")

    # 获取服务端传来的变长字符串 此时服务器会先传一个长度值
    def recv_all_string(self):
        # 获取消息长度
        length = int.from_bytes(self.client_socket.recv(4), byteorder="big")
        # utf-8编码中汉字占3字节 英文占1字节
        b_size = 3 * 1024
        times = math.ceil(length / b_size)
        content = ""
        for i in range(times):
            if i == times - 1:
                seg_b = self.client_socket.recv(length % b_size)
            else:
                seg_b = self.client_socket.recv(b_size)
            content += str(seg_b, encoding="utf-8")
        return content

    # 获取服务器发的在线用户人数
    def recv_number(self):
        return int.from_bytes(self.client_socket.recv(4), byteorder="big")