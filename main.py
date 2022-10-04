# 当运行main模块时 会先从程序入口开始运行 执行go_to_login_panel函数
# 这个函数首先创建chat_client模块的ChatSocket对象 创建对象的同时创建的socket连接服务器
# 之后再创建了chat_login_panel模块的对象显示界面 参数为这个界面的两个按钮处理事件以及关闭界面函数
# 其他界面类似

from tkinter import messagebox
import threading
import time
import tkinter.filedialog

# 导入自定义模块
import chat_register_panel
import chat_main_panel
import chat_login_panel
import chat_client

# 声明全局变量默认为群聊
chat_user = "[Public chat]"

# 关闭socket函数
def close_socket():
    print("Disconnecting socket...")
    # 对象调用实例方法关闭socket
    client.client_socket.close()

# 关闭登陆界面函数
def close_login_window():
    # 关闭前先调用关闭socket函数
    close_socket()
    # 对象调用实例方法关闭登陆界面
    login_frame.login_frame.destroy()

# 关闭聊天界面函数
def close_main_window():
    # 关闭前先用对象调用实例方法给服务器发送用户退出聊天室标记
    client.send_message("exit", chat_user)
    # 调用关闭socket函数
    close_socket()
    # 对象调用实例方法关闭登陆界面
    main_frame.main_frame.destroy()

# 打开文件对话框函数 用于添加头像
def file_open_face():
    # 打开文件对话框
    file_name = tkinter.filedialog.askopenfilename()
    # 路径不为空 则读取图片并在头像中显示
    if file_name != "":
        # 对象调用实例方法添加头像
        register_frame.add_face(file_name)
    else:
        messagebox.showwarning(title="Warning", message="You haven't selected a file!")

# 处理私聊功能函数
def private_talk(self):

    global chat_user

    # 对象使用实例变量 也就是列表组件获取点击的索引
    indices = main_frame.friend_list.curselection()
    index = indices[0]
    if index > 0:
        # 获取点击的用户名
        chat_user = main_frame.friend_list.get(index)

        # 修改标题名称
        # 如果聊天对象为群聊
        if chat_user == "[Public chat]":
            title = "Online user" + " " * 10 + "Welcome to Public chat room: " + \
                main_frame.user_name + " " * (40 - len(main_frame.user_name))
            main_frame.change_title(title)

        # 如果用户选择了自己
        elif chat_user == main_frame.user_name:
            messagebox.showwarning(title="Warning", message="You cannot chat with yourself!")
            # 把聊天对象改回群聊
            chat_user = "[Public chat]"
        
        # 如果聊天对象为私聊
        else:
            title = "[Private chat]" + " " * 15 + main_frame.user_name + " > " + chat_user + \
                " " * (75 - len(main_frame.user_name) - len(chat_user))
            main_frame.change_title(title)

# 登录按钮处理事件函数
def handding_login(self):
    # 调用chat_login_panel模块的对象实例方法获取输入的用户名和密码
    user_name, password = login_frame.get_input()
    # 判断用户名和密码不能为空
    if user_name == "":
        messagebox.showwarning(title="Warning", message="Username cannot be empty!")
        return
    if password == "":
        messagebox.showwarning(title="Warning", message="Password cannot be empty!")
        return
    # 调用在此类创建的chat_client模块的对象的实例方法
    # 如果返回True 则代表登陆成功
    if client.login_type(user_name, password) == "1":
        # 调用此类的前往聊天主界面函数 参数为用户名
        go_to_main_panel(user_name)
    else:
        messagebox.showwarning(title="Warning", message="Wrong username or password!")

# 登陆界面注册按钮处理事件函数
def handding_register():
    # 调用在此类创建的login_frame对象的实例方法关闭登陆界面
    login_frame.close_login_panel()

    global register_frame

    # 创建chat_register_panel模块的注册界面的对象 把此类关闭注册页面前往登录界面的函数close_register_window
    # 注册按钮事件函数register_submit打开文件对话框 添加头像函数作为参数
    # 把chat_login_pannel模块的事件与这些函数绑定
    register_frame = chat_register_panel.RegisterPanel(file_open_face, close_register_window, register_submit)
    # 调用对象的实例方法显示注册界面
    register_frame.show_register_panel()
    register_frame.load()

# 关闭注册界面函数
def close_register_window():
    # 调用在此类创建的register_frame对象的实例方法关闭注册界面
    register_frame.close_register_panel()

    global login_frame

    # 创建chat_login_panel模块的登录界面的对象 把此类登录处理函数handding_login
    # 注册处理函数作handding_register 关闭登录界面客户端的socket的close_login_window作为参数
    # 把chat_login_pannel模块的事件与这些函数绑定
    login_frame = chat_login_panel.LoginPanel(handding_login, handding_register, close_login_window)
    # 调用对象的实例方法显示聊天主界面
    login_frame.show_login_panel()
    login_frame.load()

