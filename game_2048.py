from tkinter import *
from tkinter import messagebox
import colors_2048 as c
import random
import numpy

# 2048游戏类
class Game_2048(Frame):

    # 构造方法
    def __init__(self):
        # 继承tkinter中Frame类
        Frame.__init__(self)
        # 设置窗口位置 标题
        self.grid()
        self.master.title("2048")

        # 创建主网格
        self.main_grid = Frame(self, bg=c.GRID_COLOR, bd=3, width=300, height=300)
        self.main_grid.grid(pady=(100, 0))

        # 调用显示游戏界面实例方法
        self.make_GUI()
        # 调用初始化游戏实例方法
        self.start_game()

        # 移动判断标签 初始化为False
        self.moved = False
        # 判断胜利标签 初始化为False
        self.win = False
        # 到达2048后是否继续游戏判断标签 初始化为False
        self.keep_playing = False
        # 关闭所有移动键功能判断标签 初始化为False
        self.shut_down = False

        # 将移动键与移动操作绑定
        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)
        
        # 调用mainloop执行循环显示界面
        self.mainloop()
    
    # 显示游戏界面实例方法
    def make_GUI(self):
        # 创建存放所有格子信息的矩阵
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                # 创建网格中的格子
                cell_frame = Frame(self.main_grid, bg=c.EMPTY_CELL_COLOR, width=75, height=75)
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                # 将格子初始化为空格子
                cell_number = Label(self.main_grid, bg=c.EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                # 创建存储每个格子信息的字典
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)
        
        # 创建计分器
        score_frame = Frame(self)
        score_frame.place(relx=0.5, y=45, anchor="center")

        # 创建计分器标题
        score_title = Label(score_frame, text="Score", font=c.SCORE_LABEL_FONT)
        score_title.grid(row=0)

        # 创建分数显示器
        self.score_label = Label(score_frame, text="0", font=c.SCORE_FONT)
        self.score_label.grid(row=1)

    # 初始化游戏实例方法
    def start_game(self):
        # 创建零矩阵
        self.matrix = [[0] * 4 for _ in range(4)]

        # 用2填充某一初始格子
        # 随机选自一个格子
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        # 用2填充 并调整该格子信息为2对应信息
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(bg=c.CELL_COLORS[2], \
            fg=c.CELL_NUMBER_COLORS[2], font=c.CELL_NUMBER_FONTS[2], text="2")

        # 用2填充另一初始格子
        # 随机选择一个空格子
        while self.matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        # 用2填充 并调整该格子信息为2对应信息
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(bg=c.CELL_COLORS[2], \
            fg=c.CELL_NUMBER_COLORS[2], font=c.CELL_NUMBER_FONTS[2], text="2")

        # 初始化分数为0
        self.score = 0

    # 矩阵stack变换实例方法
    def stack(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    # 如果stack变换产生了移动 则记录发生了移动
                    if fill_position != j:
                        self.moved = True
                    fill_position += 1
        self.matrix = new_matrix
    
    # 矩阵combine变换实例方法
    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]
                    # 记录combine变换产生的移动
                    self.moved = True
    
    # 矩阵reverse变换实例方法
    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3 - j])
        self.matrix = new_matrix
    
    # 矩阵transpose变换实例方法
    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix
    
    # 在任意一个空格子中放入2或4实例方法
    def add_new_tile(self):
        # 判断是否还能加入新数字
        if any(0 in row for row in self.matrix):
            # 随机选择一个空格子
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            while self.matrix[row][col] != 0:
                row = random.randint(0, 3)
                col = random.randint(0, 3)
            # 用2或4随机填充该格子
            # 2出现概率为90% 4出现概率为10%
            self.matrix[row][col] = numpy.random.choice([2, 4], p=[0.9, 0.1])
    
    # 根据移动后的新矩阵更新GUI实例方法
    def update_GUI(self):
        # 嵌套循环更新每一个格子的信息
        for i in range(4):
            for j in range(4):
                # 取得每一个格子对应的填充值
                cell_value = self.matrix[i][j]

                # 如果是空格子 调整为空格子对应信息
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg=c.EMPTY_CELL_COLOR, text="")

                # 调整为相应数字格子对应信息
                else:
                    self.cells[i][j]["frame"].configure(bg=c.CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(bg=c.CELL_COLORS[cell_value], \
                        fg=c.CELL_NUMBER_COLORS[cell_value], font=c.CELL_NUMBER_FONTS[cell_value], text=str(cell_value))
                
                # 更新分数
                self.score_label.configure(text=self.score)
                # 强制更新显示界面
                self.update_idletasks()
    
    # 左键移动实例方法
    def left(self, event):
        # 当移动键功能未关闭时
        if not self.shut_down:
            self.stack()
            self.combine()
            self.stack()

            # 如果发生了移动
            if self.moved:
                # 填充新格子
                self.add_new_tile()
                # 更新显示界面
                self.update_GUI()
                # 重置移动判断标签为False
                self.moved = False
            # 判断游戏是否结束
            self.game_over()
    
    # 右键移动实例方法
    def right(self, event):
        # 当移动键功能未关闭时
        if not self.shut_down:
            self.reverse()
            self.stack()
            self.combine()
            self.stack()
            self.reverse()
        
            # 如果发生了移动
            if self.moved:
                # 填充新格子
                self.add_new_tile()
                # 更新显示界面
                self.update_GUI()
                # 重置移动判断标签为False
                self.moved = False
            # 判断游戏是否结束
            self.game_over()

    # 上键移动实例方法
    def up(self, event):
        # 当移动键功能未关闭时
        if not self.shut_down:
            self.transpose()
            self.stack()
            self.combine()
            self.stack()
            self.transpose()
        
            # 如果发生了移动
            if self.moved:
                # 填充新格子
                self.add_new_tile()
                # 更新显示界面
                self.update_GUI()
                # 重置移动判断标签为False
                self.moved = False
            # 判断游戏是否结束
            self.game_over()
    
    # 下键移动实例方法
    def down(self, event):
        # 当移动键功能未关闭时
        if not self.shut_down:
            self.transpose()
            self.reverse()
            self.stack()
            self.combine()
            self.stack()
            self.reverse()
            self.transpose()
        
            # 如果发生了移动
            if self.moved:
                # 填充新格子
                self.add_new_tile()
                # 更新显示界面
                self.update_GUI()
                # 重置移动判断标签为False
                self.moved = False
            # 判断游戏是否结束
            self.game_over()

    # 检查是否还有可行的水平移动实例方法
    def horizontal_move_exists(self):
        for i in range(4):
            for j in range(3):
                # 如果横向相邻两格可以合并 则返回True
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        # 否则返回False
        return False
    
    # 检查是否还有可行的竖直移动实例方法
    def vertical_move_exists(self):
        for i in range(3):
            for j in range(4):
                # 如果纵向两格可以合并 则返回True
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        # 否则返回False
        return False

    # 检查游戏是否结束实例方法
    def game_over(self):
        # 如果出现2048数字
        # 只有未达到2048 不继续游戏 且未胜利的情况下 才判断是否胜利
        if any(2048 in row for row in self.matrix) and not self.keep_playing and not self.win:
            # 创建游戏结束界面
            game_over_frame = Frame(self.main_grid, borderwidth=0)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")

            # 创建游戏胜利标签
            win_label = Label(game_over_frame, text=" You win! ", bg=c.WINNER_BG, fg=c.GAME_OVER_FONT_COLOR, font=c.GAME_OVER_FONT)
            win_label.pack()

            # 如果选择继续游戏
            if messagebox.askyesno("2048", "Continue the game?"):
                # 设置继续游戏标签为True
                self.keep_playing = True
                # 销毁游戏胜利界面
                win_label.destroy()
                game_over_frame.destroy()
                
            # 如果选择不继续游戏
            else:
                # 关闭移动键功能
                self.shut_down = True
            
            # 设置为获得胜利
            self.win = True
        
        # 如果格子已全部填充且无法进行横向或纵向移动
        elif not any(0 in row for row in self.matrix) and not self.horizontal_move_exists() and not self.vertical_move_exists():
            # 创建游戏结束界面
            game_over_frame = Frame(self.main_grid, borderwidth=0)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")

            # 创建游戏失败标签
            lose_label = Label(game_over_frame, text="Game over!", bg=c.LOSER_BG, fg=c.GAME_OVER_FONT_COLOR, font=c.GAME_OVER_FONT)
            lose_label.pack()
            # 关闭移动键功能
            self.shut_down = True

# 定义主函数
def main():
    # 启动2048游戏
    Game_2048()

if __name__ == "__main__":
    main()