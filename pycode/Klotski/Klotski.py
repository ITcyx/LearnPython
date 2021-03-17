import random
import os
import platform
from math import *


def get_zero(blocks):
    # 获取列表值为零的索引

    for i in range(len(blocks)):
        if blocks[i] == 0:
            return i


def zero_move(orientation, blocks):
    # 移动列表值为零的索引

    z = get_zero(blocks)
    n = int(sqrt(len(blocks)))  # 开平方列表长度
    x = int(z / n)  # 计算列表值为零的索引的x坐标
    y = z % n  # 计算列表值为零的索引的y坐标
    if orientation == 'a':  # 向左的操作
        if y != n-1:
            blocks[x * n + y], blocks[x * n + y + 1] = blocks[x * n + y + 1], 0
    elif orientation == 'd':  # 向右的操作
        if y != 0:
            blocks[x * n + y], blocks[x * n + y - 1] = blocks[x * n + y - 1], 0
    elif orientation == 'w':  # 向上的操作
        if x != n-1:
            blocks[x * n + y], blocks[(x + 1) * n + y] = blocks[(x + 1) * n + y], 0
    elif orientation == 's':  # 向下的操作
        if x != 0:
            blocks[x * n + y], blocks[(x - 1) * n + y] = blocks[(x - 1) * n + y], 0


def print_int(t):
    # 打印整数

    if t == 0:  # 当打印值为零时，打印4个空格
        print("", end = "     ")
    elif t < 10:  # 当打印值大于零小于十时，前面先打印一个空格，再打印打印值，最后打印3个空格
        print(' ' + str(t), end = "   ")
    else:  # 当打印值大于九时，直接打印打印值，再打印3个空格
        print(t, end = "   ")


def screen_print(blocks):
    # 向屏幕打印列表

    sys = platform.system()  # 获取操作系统的名称
    if sys == "Windows":  # Windows系统的清屏命令
        os.system("cls")
    else:  # Linux或者MacOS系统的清屏命令
        os.system("clear")
    n = int(sqrt(len(blocks)))
    for i in range(n):
        for j in range(n):
            print_int(blocks[i*n+j])
        print("")


def is_win(blocks):
    # 判断是否胜利

    for i in range(len(blocks)-1):
        if blocks[i] != i+1:
            return False
    return True


def get_inversion(blocks):
    # 计算逆序数

    inv = 0
    for i in range(1, len(blocks)):
        for j in range(i):
            if blocks[j] > blocks[i]:
                inv += 1
    return inv


def is_soluble(blocks):
    # 判断是否可解

    n = int(sqrt(len(blocks)))  # 开平方列表长度
    if n % 2 == 1:
        f = False
    else:
        f = True
    z = get_zero(blocks)
    if (len(blocks) - 1 - z) % 2 == 1:
        f = not f
    return f == (get_inversion(blocks) % 2 == 1)


if __name__ == "__main__":
    # 主函数

    while True:  # 检测用户输入的值是否大于等于3小于等于10
        while True:
            n = int(input("please enetr a number which is Between three and ten:"))
            if n >= 3 and n <= 10:
                break
            else:
                print("Illegal input!!!")
        blocks = list(range(n ** 2))
        while True:  # 防止随机生成的列表正好胜利或者无解的情况
            for i in range(len(blocks)):
                r = random.randint(0, len(blocks) - i - 1)
                blocks[i], blocks[i+r] = blocks[i+r], blocks[i]
            if (not is_win(blocks)) and is_soluble(blocks):
                break
        while True:  # 监测用户输入并实时进行输出
            screen_print(blocks)
            if is_win(blocks):
                print("You win!")
                break
            c = input("please input 'w,a,s,d' to control:")
            zero_move(c,blocks)