# 注册界面注册按钮处理事件函数
def register_submit(self):
    # 调用在此类创建的对象实例方法获取用户名 密码 确认密码和头像文件路径
    user_name, password, confirm_password, file_name = register_frame.get_input()
    # 判断用户名 密码和确认密码不可为空
    if user_name == "" or password == "" or confirm_password == "":
        messagebox.showwarning("Cannot be empty", "Please complete the sign up form!")
        return
    # 判断密码和确认密码是否一致
    if not password == confirm_password:
        messagebox.showwarning("Error", "Two passwords are different!")
        return
    # 判断头像不可为空
    if register_frame.file_name == "":
        messagebox.showwarning("Error", "Please select a profile!")
        return
    
    # 对象调用实例方法发送消息给服务器
    result = client.register_user(user_name, password, file_name)
    # 返回0则注册成功 跳往登录界面
    if result == "0":
        messagebox.showinfo("Succeed", "Sign up succeed!")
        # 调用函数关闭注册页面前往登陆界面函数
        close_register_window()

    # 返回1则已有用户
    elif result == "1":
        # 用户名重复
        messagebox.showerror("Error", "Username has already been used!")
    
    # 返回2则为其他错误
    elif result == "2":
        # 未知错误
        messagebox.showerror("Error", "Unknown error detected!")
    
# 发送消息按钮处理事件函数
def send_message(self):

    global chat_user

    print("Send message:")
    # 调用在此类创建的chat_main_panel模块的对象的实例方法获取发送内容
    content = main_frame.get_send_text()
    # 调用在此类创建的chat_main_panel模块的对象的实例方法清空输入框内容
    main_frame.clear_send_text()
    # 判断内容不可为空
    if content.strip() == "":
        messagebox.showwarning(title="Warning", message="Cannot send empty message!")
        return
    else:
        print(content)
    # 调用在此类创建的chat_client模块的对象的实例方法发送聊天内容给服务器
    client.send_message(content, chat_user)

# 发送表情标记函数
def send_mark(exp):

    global chat_user

    # 调用在此类创建的chat_client模块的对象的实例方法发送表情标记给服务器
    client.send_message(exp, chat_user)

def send_picture(pic_file):

    global chat_user

    # 调用在此类创建的chat_client模块的对象的实例方法发送图片给服务器
    client.send_message(pic_file, chat_user)

# 刷新用户列表按钮处理事件函数
def refurbish_user():
    # 发送刷新用户列表标记给服务器
    client.send_refurbish_mark()

# 关闭登录界面前往主界面
def go_to_main_panel(user_name):
    # 调用login_frame对象的实例方法关闭窗口
    login_frame.close_login_panel()
    
    global main_frame

    # 创建chat_main_panel模块的对象
    # 把用户名 此类的发送消息函数 发送表情包标记函数 私聊功能函数 关闭聊天界面函数作为参数
    # 把chat_main_panel模块的事件与这些函数绑定
    main_frame = chat_main_panel.MainPanel(user_name, send_message, send_mark, send_picture, refurbish_user, private_talk, close_main_window)
    # 创建子线程专门负责接收并处理数据
    threading.Thread(target=recv_data).start()
    # 对象调用聊天主界面对象的实例方法创建组件布局并显示登录界面
    main_frame.show_main_panel()
    main_frame.load()

# 处理消息接收的线程方法
def recv_data():
    # 暂停1秒 等待主界面渲染完毕
    time.sleep(1)
    while True:
        try:
            # 获取处理数据类型
            # 调用对象实例方法获取服务器发送的消息
            data_type = client.recv_all_string()
            print("recv type: " + data_type)
            # 获取当前在线用户列表
            if data_type == "#!onlinelist#!":
                print("Accessing online user data...")
                # 创建列表存储用户
                online_list = list()
                # 对象调用实例方法获取在线用户数
                online_number = client.recv_number()
                for n in range(online_number):
                    # 对象每次调用实例方法获取服务器发送的用户名 都添加到列表中
                    online_list.append(client.recv_all_string())
                # 对象调用实例方法刷新聊天界面用户在线列表
                main_frame.refresh_friends(online_number, online_list)
                print(online_list)
            
            elif data_type == "#!message#!":
                print("Accessing new message")
                # 调用对象实例方法获取服务器发送的聊天对象及用户名
                chat_flag = client.recv_all_string()
                user = client.recv_all_string()
                print("User: " + user)
                # 调用对象实例方法获取服务器发送的内容
                content = client.recv_all_string()
                print("Message: " + content)
                # 对象调用实例方法显示消息
                main_frame.show_send_message(user, content, chat_flag)

        except Exception as err:
            print("Error accepting server message, subthread ended. " + str(err))
            break

# 前往登录界面 同时开启客户端口连接服务器的函数
def go_to_login_panel():

    global login_frame
    global client
    
    # 创建chat_client模块中的客户端连接服务器的socket对象
    client = chat_client.ChatSocket()

    # 创建chat_login_panel模块的登录界面的对象 把此类登录处理函数handding_login
    # 注册处理函数作handding_register 关闭登录界面客户端的socket中close_login_window函数作为参数
    # 把chat_login_pannel模块的事件与这些函数绑定
    login_frame = chat_login_panel.LoginPanel(handding_login, handding_register, close_login_window)
    # 对象调用聊天主界面对象的实例方法创建组件并显示界面
    login_frame.show_login_panel()
    login_frame.load()

# 入口
if __name__ == "__main__":
    # 调用此类的前往登录界面函数
    go_to_login_panel()