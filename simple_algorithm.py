import numpy as np
import collections
import time
import random as rd

lookTab = {"r": 0, "s": 1, "p": 2}
[r, s, p] = ["r", "s", "p"]
actions = [r, s, p]
upbound = 10000
[p11, p12, p13] = [0.001, 0.004, 0.995]  # w-, w+, w0
[p21, p22, p23] = [0.063, 0.791, 0.146]  # t-, t+, t0
[p31, p32, p33] = [0.989, 0.001, 0.01] # l-, l+, l0
(win, tie, lose) = (1, 0, -1)

def getRes(action1, action2):
    if action1 == action2:
        return (tie, tie)
    elif (action1 == r and action2 == s)or\
         (action1 == s and action2 == p)or\
         (action1 == p and action2 == r):
        return win, lose
    else:
        return lose, win

class Player:
    def __init__(self):
        self.state = tie
        self.action = s

    def generateAction(self, p1, p2, p3):
        n = rd.random()
        if n < p1:
            return actions[0]
        elif n < p1 + p2:
            return actions[1]
        else:
            return actions[2]

    def getAction(self):
        idx = lookTab[self.action]
        pr = [1, 0, 0]
        if self.state == win:
            pr[idx] = p13
            pr[(idx + 1) % 3] = p11
            pr[(idx - 1) % 3] = p12
        elif self.state == tie:
            pr[idx] = p23
            pr[(idx + 1) % 3] = p21
            pr[(idx - 1) % 3] = p22
        else:
            pr[idx] = p33
            pr[(idx + 1) % 3] = p31
            pr[(idx - 1) % 3] = p32
        return self.generateAction(pr[0], pr[1], pr[2])

    def setAction(self, new_action):
        self.action = new_action

class AI:
    def __init__(self):
        self.state = tie
        self.action = s

    def generateAction(self, op_p1, op_p2, op_p3):
        op_action_idx = np.argmax([op_p1, op_p2, op_p3])
        return actions[(op_action_idx - 1) % 3]

    def getAction(self):
        op_pr = [1, 0, 0]
        idx = lookTab[self.action]
        if self.state == lose: # the opposite player won
            op_idx = (idx - 1) % 3
            op_pr[op_idx] = p13
            op_pr[(op_idx + 1) % 3] = p11
            op_pr[(op_idx - 1) % 3] = p12
        elif self.state == tie:
            op_idx = idx
            op_pr[op_idx] = p23
            op_pr[(op_idx + 1) % 3] = p21
            op_pr[(op_idx - 1) % 3] = p22
        else: # the opposite player lost
            op_idx = (idx + 1) % 3
            op_pr[op_idx] = p33
            op_pr[(op_idx + 1) % 3] = p31
            op_pr[(op_idx - 1) % 3] = p32
        return self.generateAction(op_pr[0], op_pr[1], op_pr[2])
    def setAction(self, new_action):
        self.action = new_action

p1 = Player()
p2 = AI()

cnt_win = 0
cnt_lose = 0
cnt_tie = 0
for i in range(upbound):
    action1 = p1.getAction()
    action2 = p2.getAction()
    p1.setAction(action1)
    p2.setAction(action2)
    (p1.state, p2.state) = getRes(action1, action2)
    # print(action1, action2, p2.state)
    if (p2.state == win):
        cnt_win = cnt_win + 1
    elif (p2.state == lose):
        cnt_lose = cnt_lose + 1
    else:
        cnt_tie = cnt_tie + 1

print('win: ', cnt_win/upbound, ' tie: ', cnt_tie/upbound, ' lose: ', cnt_lose/upbound)   
