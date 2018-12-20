# -*- coding: utf-8 -*-
# @Time    : 2018/12/20 16:55
# @Author  : 长毛金眼大黑猫
# @FileName: GAME_2048.py
# @Software: PyCharm
# @Blog    ：https://github.com/maaruilin

from tkinter import *
from tkinter import messagebox
import random
import copy
import operator

KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"

SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
                         32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
                         512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"}
CELL_COLOR_DICT = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2",
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2",
                   512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2"}
FONT = ("Verdana", 40, "bold")
LABEL_COLOR_BG = "#92877d"
LABEL_COLOR_FG = "#ffffff"
BUTTON_COLOR_FG = "#ffffff"
BUTTON_COLOR_BG = "#f59563"
totalScore = 0


class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.grid()
        self.master.title('GAME 2048')
        self.master.bind("<Key>", self.key_press)
        self.commands = {KEY_UP: up, KEY_DOWN: down, KEY_LEFT: left, KEY_RIGHT: right}
        self.grid_cells = []
        self.total_score_var = StringVar()
        self.init_grid()
        self.g_field = []
        self.init_matrix()
        self.update_grid_cells()

    def init_grid(self):
        background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)#背景
        background.grid()

        for i in range(GRID_LEN):#产生4*4方格
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE/GRID_LEN, height=SIZE/GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                num = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY,
                            justify=CENTER, font=FONT, width=4, height=2)
                num.grid()
                grid_row.append(num)
            self.grid_cells.append(grid_row)

        label_instruction = Label(background, text="(↑:w)(↓:s)\n(←:a)(→:d)",
                                  bg=LABEL_COLOR_BG, fg=LABEL_COLOR_FG, font=('Verdana', 12, "bold"), width=15, height=2)
        label_instruction.grid(row=4, column=0)  #操作说明标签

        label_total_score = Label(background, textvariable=self.total_score_var,
                                  bg=LABEL_COLOR_BG, fg=LABEL_COLOR_FG, font=('Verdana', 12, "bold"), width=15, height=2)
        label_total_score.grid(row=4, column=1)  #游戏得分标签

        button_restart = Button(background, text="重新开始", bg=BUTTON_COLOR_BG, fg=BUTTON_COLOR_FG,
                                font=('Verdana', 12, "bold"), width=13, height=2, command=self.restart_game)
        button_restart.grid(row=4, column=2)#重新开始按钮

        button_exit = Button(background, text="退出", bg=BUTTON_COLOR_BG, fg=BUTTON_COLOR_FG, font=('Verdana', 12, "bold"),
                             width=13, height=2, command=self.end_game)
        button_exit.grid(row=4, column=3)#退出按钮

    def init_matrix(self):
        initNumFlag = 0
        self.g_field = [[0 for i in range(4)] for i in range(4)]

        while 1:
            k = 2 if random.randrange(0, 10) > 1 else 4  # 当生成随机数大于1的时候k=2否则k=4 生成2和4的概率为9：1
            s = divmod(random.randrange(0, 16), 4)  # 生成矩阵初始化的下标 比如divmod（15，4）的话，s为（3，3）正好可以作为矩阵下标
            if self.g_field[s[0]][s[1]] == 0:
                self.g_field[s[0]][s[1]] = k
                initNumFlag += 1
                if initNumFlag == 2:
                    break

    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.g_field[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number],
                                                    fg=CELL_COLOR_DICT[new_number])
        self.total_score_var.set("游戏得分:"+str(totalScore))
        self.update_idletasks()

    def key_press(self, event):
        key = repr(event.char)
        if key in self.commands:
            self.g_field, done = self.commands[repr(event.char)](self.g_field)
            if done:
                add_random_num(self.g_field)
                self.update_grid_cells()
                if judge(self.g_field):
                    textbox = messagebox.askyesnocancel(title='2048', message='是否再来一局')  # 弹窗 return True/False
                    if textbox is True:
                        self.restart_game()
                    elif textbox is None:
                        pass
                    else:
                        self.end_game()

    def restart_game(self):
        global totalScore
        totalScore = 0
        self.init_matrix()
        self.update_grid_cells()

    # @staticmethod
    def end_game(self):
        exit()


