from tkinter import *
from PIL import Image

# 注册界面类
class RegisterPanel:

    # 构造方法 参数为按钮事件处理函数
    # 从客户端main传入 可实现按钮回调
    def __init__(self, file_open_face, close_register_window, register_submit):
        # 初始化参数实例变量
        self.file_open_face = file_open_face
        self.close_register_window = close_register_window
        self.register_submit = register_submit
        # 文件路径
        self.file_name = ""
    
    # 显示注册界面实例方法
    def show_register_panel(self):

        global register_frame
        global frames
        global imgLabel
        global numIdx
    
        # 创建主窗口
        self.register_frame = Tk()
        # 设置背景颜色
        self.register_frame.configure(background="lightgrey")
        # 绑定全局变量
        register_frame = self.register_frame

        # 设置窗口大小 位置 (居中)
        width, height = 503, 400
        self.register_frame.geometry("%dx%d+%d+%d" % (\
            width, height, (self.register_frame.winfo_screenwidth() - width) / 2, \
            (self.register_frame.winfo_screenheight() - 1.2 * height) / 2))
        # 设置窗口标题
        self.register_frame.title("Sign up")
        # 声明窗口大小不可变
        self.register_frame.resizable(width=False, height=False)

        # 把图片转化为PhotoImage类型
        self.pp1 = PhotoImage(file="add_profile_button.png")

        # gif的帧数
        numIdx = 3
        # 循环遍历gif的帧
        frames = [PhotoImage(file="register.gif", format="gif -index %i" % (i)) for i in range(numIdx)]
        # 创建存放gif的标签
        imgLabel = Label(self.register_frame, height=400, width=500)
        imgLabel.place(x=-252, y=-200, relx=0.5, rely=0.5, relwidth=1, relheight=0.5)

        # 创建用户存放头像文本框
        self.face_show = Text(self.register_frame, bg="#F8F8FF", height=3.5, width=7, highlightcolor="#F8F8FF")
        self.face_show.place(x=370, y=230)
        # 设置文本框不可编辑
        self.face_show.config(state=DISABLED)

        # 声明图片宽度 高度
        self.width = 50
        self.height = 50
        # 在注册页面文本框中显示默认头像
        img = Image.open("default_profile.png")
        out = img.resize((self.width, self.height), Image.ANTIALIAS)
        out.save(r"profile.png", "png")

        # 头像转换为PhotoImage类 用于在文本框显示
        self.pp2 = PhotoImage(file="profile.png")
        # 设置文本框可编辑
        self.face_show.config(state=NORMAL)
        # 把头像图片插入文本框
        self.face_show.image_create(END, image=self.pp2)
        # 设置文本框不可编辑
        self.face_show.config(state=DISABLED)
        # 设置文本框滑到最低
        self.face_show.see(END)

        # 创建用户名 密码和确认密码的文本标签
        usernameLabel = Label(self.register_frame, text="Username: ", font=("Arial", 12), bg="lightgrey", fg="black")
        usernameLabel.place(x=116, y=230)
        passwordLabel = Label(self.register_frame, text="Password: ", font=("Arial", 12), bg="lightgrey", fg="black")
        passwordLabel.place(x=117, y=260)
        repasswordLabel = Label(self.register_frame, text="Confirm password: ", font=("Arial", 12), bg="lightgrey", fg="black")
        repasswordLabel.place(x=60, y=290)

        # 声明用户名 密码和确认密码变量
        self.user_name = StringVar()
        self.password = StringVar()
        self.confirm_password = StringVar()

        # 设置输入框及位置
        self.entry1 = Entry(self.register_frame, textvariable=self.user_name, fg="black", width=20)
        self.entry1.place(x=195, y=230)
        self.entry2 = Entry(self.register_frame, textvariable=self.password, show="*", fg="black", width=20)
        self.entry2.place(x=195, y=260)
        self.entry3 = Entry(self.register_frame, textvariable=self.confirm_password, show="*", fg="black", width=20)
        self.entry3.place(x=195, y=290)

        # 创建退出注册页面按钮
        # 按钮事件为close_register_window函数
        self.button_quit = Button(self.register_frame, text="Back", relief=FLAT, bg="lightgrey", fg="black", \
            font=("Arial", 15), command=self.close_register_window)
        self.button_quit.place(x=0, y=360)

        # 绑定回车键
        self.register_frame.bind("<Return>", self.register_submit)
        # 创建注册按钮
        # 按钮事件为register.submit函数
        self.button_register = Button(self.register_frame, text="Sign up right now", bg="#00BFFF", fg="white", \
            width=27, height=2, font=("Arial", 15), command=lambda: self.register_submit(self))
        self.button_register.place(x=120, y=330)

        # 创建添加头像按钮
        # 按钮事件为file_open_face函数
        self.button_file_open = Button(self.register_frame, image=self.pp1, relief=FLAT, bd=2, command=self.file_open_face)
        self.button_file_open.place(x=430, y=230)

    # 定时器函数 用于刷新gif的帧
    def update(idx):
        frame = frames[idx]
        # 切换到下一张的序号
        idx += 1
        imgLabel.configure(image=frame)
        # 500毫秒之后继续执行定时器函数
        register_frame.after(500, RegisterPanel.update, idx % numIdx)
    
    # 执行循环mainloop显示界面实例方法
    def load(self):
        RegisterPanel.update(0)
        self.register_frame.mainloop()
    
    # 添加头像实例方法
    def add_face(self, file_name):
        self.file_name = file_name
        # 调整头像大小与文件格式
        img = Image.open(file_name)
        out = img.resize((self.width, self.height), Image.ANTIALIAS)
        out.save(r"profile.png", "png")
        # 把头像转化为PhotoImage
        self.p = PhotoImage(file="profile.png")
        # 设置文本框可编辑
        self.face_show.config(state=NORMAL)
        self.face_show.delete("0.0", END)
        # 头像插入文本框
        self.face_show.image_create(END, image=self.p)
        # 设置文本不可编辑
        self.face_show.config(state=DISABLED)
        # 设置文本框滑到最低
        self.face_show.see(END)
    
    # 关闭注册界面实例方法
    def close_register_panel(self):
        if self.register_frame is None:
            print("Interface not generated properly")
        else:
            # 关闭登录界面
            self.register_frame.destroy()
        
    # 获取输入的用户名密码实例方法
    def get_input(self):
        return self.user_name.get(), self.password.get(), self.confirm_password.get(), self.file_name