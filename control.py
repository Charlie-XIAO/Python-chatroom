from tkinter import *
from tkinter import messagebox
import os

def control_panel():
    # 创建主窗口
    root = Tk()
    # 设置背景颜色
    root.configure(background="#F0F0F0")
    # 设置标题
    root.title("Chat system (Powered by C & R)")
    # 设置位置大小
    root.geometry("400x200+0+0")

    # 创建新建用户按钮
    # 按钮事件为add_new_client函数
    new_client = Button(root, text="New client", fg="#00BFFF", width=16, height=2, font=("Arial", 16), command=add_new_client)
    new_client.place(x=14,y=97)

    # 创建打开服务器按钮
    # 按钮事件为start_server函数
    server_b = Button(root, text="Start server", fg="#00BFFF", width=16, height=2, font=("Arial", 16), command=start_server)
    server_b.place(x=14,y=27)

    # gif的帧数
    numIdx = 4
    # 循环遍历gif的帧
    frames = [PhotoImage(file="Control_pad.gif", format="gif -index %i" % (i)) for i in range(numIdx)]
    # 创建存放gif的标签
    imgLabel = Label(root, height=150, width=150)
    imgLabel.place(x=225, y=22)

    # 定时器函数 用于刷新gif的帧
    def update(idx):
        frame = frames[idx]
        # 切换到下一张的序号
        idx += 1
        imgLabel.configure(image=frame)
        # 100毫秒之后继续执行定时器函数
        root.after(100, update, idx % numIdx)
    
    # 执行循环mainloop和显示界面
    update(0)
    root.mainloop()

# 新建用户函数
def add_new_client():
    # 如果服务器已启动 启动新用户子线程
    if server_check == 1:
        os.startfile(os.path.join(os.path.dirname(__file__), "main.py"))
    # 如果服务器未启动 警告应先启动服务器
    else:
        messagebox.showwarning(title="Warning", message="Please start server first!")

# 打开服务器函数
def start_server():

    global server_check

    # 如果服务器未启动 启动服务器
    if server_check == 0:
        # 设置为服务器已启动
        server_check = 1
        # 启动服务器
        os.startfile(os.path.join(os.path.dirname(__file__), "server.py"))
    # 如果服务器已启动 警告已启动服务器
    else:
        messagebox.showwarning(title="Warning", message="Server already started!")
# 设置为服务器未启动
server_check = 0
# 显示控制面板
control_panel()
