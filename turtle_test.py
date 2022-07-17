from turtle import *
from time import sleep
color('red', 'yellow')
colors = ['green', 'red', 'yellow', 'blue']
movedx = False
movedz = False
y = 10
z = 5
x = 5
data = [[[2, 0, 0, 0, 2], [0, 2, 0, 2, 0], [0, 0, 2, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 2, 2, 2], [0, 0, 2, 2, 2], [0, 0, 2, 2, 2], [0, 0, 2, 2, 2], [0, 0, 2, 2, 2]], [[2, 2, 2, 0, 0], [2, 2, 2, 0, 0], [2, 2, 2, 0, 0], [2, 2, 2, 0, 0], [2, 2, 2, 0, 0]], [[2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2]], [[0, 0, 0, 0, 0], [2, 2, 2, 2, 2], [0, 0, 0, 0, 0], [2, 2, 2, 2, 2], [0, 0, 0, 0, 0]], [[0, 2, 0, 2, 0], [0, 2, 0, 2, 0], [0, 2, 0, 2, 0], [0, 2, 0, 2, 0], [0, 2, 0, 2, 0]], [[0, 0, 0, 0, 0], [0, 2, 2, 2, 0], [0, 2, 2, 2, 0], [0, 2, 2, 2, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 2, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]]
slow = True
turns = 0


def turn(x):
    global turns
    if abs(x-turns) > 2:
        if x-turns > 0:
            left(90)
            turns -= 1
        else:
            right(90)
            turns += 1
        turns %= 4
        return
    while x-turns > 0:
        right(90)
        turns += 1
    while x-turns < 0:
        left(90)
        turns -= 1
    turns %= 4


def first_in_line(d):
    for j in range(z):
        if d[j]:
            return j


def last_in_line(d):
    for j in range(z):
        j = z - j - 1
        if d[j]:
            return j


left(90)
for k in range(y):
    if any([any(data[k][i]) for i in range(x)]):
        for i in range(x):
            if movedx:
                i, lasti = x - i - 1, 0
            else:
                lasti = x-1
            if any(data[k][i]):
                for j in range(z):
                    if movedz:
                        j, nextj, lastj = z - j - 1, z - j - 2, 0
                        turn(2)
                    else:
                        nextj, lastj = j+1, z-1
                        turn(0)
                    if data[k][i][j]:
                        dot(20, colors[k % len(colors)])
                    if j != lastj:
                        forward(20)
                movedz = not movedz
            if i != lasti:
                if movedx:
                    turn(3)
                else:
                    turn(1)
                forward(20)
        movedx = not movedx
done()