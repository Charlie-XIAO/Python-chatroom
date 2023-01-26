import os
from tkinter import *
import tkinter.font as tf
import tkinter.filedialog
import time
import chat_mysql
from random import random
from PIL import Image
from nltk.util import ngrams

# 主界面类
class MainPanel:

    # 构造方法 参数为按钮事件处理函数
    # 从客户端main传入 可实现按钮回调
    def __init__(self, user_name, send_message, send_mark, send_picture, refurbish_user, private_talk, close_main_window):
        # 初始化参数实例变量
        self.user_name = user_name
        self.send_message = send_message
        self.send_mark = send_mark
        self.send_picture = send_picture
        self.refurbish_user = refurbish_user
        self.private_talk = private_talk
        self.close_main_window = close_main_window
        # 用字典将标记与表情图片对应 用于接收标记判断表情贴图
        self.dic = {}
        # 判断表情面板开关的标志
        self.ee = 0
        # 用字典将图片文件名与图片对应 用于接收要发送的图片
        self.pic = {}
        # 存储头像列表
        self.face = []
        # indexer聊天记录索引器
        self.indexer = {}

    # 显示聊天界面的实例方法
    def show_main_panel(self):

        global main_frame
        global frames
        global imgLabel
        global numIdx
    
        # 创建主窗口
        main_frame = Tk()
        # 全局变量绑定于实例变量
        self.main_frame = main_frame
        # 设置主窗口标题
        self.main_frame.title("Python Chat Room (Powered C & R)")
        # 设置主窗口颜色
        self.main_frame.configure(background="#F8F8FF")
        # 设置窗口关闭按钮回调 用于退出时断开socket连接
        self.main_frame.protocol("WM_DELETE_WINDOW", self.close_main_window)

        # 设置窗口大小 位置 (居中)
        width, height = 1000, 700
        # width, height = 1300, 700
        self.main_frame.geometry("%dx%d+%d+%d" % (\
            width, height, (self.main_frame.winfo_screenwidth() - width) / 2, \
            (self.main_frame.winfo_screenheight() - 1.2 * height) / 2))
        # 声明窗口大小不可变
        self.main_frame.resizable(width=False, height=False)

        # 表情图片 把图片转换为PhotoImage
        self.p1 = PhotoImage(file="emojis/Emoji1.png")
        self.p2 = PhotoImage(file="emojis/Emoji2.png")
        self.p3 = PhotoImage(file="emojis/Emoji3.png")
        self.p4 = PhotoImage(file="emojis/Emoji4.png")
        self.p5 = PhotoImage(file="emojis/Emoji5.png")
        self.p6 = PhotoImage(file="emojis/Emoji6.png")
        self.p7 = PhotoImage(file="emojis/Emoji7.png")
        self.p8 = PhotoImage(file="emojis/Emoji8.png")
        self.p9 = PhotoImage(file="emojis/Emoji9.png")
        self.p10 = PhotoImage(file="emojis/Emoji10.png")
        self.p11 = PhotoImage(file="emojis/Emoji11.png")
        self.p12 = PhotoImage(file="emojis/Emoji12.png")
        self.p13 = PhotoImage(file="emojis/Emoji13.png")
        self.p14 = PhotoImage(file="emojis/Emoji14.png")
        self.p15 = PhotoImage(file="emojis/Emoji15.png")

        # 按钮图片 把图片转换为PhotoImage
        self.p_1 = PhotoImage(file="Emoji_button.png")
        self.p_2 = PhotoImage(file="Chat_history_button.png")
        self.p_3 = PhotoImage(file="Search_button.png")
        self.p_4 = PhotoImage(file="2048_button.png")
        self.p_5 = PhotoImage(file="Send_picture_button.png")
        self.p_6 = PhotoImage(file="Snake_button.png")

        # 表情包字典 每一个表情包对应一个标记
        self.dic = {"aa**": self.p1, "bb**": self.p2, "cc**": self.p3, "dd**": self.p4, "ee**": self.p5, \
                    "ff**": self.p6, "gg**": self.p7, "hh**": self.p8, "jj**": self.p9, "kk**": self.p10, \
                    "ll**": self.p11, "mm**": self.p12, "nn**": self.p13, "pp**": self.p14, "qq**": self.p15}
        
        # 创建文本标签
        self.label1 = Label(self.main_frame, text="Online user" + " " * 10 + "Welcome to Python Chat room: " + \
            self.user_name + " " * (40 - len(self.user_name)), font=("Arial", 20), bg="#00BFFF", fg="white")
        self.label1.grid(row=0, column=0, ipady=0, padx=0, columnspan=3, sticky=E+W)

        # 声明在线用户列表框变量
        friend_list_var = StringVar()

        # 设置列表框及位置
        self.friend_list = Listbox(self.main_frame, selectmode=NO, listvariable=friend_list_var, \
            bg="#F8F8FF", fg="#00BFFF", font=("Arial", 14), highlightcolor="#F8F8FF", selectbackground="#00BFFF")
        self.friend_list.grid(row=1, column=0, rowspan=3, sticky=N+S, padx=0, pady=(0, 0))
        # 绑定列表框点击事件
        self.friend_list.bind("<ButtonRelease-1>", self.private_talk)

        # 设置列表框缩放比例
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # 创建列表框滚动条
        sc_bar = Scrollbar(self.main_frame, activebackground="red")
        sc_bar.grid(row=1, column=0, sticky=N+S+E, rowspan=3, pady=(0, 3))

        # 列表框与列表框滚动条绑定
        sc_bar["command"] = self.friend_list.yview
        self.friend_list["yscrollcommand"] = sc_bar.set

        # 创建消息框滚动条
        msg_sc_bar = Scrollbar(self.main_frame)
        msg_sc_bar.grid(row=1, column=1, sticky=E+N+S, padx=(0, 1), pady=1)

        # 创建显示消息的文本框
        self.message_text = Text(self.main_frame, bg="#F8F8FF", height=1, highlightcolor="#F8F8FF", highlightthickness=1)
        self.message_text.grid(row=1, column=1, sticky=W+E+N+S, padx=(0, 15), pady=(0, 27))
        # 声明显示消息的文本框不可编辑
        # 当需要修改内容时 再修改state为可以编辑模式NORMAL
        self.message_text.config(state=DISABLED)

        # 消息框与消息框滚动条绑定
        msg_sc_bar["command"] = self.message_text.yview
        self.message_text["yscrollcommand"] = msg_sc_bar.set

        # # gif的帧数
        # numIdx = 4
        # # 循环遍历gif的帧
        # frames = [PhotoImage(file="main.gif", format="gif -index %i" % (i)) for i in range(numIdx)]
        # # 创建存放gif的标签
        # imgLabel = Label(self.main_frame, height=400, width=490)
        # imgLabel.grid(row=1, column=2, sticky=W+E+N+S, rowspan=100, padx=(0, 0), pady=(160, 175))

        # 创建发送消息框滚动条
        send_sc_bar = Scrollbar(self.main_frame)
        send_sc_bar.grid(row=2, column=1, sticky=E+N+S, padx=(0, 1), pady=1)

        # 创建发送消息框
        self.send_text = Text(self.main_frame, bg="#F8F8FF", height=11, highlightcolor="#F8F8FF", highlightbackground="#444444", highlightthickness=0)
        self.send_text.grid(row=2, column=1, sticky=W+E+N+S, padx=(0, 15), pady=0)
        # 滚动到底部
        self.send_text.see(END)

        # 发送消息框与发送消息框滚动条绑定
        send_sc_bar["command"] = self.send_text.yview
        self.send_text["yscrollcommand"] = send_sc_bar.set

        # 发送按钮绑定回车键
        self.main_frame.bind("<Return>", self.send_message)

        # 创建发送消息按钮
        # 按钮事件为send_message函数
        button1 = Button(self.main_frame, command=lambda: self.send_message(self), text="Send", \
            bg="#00BFFF", fg="white", width=13, height=2, font=("Arial", 12))
        button1.place(x=850, y=640)
        # button1.place(x=650, y=640)

        # 创建关闭窗口按钮
        # 按钮事件为close_main_window函数
        button2 = Button(self.main_frame, text="Close", bg="#F8F8FF", fg="black", \
            width=13, height=2, font=("Arial", 12), command=self.close_main_window)
        button2.place(x=730, y=640)
        # button2.place(x=530, y=640)

        # 创建表情包按钮
        # 按钮事件为express函数
        button3 = Button(self.main_frame, command=self.express, image=self.p_1, relief=FLAT, bd=0)
        button3.place(x=227, y=525)

        # 创建发送图片按钮
        # 按钮事件为picture函数
        button8 = Button(self.main_frame, command=self.picture, image=self.p_5, relief=FLAT, bd=0)
        button8.place(x=254, y=525)

        # 创建聊天记录按钮
        # 按钮事件为create_window实例方法
        button4 = Button(self.main_frame, command=self.create_window, image=self.p_2, relief=FLAT, bd=0)
        button4.place(x=281, y=525)

        # 创建查找聊天记录按钮
        # 按钮事件为create_search_window实例方法
        button6 = Button(self.main_frame, command=self.create_search_window, image=self.p_3, relief=FLAT, bd=0)
        button6.place(x=308, y=525)

        # 创建2048游戏按钮
        # 按钮事件为game_2048实例方法
        button7 = Button(self.main_frame, command=self.game_2048, image=self.p_4, relief=FLAT, bd=0)
        button7.place(x=335, y=525)

        # 创建贪吃蛇游戏按钮
        # 按钮事件为game_snake实例方法
        button8 = Button(self.main_frame, command=self.game_snake, image=self.p_6, relief=FLAT, bd=0)
        button8.place(x=362, y=525)

        # 创建刷新用户列表按钮
        # 按钮事件为refurbish_user函数
        button5 = Button(self.main_frame, command=self.refurbish_user, text="Refurbish", \
            bg="#00BFFF", fg="white", width=13, height=2, font=("Arial", 12))
        button5.place(x=40, y=640)
    
    # # 定时器函数 用于刷新gif的帧
    # def update(idx):
    #     frame = frames[idx]
    #     # 切换到下一张的序号
    #     idx += 1
    #     imgLabel.configure(image=frame)
    #     # 200毫秒之后继续执行定时器函数
    #     main_frame.after(100, MainPanel.update, idx % numIdx)

    # 执行循环mainloop显示界面实例方法
    def load(self):
    #     MainPanel.update(0)
        self.main_frame.mainloop()

    # 聊天记录按钮处理事件实例方法
    def create_window(self):
        # 创建子窗口
        top1 = Toplevel()
        top1.configure(background="#FFFAFA")
        # 设置窗口大小 位置 (居中)
        width, height = 600, 650
        top1.geometry("%dx%d+%d+%d" % (\
            width, height, (top1.winfo_screenwidth() - width) / 2, \
            (top1.winfo_screenheight() - 1.2 * height) / 2))
        # 设置窗口标题
        top1.title("Chat history")
        # 声明窗口大小不可变
        top1.resizable(width=False, height=False)

        # 创建文本标签
        title_table = Label(top1, text="Chat history", font=("Arial", 20), fg="white", bg="#00BFFF")
        title_table.pack(ipady=10, fill=X)

        # 创建用户存放聊天记录信息文本框
        self.chatting_records = Text(top1, bg="#F8F8FF", height=50, highlightcolor="#F8F8FF", highlightthickness=1)
        self.chatting_records.pack(ipady=10, fill=X)
        # 声明显示消息的文本框不可编辑
        # 当需要修改内容时 再修改state为可以编辑模式NORMAL
        self.chatting_records.config(state=DISABLED)

        # 创建清除聊天记录按钮
        # 按钮事件为clear_chatting_records实例方法
        button6 = Button(top1, text="Clear history", command=self.clear_chatting_records, \
            bg="#00BFFF", fg="white", width=12, height=2, font=("Arial", 11))
        button6.place(x=480, y=600)

        # 调用实例方法显示聊天记录
        self.show_chatting_records()
    
    # 显示聊天记录实例方法
    def show_chatting_records(self):
        # 设置显示消息的文本框可编辑
        self.chatting_records.config(state=NORMAL)
        # 打开用户存放聊天记录的本地文件
        f = open(os.path.join(os.path.dirname(__file__), "chatting_records", self.user_name + ".txt"), "r")
        while True:
            # 每次读取一行
            content = f.readline()
            # 设置字体样式和大小
            self.chatting_records.tag_config("tag_9", foreground="#00BFFF", font=tf.Font(family="Arial", size=13))
            # 如果不为空 则在文本框最后一行插入文本
            if content != "":
                self.chatting_records.insert(END, content, "tag_9")
            # 否则重新声明显示消息的文本框不可编辑
            else:
                self.chatting_records.config(state=DISABLED)
                return
        
    # 清除聊天记录按钮处理实例方法
    def clear_chatting_records(self):
        # 设置显示消息的文本框可编辑
        self.chatting_records.config(state=NORMAL)
        # 删除文本框内容
        self.chatting_records.delete("1.0", END)
        # 打开聊天记录文件 以空字符串覆盖方式清楚内容
        a = open(os.path.join(os.path.dirname(__file__), "chatting_records", self.user_name + ".txt"), "w")
        a.write("")
        a.close()
        # 重新声明显示消息的文本框不可编辑
        self.chatting_records.config(state=DISABLED)

    # 保存聊天记录实例方法
    def sava_chatting_records(self, content):
        # 打开聊天记录文件 写入信息
        a = open(os.path.join(os.path.dirname(__file__), "chatting_records", self.user_name + ".txt"), "a")
        a.write(content)
        a.close()
    
    # 建立聊天记录索引实例方法
    def indexing_chatting_records(self, title, text):
        # 提取用户输入内容的单词
        # 根据空格拆分词句
        splitted_text = text.split()
        # 避免标点符号对单词判定的影响
        words = []
        for w in splitted_text:
            temp = ""
            for ch in w:
                if ch.isalpha():
                    temp += ch.lower()
            if temp != "":
                words.append(temp)
        # 把用户输入内容对应各个单词词组的索引
        for n in range(1, len(words) + 1):
            n_grams = ngrams(words, n)
            for tup in list(n_grams):
                phrase = " ".join(tup)
                if phrase not in self.indexer:
                    self.indexer[phrase] = [title + text,]
                else:
                    self.indexer[phrase].append(title + text)

    # 搜索聊天记录按钮处理事件实例方法
    def create_search_window(self):
        # 创建子窗口
        top2 = Toplevel()
        top2.configure(background="#FFFAFA")
        # 设置窗口大小 位置 (居中)
        width, height = 600, 650
        top2.geometry("%dx%d+%d+%d" % (\
            width, height, (top2.winfo_screenwidth() - width) / 2, \
            (top2.winfo_screenheight() - 1.2 * height) / 2))
        # 设置窗口标题
        top2.title("Search in chat history")
        # 声明窗口大小不可变
        top2.resizable(width=False, height=False)

        # 创建文本标签
        title_table = Label(top2, text="Search in chat history", font=("Arial", 20), fg="white", bg="#00BFFF")
        title_table.pack(ipady=10, fill=X)

        # 创建搜索消息栏
        search_frame = Frame(top2, relief=FLAT) 
        search_frame.pack(ipady=10, fill=X)

        # 创建搜索消息按钮
        # 按钮事件为search_message函数
        search_message_button = Button(search_frame, command=lambda: self.show_search_results(self.get_search_term()[:-1]), text="Search", \
            bg="#00BFFF", fg="white", font=("Arial", 11))
        search_message_button.pack(side=RIGHT)

        # 创建搜索消息框
        self.search_text = Text(search_frame, bg="#F8F8FF", height=2, highlightcolor="#F8F8FF", highlightbackground="#444444", highlightthickness=0)
        self.search_text.pack(side=LEFT, fill=X)

        # 创建用户存放聊天记录信息文本框
        self.search_chatting_records = Text(top2, bg="#F8F8FF", height=50, highlightcolor="#F8F8FF", highlightthickness=1)
        self.search_chatting_records.pack(ipady=10, fill=X)
        # 声明显示消息的文本框不可编辑
        # 当需要修改内容时 再修改state为可以编辑模式NORMAL
        self.search_chatting_records.config(state=DISABLED)

    def show_search_results(self, term):
        # 设置显示消息的文本框可编辑
        self.search_chatting_records.config(state=NORMAL)
        # 删除显示消息的文本框中原有的内容
        self.clear_search_result()
        # 设置字体样式和大小
        self.search_chatting_records.tag_config("tag_10", foreground="#00BFFF", font=tf.Font(family="Arial", size=13))
        # 在显示消息的文本框中显示所有搜索结果
        if term.lower() in self.indexer:
            # 新建临时存储搜索结果的集合
            # 避免重复显示同一搜索结果
            results = set()
            for result in self.indexer[term.lower()]:
                results.add(result)
            # 遍历搜索结果集合 在文本框最后一行插入文本 
            for result in results:
                self.search_chatting_records.insert(END, result, "tag_10")
        # 重新声明显示消息的文本框不可编辑
        self.search_chatting_records.config(state=DISABLED)
    
    # 定义2048游戏按钮处理事件实例方法
    def game_2048(self):
        # 打开2048_game.py文件启动游戏 不影响聊天室运行
        os.startfile(os.path.join(os.path.dirname(__file__), "game_2048.py"))
    
    # 定义贪吃蛇游戏按钮处理事件实例方法
    def game_snake(self):
        # 打开snake_game.py文件启动游戏 不影响聊天室运行
        os.startfile(os.path.join(os.path.dirname(__file__), "game_snake.py"))
    
    # 定义表情包按钮处理事件实例方法
    def express(self):
        # 如果ee标记为0 则弹出表情包
        if self.ee == 0:
            # 把ee标记置为1 用于下次点击按钮时销毁表情
            self.ee = 1
            # 创建表情图按钮
            self.b1 = Button(self.main_frame, command=self.bb1, image=self.p1, relief=FLAT, bd=0)
            self.b2 = Button(self.main_frame, command=self.bb2, image=self.p2, relief=FLAT, bd=0)
            self.b3 = Button(self.main_frame, command=self.bb3, image=self.p3, relief=FLAT, bd=0)
            self.b4 = Button(self.main_frame, command=self.bb4, image=self.p4, relief=FLAT, bd=0)
            self.b5 = Button(self.main_frame, command=self.bb5, image=self.p5, relief=FLAT, bd=0)
            self.b6 = Button(self.main_frame, command=self.bb6, image=self.p6, relief=FLAT, bd=0)
            self.b7 = Button(self.main_frame, command=self.bb7, image=self.p7, relief=FLAT, bd=0)
            self.b8 = Button(self.main_frame, command=self.bb8, image=self.p8, relief=FLAT, bd=0)
            self.b9 = Button(self.main_frame, command=self.bb9, image=self.p9, relief=FLAT, bd=0)
            self.b10 = Button(self.main_frame, command=self.bb10, image=self.p10, relief=FLAT, bd=0)
            self.b11 = Button(self.main_frame, command=self.bb11, image=self.p11, relief=FLAT, bd=0)
            self.b12 = Button(self.main_frame, command=self.bb12, image=self.p12, relief=FLAT, bd=0)
            self.b13 = Button(self.main_frame, command=self.bb13, image=self.p13, relief=FLAT, bd=0)
            self.b14 = Button(self.main_frame, command=self.bb14, image=self.p14, relief=FLAT, bd=0)
            self.b15 = Button(self.main_frame, command=self.bb15, image=self.p15, relief=FLAT, bd=0)
            # 设置表情包的位置
            self.b1.place(x=207, y=470)
            self.b2.place(x=255, y=470)
            self.b3.place(x=303, y=470)
            self.b4.place(x=351, y=470)
            self.b5.place(x=399, y=470)
            self.b6.place(x=207, y=420)
            self.b7.place(x=255, y=420)
            self.b8.place(x=303, y=420)
            self.b9.place(x=351, y=420)
            self.b10.place(x=399, y=420)
            self.b11.place(x=207, y=370)
            self.b12.place(x=255, y=370)
            self.b13.place(x=303, y=370)
            self.b14.place(x=351, y=370)
            self.b15.place(x=399, y=370)
        else:
            # 把ee标记置为0 并销毁所有按钮
            self.ee = 0
            self.b1.destroy()
            self.b2.destroy()
            self.b3.destroy()
            self.b4.destroy()
            self.b5.destroy()
            self.b6.destroy()
            self.b7.destroy()
            self.b8.destroy()
            self.b9.destroy()
            self.b10.destroy()
            self.b11.destroy()
            self.b12.destroy()
            self.b13.destroy()
            self.b14.destroy()
            self.b15.destroy()
    
    # 所有表情按钮处理实例方法
    def bb1(self):
        self.mark("aa**")
    def bb2(self):
        self.mark("bb**")
    def bb3(self):
        self.mark("cc**")
    def bb4(self):
        self.mark("dd**")
    def bb5(self):
        self.mark("ee**")
    def bb6(self):
        self.mark("ff**")
    def bb7(self):
        self.mark("gg**")
    def bb8(self):
        self.mark("hh**")
    def bb9(self):
        self.mark("jj**")
    def bb10(self):
        self.mark("kk**")
    def bb11(self):
        self.mark("ll**")
    def bb12(self):
        self.mark("mm**")
    def bb13(self):
        self.mark("nn**")
    def bb14(self):
        self.mark("pp**")
    def bb15(self):
        self.mark("qq**")

    # 处理发送表情实例方法
    # 参数为发送的表情图标记 发送后将按钮销毁
    def mark(self, exp):
        # 函数回调把标记作为参数
        self.send_mark(exp)
        # 发送后将所有按钮销毁
        self.b1.destroy()
        self.b2.destroy()
        self.b3.destroy()
        self.b4.destroy()
        self.b5.destroy()
        self.b6.destroy()
        self.b7.destroy()
        self.b8.destroy()
        self.b9.destroy()
        self.b10.destroy()
        self.b11.destroy()
        self.b12.destroy()
        self.b13.destroy()
        self.b14.destroy()
        self.b15.destroy()
        # 把ee标记重置为0
        self.ee = 0
    
    # 处理发送图片实例方法
    def picture(self):
        # 打开文件对话框
        pic_file = tkinter.filedialog.askopenfilename()
        # 打开发送的图片
        img = Image.open(pic_file)
        # 读取原始文件的长宽 计算横纵比
        width, height = img.size
        # 如果图片过大 等比例放缩至宽度为500
        if width > 500:
            width, height = 500, int(height / width * 500)
        # 调整图片大小与文件格式
        out = img.resize((width, height), Image.ANTIALIAS)
        out.save(pic_file[:-4] + "_save.png", "png")

        # 函数回调把PhotoImage图片作为参数
        self.send_picture("pic**" + pic_file)

    # 刷新在线列表实例方法
    def refresh_friends(self, online_number, names):
        # 删除当前在线列表
        self.friend_list.delete(0, END)
        # 循环插入在线用户
        for name in names:
            self.friend_list.insert(0, name)
        # 在第二行插入群聊
        self.friend_list.insert(0, "[Public chat]")
        # 设置群聊字体颜色
        self.friend_list.itemconfig(0, fg="#00BFFF")
        # 在第一行插入在线用户数
        self.friend_list.insert(0, "Online users: " + str(online_number))
        # 设置在线用户数字体颜色
        self.friend_list.itemconfig(0, fg="#FF00FF")

    # 在界面显示消息实例方法
    # 接收到消息时 在文本框中显示 自己的消息为蓝色 他人的消息为绿色
    def show_send_message(self, user_name, content, chat_flag):
        # 设置显示消息的文本框可编辑
        self.message_text.config(state=NORMAL)
        # 设置发送的消息的用户名和时间变量
        title = user_name + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n"

        # 加入聊天室标记处理
        if content == "* [SYSTEM MESSAGE] " + user_name + " joins the chat room":
            # 设置字体颜色样式及大小
            self.message_text.tag_config("tag_1", foreground="#FF00FF", font=tf.Font(family="Arial", size=13))
            # 在最后一行插入消息
            self.message_text.insert(END, content + "\n", "tag_1")
            # 重新声明显示消息的文本框不可编辑
            self.message_text.config(state=DISABLED)

        # 离开聊天室标记处理
        elif content == "* [SYSTEM MESSAGE] " + user_name + " has left the chat room":
            # 设置字体颜色样式及大小
            self.message_text.tag_config("tag_2", foreground="#DC143C", font=tf.Font(family="Arial", size=13))
            # 在最后一行插入消息
            self.message_text.insert(END, content + "\n", "tag_2")
            # 重新声明显示消息的文本框不可编辑
            self.message_text.config(state=DISABLED)

        # 发送消息的用户是自己
        elif user_name == self.user_name:
            # 如果标记是群聊标记 自己的消息用蓝色
            if chat_flag == "group_chat":
                self.message_text.tag_config("tag_4", foreground="#00BFFF", font=tf.Font(family="Arial", size=13))
                # 在最后一行插入消息
                self.message_text.insert(END, title, "tag_4")
                # 调用实例方法保存聊天记录
                self.sava_chatting_records(title)
            # 如果标记是私聊标记 消息用红色
            elif chat_flag == "private_chat":
                self.message_text.tag_config("tag_5", foreground="#DC143C", font=tf.Font(family="Arial", size=13))
                # 在最后一行插入消息
                self.message_text.insert(END, title, "tag_5")
                # 调用实例方法保存聊天记录
                self.sava_chatting_records(title)
            
        # 发送消息的用户不是自己
        else:
            # 如果标记是群聊标记 消息用绿色
            if chat_flag == "group_chat":
                self.message_text.tag_config("tag_6", foreground="#008000", font=tf.Font(family="Arial", size=13))
                # 在最后一行插入消息
                self.message_text.insert(END, title, "tag_6")
                # 调用实例方法保存聊天记录
                self.sava_chatting_records(title)
            # 如果标记是私聊标记 消息用红色
            elif chat_flag == "private_chat":
                self.message_text.tag_config("tag_7", foreground="#DC143C", font=tf.Font(family="Arial", size=13))
                # 在最后一行插入消息
                self.message_text.insert(END, title, "tag_7")
                # 调用实例方法保存聊天记录
                self.sava_chatting_records(title)
        
        # 内容为表情标记
        if content in self.dic:
            # 从数据库中读取用户头像
            chat_mysql.LogInformation.fing_face(user_name)
            # 为数据库读取用户头像以及保存到本地文件的时间留出缓冲
            time.sleep(0.5)
            # 打开图片 设置大小 并保存为png
            self.img1 = Image.open("profiles/user_profile.png")
            self.out1 = self.img1.resize((50, 50), Image.ANTIALIAS)
            self.out1.save(r"profiles/user_profile1.png", "png")
            # 为修改图片大小以及保存修改后的图片的时间留出缓冲
            time.sleep(0.5)
            # 把头像转化为PhotoImage 加入到列表中
            self.face.append(PhotoImage(file="profiles/user_profile1.png"))
            # 插入列表最后一个头像
            self.message_text.image_create(END, image=self.face[-1])
            self.message_text.insert(END, " : ")
            # 插入表情
            self.message_text.image_create(END, image=self.dic[content])
            self.message_text.insert(END, "\n\n")
            # 重新声明显示消息的文本框不可编辑
            self.message_text.config(state=DISABLED)
            # 滚动到最底部
            self.message_text.see(END)
            # 调用实例方法保存聊天记录
            self.sava_chatting_records("[Emoji]\n\n")
        
        # 内容为图片
        elif content[:5] == "pic**":
            # 从数据库中读取用户头像
            chat_mysql.LogInformation.fing_face(user_name)
            # 为数据库读取用户头像以及保存到本地文件的时间留出缓冲
            time.sleep(0.5)
            # 打开图片 设置大小 并保存为png
            self.img1 = Image.open("profiles/user_profile.png")
            self.out1 = self.img1.resize((50, 50), Image.ANTIALIAS)
            self.out1.save(r"profiles/user_profile3.png", "png")
            # 为修改图片大小以及保存修改后的图片的时间留出缓冲
            time.sleep(0.5)
            # 把头像转化为PhotoImage 加入到列表中
            self.face.append(PhotoImage(file="profiles/user_profile3.png"))
            # 插入列表最后一个头像
            self.message_text.image_create(END, image=self.face[-1])
            self.message_text.insert(END, " : ")
            # 打开图片 并存入字典
            prefx = str(random()) + "_"
            filename = content[5:-4] + "_save.png"
            img = PhotoImage(file=filename)
            self.pic[prefx + filename] = img
            # 插入图片
            self.message_text.image_create(END, image=self.pic[prefx + filename])
            self.message_text.insert(END, "\n\n")
            # 重新声明显示消息的文本框不可编辑
            self.message_text.config(state=DISABLED)
            # 滚动到最底部
            self.message_text.see(END)
            # 调用实例方法保存聊天记录
            self.sava_chatting_records("[Picture]\n\n")

        # 内容为消息
        elif content != "* [SYSTEM MESSAGE] " + user_name + " joins the chat room" \
            and content != "* [SYSTEM MESSAGE] " + user_name + " has left the chat room":
            # 从数据库中读取用户头像
            chat_mysql.LogInformation.fing_face(user_name)
            # 为数据库读取用户头像以及保存到本地文件的时间留出缓冲
            time.sleep(0.5)
            # 打开图片 设置大小 并保存为png
            self.img2 = Image.open("profiles/user_profile.png")
            self.out2 = self.img2.resize((50, 50), Image.ANTIALIAS)
            self.out2.save(r"profiles/user_profile2.png", "png")
            # 为修改图片大小以及保存修改后的图片的时间留出缓冲
            time.sleep(0.5)
            # 把头像转化为PhotoImage 加入到列表中
            self.face.append(PhotoImage(file="profiles/user_profile2.png"))
            # 插入列表最后一个头像
            self.message_text.image_create(END, image=self.face[-1])
            self.message_text.insert(END, " : ")
            # 插入消息
            self.message_text.tag_config("tag_8", foreground="#000000", font=tf.Font(family="Arial", size=15))
            self.message_text.insert(END, content, "tag_8")
            # 重新声明显示消息的文本框不可编辑
            self.message_text.config(state=DISABLED)
            # 滚动到最底部
            self.message_text.see(END)
            # 保存聊天记录
            self.sava_chatting_records(content)
            self.indexing_chatting_records(title, content)

    # 改变群聊/私聊标签实例方法
    def change_title(self, title):
        self.label1["text"] = title
    
    # 清空发送消息输入框实例方法
    def clear_send_text(self):
        self.send_text.delete("0.0", END)
    
    # 获取发送消息输入框内容实例方法
    def get_send_text(self):
        return self.send_text.get("0.0", END)

    # 清空显示查找聊天记录结果实例方法
    def clear_search_result(self):
        self.search_chatting_records.delete("0.0", END)

    # 获取查找聊天记录输入框内容实例方法
    def get_search_term(self):
        return self.search_text.get("0.0", END)