from tkinter import *
import random

UNIT_SIZE = 20

global row, col
global direction
global fps
global have_food
global food_coord
global score
global snake_list
global game_map

row = 20
col = 20

height = row * UNIT_SIZE
width = col * UNIT_SIZE

# 方向变量direction取值为-1, 1, -2, 2
# 分别对应Up, Down, Left, Right
direction = 2
fps = 150

have_food = 0
food_coord = [0, 0]

score = 0

snake_list = [[11, 10], [10, 10], [9, 10]]
game_map = []

def draw_unit(canvas, col, row, unit_color="green"):
    # 绘制以左上角为参照的(col, row)的方块
    x1 = col * UNIT_SIZE
    y1 = row * UNIT_SIZE
    x2 = (col + 1) * UNIT_SIZE
    y2 = (row + 1) * UNIT_SIZE
    # 绘制从(x0, y0)到(x1, y1)对角线构成的矩形
    canvas.create_rectangle(x1, y1, x2, y2, fill=unit_color, outline="white")

def put_background(canvas, color="silver"):
    # 画布上构建像素网格
    for x in range(col) :
        for y in range(row) :
            draw_unit(canvas, x, y, unit_color=color)
            game_map.append([x, y])

def draw_the_snake(canvas, snake_list, color="green"):
    for i in snake_list :
        draw_unit(canvas, i[0], i[1], unit_color=color)

def snake_move(snake_list, dir):

    global row, col
    global have_food
    global food_coord
    global score

    new_coord = [0, 0]

    if dir % 2 == 1:
        new_coord[0] = snake_list[0][0]
        new_coord[1] = snake_list[0][1] + dir
    else:
        new_coord[0] = snake_list[0][0] + int(dir / 2)
        new_coord[1] = snake_list[0][1]
    
    snake_list.insert(0, new_coord)

    # 取模处理 形成穿越边界的效果
    for coord in snake_list:
        if coord[0] not in range(col):
            coord[0] %= col
            break
        elif coord[1] not in range(row):
            coord[1] %= row
            break
    
    if snake_list[0] == food_coord:
        draw_unit(canvas, snake_list[0][0], snake_list[0][1],)
        have_food = 0
        score += 10
        str_score.set("Your Score: " + str(score))
    else:
        draw_unit(canvas, snake_list[-1][0], snake_list[-1][1], unit_color="silver")
        draw_unit(canvas, snake_list[0][0], snake_list[0][1],)
        snake_list.pop()

    return snake_list

# 蛇头不可以朝原有的蛇的方向前进
# event为绑定的键盘鼠标事件
def callback(event) :
    
    global direction

    ch = event.keysym
    if ch == "Up":
        if snake_list[0][0] != snake_list[1][0]:
            direction = -1
    elif ch == "Down":
        if snake_list[0][0] != snake_list[1][0]:
            direction = 1
    elif ch == "Left":
        if snake_list[0][1] != snake_list[1][1]:
            direction = -2
    elif ch == "Right":
        if snake_list[0][1] != snake_list[1][1]:
            direction = 2
    return

# 判断当前状态下蛇是否撞上自己
# 返回0 - 没有死亡 1 - 死亡
def snake_death_judge(snake_list):
    set_list = snake_list[1:]
    return int(snake_list[0] in set_list)

def food(canvas, snake_list):

    global row, col
    global have_food
    global food_coord
    global game_map

    if have_food:
        return

    food_coord[0] = random.choice(range(col))
    food_coord[1] = random.choice(range(row))
    while food_coord in snake_list :
        food_coord[0] = random.choice(range(col))
        food_coord[1] = random.choice(range(row))
    draw_unit(canvas, food_coord[0], food_coord[1], unit_color="red")
    have_food = 1

def game_loop():

    global fps
    global snake_list

    win.update()
    food(canvas, snake_list)
    snake_list = snake_move(snake_list, direction)
    flag = snake_death_judge(snake_list)

    if flag:
        over_lavel = Label(win, text="Game Over", font=("Arial", 25), width=15, height=1)
        over_lavel.place(x=40, y=height / 2, bg=None)
        return

    fps = max(int(197 / len(snake_list) ** 0.25), 75)
    win.after(fps, game_loop)


win = Tk()
win.title("Snake")

canvas = Canvas(win, width=width, height=height + 2 * UNIT_SIZE)
canvas.pack()

str_score = StringVar()
score_label = Label(win, textvariable=str_score, font=("Arial", 16), width=15, height=1)
str_score.set("Your Score: " + str(score))
score_label.place(x=100, y=height)
put_background(canvas)
draw_the_snake(canvas, snake_list)

# 绑定键盘鼠标事件关系
canvas.focus_set()
canvas.bind("<KeyPress-Left>", callback)
canvas.bind("<KeyPress-Right>", callback)
canvas.bind("<KeyPress-Up>", callback)
canvas.bind("<KeyPress-Down>", callback)

game_loop()
win.mainloop()