#2048 game
import random
import copy
import operator


class game2048:
    totalScore = 0
    # g_field = [[0 for i in range(4)] for i in range(4)]        # 用列表推导式初始化生成一个4*4的列表，列表元素全为 0
    # print(g_field)

    def __init__(self):
        initNumFlag = 0
        self.g_field = [[0 for i in range(4)] for i in range(4)]
        self.g_field_change = [[0 for i in range(4)] for i in range(4)]
        self.g_field_v = []
        while 1:
            k = 2 if random.randrange(0, 10) > 1 else 4  # 当生成随机数大于1的时候k=2否则k=4 生成2和4的概率为9：1
            s = divmod(random.randrange(0, 16), 4)  # 生成矩阵初始化的下标 比如divmod（15，4）的话，s为（3，3）正好可以作为矩阵下标
            if self.g_field[s[0]][s[1]] == 0:
                self.g_field[s[0]][s[1]] = k
                initNumFlag += 1
                if initNumFlag == 2:
                    break


    def display(self):
        print('{0:4} {1:4} {2:4} {3:4}'.format(self.g_field[0][0], self.g_field[0][1], self.g_field[0][2], self.g_field[0][3]))
        print('{0:4} {1:4} {2:4} {3:4}'.format(self.g_field[1][0], self.g_field[1][1], self.g_field[1][2], self.g_field[1][3]))
        print('{0:4} {1:4} {2:4} {3:4}'.format(self.g_field[2][0], self.g_field[2][1], self.g_field[2][2], self.g_field[2][3]))
        print('{0:4} {1:4} {2:4} {3:4}'.format(self.g_field[3][0], self.g_field[3][1], self.g_field[3][2], self.g_field[3][3]))
        print("游戏的分:{0:4}".format(self.totalScore))
        # print("游戏是否结束:{0:4}".format(self.isover))

    def is_over(self):
        n = 0
        for i in range(4):
            n += self.g_field[i].count(0)
        if n > 0:
            return False
        else:
            for row in range(4):
                for i in range(3):
                    if self.g_field[row][i] == self.g_field[row][i + 1] and self.g_field[row][i + 1] != 0:
                        return False
            for col in range(4):
                for j in range(3):
                    if self.g_field[j][col] == self.g_field[j + 1][col] and self.g_field[j + 1][col] != 0:
                        return False
            return True

    def judge(self):
        if self.is_over():
            print("游戏结束")
            return False
        else:
            if self.totalScore >= 2048:
                print("恭喜,获得满分")
            return True


    def addRandomNum(self):
        while 1:
            k = 2 if random.randrange(0, 10) > 1 else 4  # 当生成随机数大于1的时候k=2否则k=4 生成2和4的概率为9：1
            s = divmod(random.randrange(0, 16), 4)  # 生成矩阵初始化的下标 比如divmod（15，4）的话，s为（3，3）正好可以作为矩阵下标
            if self.g_field[s[0]][s[1]] == 0:
                self.g_field[s[0]][s[1]] = k
                break

        pass

    def g_field_handle(self, x, direction):
        for i in range(self.g_field[x].count(0)):
            self.g_field[x].remove(0)
        zeros = [0 for j in range(4 - len(self.g_field[x]))]
        if direction is 'left':
            self.g_field[x].extend(zeros)
        else:
            self.g_field[x][0:0] = zeros

    def g_field_handle_v(self, y, direction):
        self.g_field_v = [self.g_field[x][y] for x in range(4)]
        for i in range(self.g_field_v.count(0)):
            self.g_field_v.remove(0)
        zeros = [0 for j in range(4 - len(self.g_field_v))]
        if direction is 'up':
            self.g_field_v.extend(zeros)
        else:
            self.g_field_v[0:0] = zeros
        for k in range(4):
            self.g_field[k][y] = self.g_field_v[k]



    def moveAndMergeNum(self, direction):
        self.g_field_change = copy.deepcopy(self.g_field)
        if direction == "w":
            for y in range(4):
                self.g_field_handle_v(y, 'up')
                for k in range(3):
                    if self.g_field[k][y] == self.g_field[k + 1][y] and self.g_field[k + 1][y] != 0:
                        self.g_field[k][y] *= 2
                        self.g_field[k + 1][y] = 0
                        self.totalScore += self.g_field[k][y]
                self.g_field_handle_v(y, 'up')
                            # print(
                            #     '{0:4} {1:4} {2:4} {3:4}'.format(self.g_field[0][0], self.g_field[0][1],
                            #                                      self.g_field[0][2],
                            #                                      self.g_field[0][3]))
                            # print(
                            #     '{0:4} {1:4} {2:4} {3:4}'.format(self.g_field[1][0], self.g_field[1][1],
                            #                                      self.g_field[1][2],
                            #                                      self.g_field[1][3]))
                            # print(
                            #     '{0:4} {1:4} {2:4} {3:4}'.format(self.g_field[2][0], self.g_field[2][1],
                            #                                      self.g_field[2][2],
                            #                                      self.g_field[2][3]))
                            # print(
                            #     '{0:4} {1:4} {2:4} {3:4}'.format(self.g_field[3][0], self.g_field[3][1],
                            #                                      self.g_field[3][2],
                            #                                      self.g_field[3][3]))
                            # print("\n")

        if direction == "a":
            for x in range(4):
                self.g_field_handle(x, 'left')
                for k in range(3):
                    if self.g_field[x][k] == self.g_field[x][k + 1] and self.g_field[x][k + 1] != 0:
                        self.g_field[x][k] *= 2
                        self.g_field[x][k + 1] = 0
                        self.totalScore += self.g_field[x][k]
                self.g_field_handle(x, 'left')

        if direction == "s":
            for y in range(4):
                self.g_field_handle_v(y, 'down')
                for k in range(3, 0, -1):
                    if self.g_field[k][y] == self.g_field[k - 1][y] and self.g_field[k - 1][y] != 0:
                        self.g_field[k][y] *= 2
                        self.g_field[k - 1][y] = 0
                        self.totalScore += self.g_field[k][y]
                self.g_field_handle_v(y, 'down')

        if direction == "d":
            for x in range(4):
                self.g_field_handle(x, 'right')
                for k in range(3, 0, -1):
                    if self.g_field[x][k] == self.g_field[x][k - 1] and self.g_field[x][k - 1] != 0:
                        self.g_field[x][k] *= 2
                        self.g_field[x][k - 1] = 0
                        self.totalScore += self.g_field[x][k]
                self.g_field_handle(x, 'right')

        else:
            pass



    def readOperate(self):
        direction = input('\033[33;1m (↑:w) (↓:s) (←:a) (→:d),q(uit) :\033[0m')    #不断处理用户输入
        self.moveAndMergeNum(direction)







mygame = game2048()
while 1:
    mygame.display()
    mygame.readOperate()
    if mygame.judge():
        if operator.eq(mygame.g_field, mygame.g_field_change):
            pass
        else:
            mygame.addRandomNum()
    else:
        exit()