def add_random_num(mat):
    while 1:
        k = 2 if random.randrange(0, 10) > 1 else 4  # 当生成随机数大于1的时候k=2否则k=4 生成2和4的概率为9：1
        s = divmod(random.randrange(0, 16), 4)  # 生成矩阵初始化的下标 比如divmod（15，4）的话，s为（3，3）正好可以作为矩阵下标
        if mat[s[0]][s[1]] == 0:
            mat[s[0]][s[1]] = k
            break


def g_field_handle(mat, x, direction):
    for i in range(mat[x].count(0)):
        mat[x].remove(0)
    zeros = [0 for j in range(4 - len(mat[x]))]
    if direction is 'left':
        mat[x].extend(zeros)
    else:
        mat[x][0:0] = zeros


def g_field_handle_v(mat, y, direction):
    g_field_v = [mat[x][y] for x in range(4)]
    for i in range(g_field_v.count(0)):
        g_field_v.remove(0)
    zeros = [0 for j in range(4 - len(g_field_v))]
    if direction is 'up':
        g_field_v.extend(zeros)
    else:
        g_field_v[0:0] = zeros
    for k in range(4):
        mat[k][y] = g_field_v[k]


def is_over(mat):
    n = 0
    for i in range(4):
        n += mat[i].count(0)
    if n > 0:
        return False
    else:
        for row in range(4):
            for i in range(3):
                if mat[row][i] == mat[row][i + 1] and mat[row][i + 1] != 0:
                    return False
        for col in range(4):
            for j in range(3):
                if mat[j][col] == mat[j + 1][col] and mat[j + 1][col] != 0:
                    return False
        return True


def judge(mat):
    if is_over(mat):
        return True
    else:
        return False


def up(mat):
    global totalScore
    g_field_change = copy.deepcopy(mat)
    for y in range(4):
        g_field_handle_v(mat, y, 'up')
        for k in range(3):
            if mat[k][y] == mat[k + 1][y] and mat[k + 1][y] != 0:
                mat[k][y] *= 2
                mat[k + 1][y] = 0
                totalScore += mat[k][y]
        g_field_handle_v(mat, y, 'up')

    if operator.eq(mat, g_field_change):
        done = False
    else:
        done = True
    return mat, done


def down(mat):
    global totalScore
    g_field_change = copy.deepcopy(mat)
    for y in range(4):
        g_field_handle_v(mat, y, 'down')
        for k in range(3, 0, -1):
            if mat[k][y] == mat[k - 1][y] and mat[k - 1][y] != 0:
                mat[k][y] *= 2
                mat[k - 1][y] = 0
                totalScore += mat[k][y]
        g_field_handle_v(mat, y, 'down')

    if operator.eq(mat, g_field_change):
        done = False
    else:
        done = True
    return mat, done


def left(mat):
    global totalScore
    g_field_change = copy.deepcopy(mat)
    for x in range(4):
        g_field_handle(mat, x, 'left')
        for k in range(3):
            if mat[x][k] == mat[x][k + 1] and mat[x][k + 1] != 0:
                mat[x][k] *= 2
                mat[x][k + 1] = 0
                totalScore += mat[x][k]
        g_field_handle(mat, x, 'left')

    if operator.eq(mat, g_field_change):
        done = False
    else:
        done = True
    return mat, done


def right(mat):
    global totalScore
    g_field_change = copy.deepcopy(mat)
    for x in range(4):
        g_field_handle(mat, x, 'right')
        for k in range(3, 0, -1):
            if mat[x][k] == mat[x][k - 1] and mat[x][k - 1] != 0:
                mat[x][k] *= 2
                mat[x][k - 1] = 0
                totalScore += mat[x][k]
        g_field_handle(mat, x, 'right')

    if operator.eq(mat, g_field_change):
        done = False
    else:
        done = True
    return mat, done


game_grid = GameGrid()
game_grid.mainloop()
