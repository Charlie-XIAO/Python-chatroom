# 创建登陆界面类LoginPanel - 类的构造方法是初始化从客户端传入的函数 用与处理按钮事件 当用户点击按钮时便会回调给客户端处理
# 实例方法show_login_panel - 封装组件 实现多人登陆且登陆界面互不干扰

# 客户端调用过程
# 首先调用实例方法show_login_panel创建组件
# 然后调用load循环函数显示界面

from tkinter import *

# 登陆界面类
class LoginPanel:

    # 构造方法 参数为按钮事件处理函数
    # 从客户端main传入 可实现按钮回调
    def __init__(self, handle_login, handle_register, close_login_window):
        # 初始化参数实例变量
        self.handle_login = handle_login
        self.handle_register = handle_register
        self.close_login_window = close_login_window
    
    # 显示登陆界面的实例方法
    def show_login_panel(self):

        global login_frame
        global frames
        global imgLabel
        global numIdx

        # 创建主窗口
        self.login_frame = Tk()
        # 设置背景颜色
        self.login_frame.configure(background="lightgrey")
        # 绑定全局变量
        login_frame = self.login_frame
        # 设置窗口关闭按钮回调 用于退出时断开socket连接
        self.login_frame.protocol("WM_DELETE_WINDOW", self.close_login_window)

        # 设置窗口大小 位置 (居中)
        width, height = 503, 400
        self.login_frame.geometry("%dx%d+%d+%d" % (\
            width, height, (self.login_frame.winfo_screenwidth() - width) / 2, \
            (self.login_frame.winfo_screenheight() - 1.2 * height) / 2))
        # 设置窗口标题
        self.login_frame.title("Login")
        # 声明窗口大小不可变
        self.login_frame.resizable(width=False, height=False)

        # gif的帧数
        numIdx = 13
        # 循环遍历gif的帧
        frames = [PhotoImage(file="login.gif", format="gif -index %i" % (i)) for i in range(numIdx)]
        # 创建存放gif的标签
        imgLabel = Label(self.login_frame, height=300, width=500)
        imgLabel.place(x=-252, y=-200, relx=0.5, rely=0.5, relwidth=1, relheight=0.5)

        # 创建昵称和密码的文本标签
        nicknameLabel = Label(login_frame, text="Username: ", font=("Arial", 12), bg="lightgrey", fg="black")
        nicknameLabel.place(x=100, y=230)
        passwordLabel = Label(login_frame, text="Password: ", font=("Arial", 12), bg="lightgrey", fg="black")
        passwordLabel.place(x=100, y=260)

        # 声明用户名密码变量
        self.user_name = StringVar()
        self.password = StringVar()

        # 设置输入框及位置
        self.entry1 = Entry(login_frame, textvariable=self.user_name, fg="black", width=25)
        self.entry1.place(x=190, y=230)
        self.entry2 = Entry(login_frame, textvariable=self.password, show="*", fg="black", width=25)
        self.entry2.place(x=190, y=260)

        # 创建注册按钮
        # 按钮事件为handle_register函数
        self.button_register = Button(login_frame, text="Sign up", relief=FLAT, \
            bg="lightgrey", fg="black", font=("Arial", 15), command=self.handle_register)
        self.button_register.place(x=0, y=360)

        # 绑定回车键
        self.login_frame.bind("<Return>", self.handle_login)
        # 创建登录按钮
        # 按钮事件为handle_login函数
        self.button_login = Button(login_frame, text="Log in", bg="#00BFFF", fg="white", \
            width=21, height=2, font=("Arial", 15), command=lambda: self.handle_login(self))
        self.button_login.place(x=160, y=300)
    
    # 定时器函数 用于刷新gif的帧
    def update(idx):
        frame = frames[idx]
        # 切换到下一张的序号
        idx += 1
        imgLabel.configure(image=frame)
        # 200毫秒之后继续执行定时器函数
        login_frame.after(200, LoginPanel.update, idx % numIdx)
    
    # 执行循环mainloop显示界面实例方法
    def load(self):
        LoginPanel.update(0)
        self.login_frame.mainloop()

    # 关闭登录界面实例方法
    def close_login_panel(self):
        if self.login_frame is None:
            print("Interface not generated properly")
        else:
            # 关闭登录界面
            self.login_frame.destroy()

    # 获取输入的用户名密码实例方法
    def get_input(self):
        return self.user_name.get(), self.password.get()