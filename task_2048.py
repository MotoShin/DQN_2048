'''
https://qiita.com/masa_ramen/items/ac31db0d20ad88cff09a のコードそのまま
'''
# ライブラリのインポート
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import shutil
import numpy as np
import pprint
import time
import copy
from numpy.random import *
import math

# デバッグ
import logging
# logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
# logging.debug('Start of program')
# logging.disable(logging.CRITICAL)# debugしない

'''
上 : u 0
下 : d 2
左 : l 3
右 : r 1
'''

class Task_2048():

    def __init__(self):
        self.max_num = 0
        self.board = {}
        self.score = 0
        self.cnt = 0
        self.end_flag = False
        self.dirs = ['u', 'r', 'd', 'l']

    def print_board(self):
        # 盤を見やすく表示
        board = self.board
        print('  ' + '____'*4)
        print(' | ' + board['1-1'] + ' | ' + board['2-1'] + ' | ' + board['3-1'] + ' | ' + board['4-1'] + ' | ')
        print(' | ' + board['1-2'] + ' | ' + board['2-2'] + ' | ' + board['3-2'] + ' | ' + board['4-2'] + ' | ')
        print(' | ' + board['1-3'] + ' | ' + board['2-3'] + ' | ' + board['3-3'] + ' | ' + board['4-3'] + ' | ')
        print(' | ' + board['1-4'] + ' | ' + board['2-4'] + ' | ' + board['3-4'] + ' | ' + board['4-4'] + ' | ')
        print('  ' + '____'*4)

    def move_tile(self, next_board, a, b):
        next_board[b] = next_board[a]
        next_board[a] = '0'
        return next_board# タイルの移動

    def sum_tile(self, next_board, c, d, end):
        c_num = int(next_board[c])
        d_num = int(next_board[d])
        next_board[c] = '0'
        next_board[d] = str(c_num + d_num)
        if end==0:
            print('{0}+{1}={2}'.format(c_num,d_num,c_num+d_num))
            self.score += c_num + d_num
        return next_board# タイルの結合

    def down_move(self, next_board, end):
        # 下方向移動
        if next_board['1-4']=='0':# ok
            if next_board['1-3']=='0':# ok
                if next_board['1-2']=='0':# ok
                    if next_board['1-1']=='0':
                        #[0,0,0,0]->何もしない
                        logging.debug('hoge')
                    elif next_board['1-1']!='0':
                        #[2,0,0,0]->[0,0,0,2]
                        next_board = self.move_tile(next_board,'1-1','1-4')
                elif next_board['1-2']!='0':# ok
                    if next_board['1-1']=='0':
                        #[0,2,0,0]->[0,0,0,2]
                        next_board = self.move_tile(next_board,'1-2','1-4')
                    elif next_board['1-1']!='0':
                        if next_board['1-1']==next_board['1-2']:
                            #[2,2,0,0]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'1-1','1-2',end)
                            next_board = self.move_tile(next_board,'1-2','1-4')
                        elif next_board['1-1']!=next_board['1-2']:
                            #[2,4,0,0]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'1-2','1-4')
                            next_board = self.move_tile(next_board,'1-1','1-3')
            elif next_board['1-3']!='0':# ok
                if next_board['1-2']=='0':# ok
                    if next_board['1-1']=='0':# ok
                        #[0,0,2,0]->[0,0,0,2]
                        next_board = self.move_tile(next_board,'1-3','1-4')
                    elif next_board['1-1']!='0':# ok
                        if next_board['1-1']==next_board['1-3']:# ok
                            #[2,0,2,0]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'1-1','1-3',end)
                            next_board = self.move_tile(next_board,'1-3','1-4')
                        elif next_board['1-1']!=next_board['1-3']:# ok
                            #[2,0,4,0]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'1-3','1-4')
                            next_board = self.move_tile(next_board,'1-1','1-3')
                elif next_board['1-2']!='0':# ok
                    if next_board['1-1']=='0':# ok
                        if next_board['1-2']==next_board['1-3']:# ok
                            #[0,2,2,0]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'1-2','1-3',end)
                            next_board = self.move_tile(next_board,'1-3','1-4')
                        elif next_board['1-2']!=next_board['1-3']:# ok
                            #[0,2,4,0]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'1-3','1-4')
                            next_board = self.move_tile(next_board,'1-2','1-3')
                    elif next_board['1-1']!='0':# ok
                        if next_board['1-2']==next_board['1-3']:# ok
                            #[2,2,2,0]->[0,0,2,4]
                            next_board = self.sum_tile(next_board,'1-2','1-3',end)
                            next_board = self.move_tile(next_board,'1-3','1-4')
                            next_board = self.move_tile(next_board,'1-1','1-3')
                        elif next_board['1-1']==next_board['1-2']:# ok
                            #[2,2,4,0]->[0,0,4,4]
                            next_board = self.sum_tile(next_board,'1-1','1-2',end)
                            next_board = self.move_tile(next_board,'1-3','1-4')
                            next_board = self.move_tile(next_board,'1-2','1-3')
                        else:# ok
                            #[2,4,8,0]->[0,2,4,8]
                            next_board = self.move_tile(next_board,'1-3','1-4')
                            next_board = self.move_tile(next_board,'1-2','1-3')
                            next_board = self.move_tile(next_board,'1-1','1-2')
        elif next_board['1-4']!='0':# ok
            if next_board['1-3']=='0':# ok
                if next_board['1-2']=='0':# ok
                    if next_board['1-1']=='0':# ok
                        #[0,0,0,2]->何もしない
                        logging.debug('hoge')
                    elif next_board['1-1']!='0':# ok
                        if next_board['1-1']==next_board['1-4']:# ok
                            #[2,0,0,2]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'1-1','1-4',end)
                        elif next_board['1-1']!=next_board['1-4']:# ok
                            #[2,0,0,4]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'1-1','1-3')
                elif next_board['1-2']!='0':# ok
                    if next_board['1-1']=='0':# ok
                        if next_board['1-2']==next_board['1-4']:# ok
                            #[0,2,0,2]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'1-2','1-4',end)
                        elif next_board['1-2']!=next_board['1-4']:# ok
                            #[0,2,0,4]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'1-2','1-3')
                    elif next_board['1-1']!='0':# ok
                        if next_board['1-1']==next_board['1-2']:# ok #ミス
                            #[2,2,0,4]->[0,0,4,4]
                            next_board = self.sum_tile(next_board,'1-1','1-2',end)
                            next_board = self.move_tile(next_board,'1-2','1-3')
                        elif next_board['1-1']!=next_board['1-2']:# ok
                            #[2,4,0,0]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'1-2','1-4')
                            next_board = self.move_tile(next_board,'1-1','1-3')
            elif next_board['1-3']!='0':# ok
                if next_board['1-2']=='0':# ok
                    if next_board['1-1']=='0':# ok
                        if next_board['1-3']==next_board['1-4']:# ok
                            #[0,0,2,2]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'1-3','1-4',end)
                        elif next_board['1-3']!=next_board['1-4']:# ok
                            #[0,0,2,4]->[0,0,2,4]
                            logging.debug('hoge')
                    elif next_board['1-1']!='0':# ok
                        if next_board['1-3']==next_board['1-4']:# ok
                            #[2,0,2,2]->[0,0,2,4]
                            next_board = self.sum_tile(next_board,'1-3','1-4',end)
                            next_board = self.move_tile(next_board,'1-1','1-3')
                        elif next_board['1-1']==next_board['1-3']:# ok
                            #[2,0,2,4]->[0,0,4,4]
                            next_board = self.sum_tile(next_board,'1-1','1-3',end)
                        else:# ok
                            #[2,0,4,8]->[0,2,4,8]
                            next_board = self.move_tile(next_board,'1-1','1-2')
                elif next_board['1-2']!='0':# ok
                    if next_board['1-1']=='0':# ok
                        if next_board['1-3']==next_board['1-4']:# ok
                            #[0,2,2,2]->[0,0,2,4]
                            next_board = self.sum_tile(next_board,'1-3','1-4',end)
                            next_board = self.move_tile(next_board,'1-2','1-3')
                        elif next_board['1-2']==next_board['1-3']:# ok
                            #[0,2,2,4]->[0,0,4,4]
                            next_board = self.sum_tile(next_board,'1-2','1-3',end)
                        else:# ok
                            #[0,2,4,8]->[0,2,4,8]
                            logging.debug('hoge')
                    elif next_board['1-1']!='0':#全部違う場合->ok
                        if next_board['1-3']==next_board['1-4']:# ok
                            if next_board['1-1']==next_board['1-2']:# ok
                                #[2,2,2,2]->[0,0,4,4]
                                next_board = self.sum_tile(next_board,'1-3','1-4',end)
                                next_board = self.sum_tile(next_board,'1-1','1-2',end)
                                next_board = self.move_tile(next_board,'1-2','1-3')
                            else:# ok
                                #[2,4,2,2]->[0,2,4,4]
                                next_board = self.sum_tile(next_board,'1-3','1-4',end)
                                next_board = self.move_tile(next_board,'1-2','1-3')
                                next_board = self.move_tile(next_board,'1-1','1-2')
                        elif next_board['1-2']==next_board['1-3'] and next_board['1-3']!=next_board['1-4']:# ok
                            #[2,2,2,4]->[0,2,4,4]
                            next_board = self.sum_tile(next_board,'1-2','1-3',end)
                            next_board = self.move_tile(next_board,'1-1','1-2')
                        elif next_board['1-1']==next_board['1-2'] and next_board['1-2']!=next_board['1-3'] and next_board['1-3']!=next_board['1-4']:# ok
                            #[2,2,4,8]->[0,4,4,8]
                            next_board = self.sum_tile(next_board,'1-1','1-2',end)
                        else:# ok
                            #[2,4,8,16]->[2,4,8,16]
                            logging.debug('hoge')

        if next_board['2-4']=='0':# ok
            if next_board['2-3']=='0':# ok
                if next_board['2-2']=='0':# ok
                    if next_board['2-1']=='0':
                        #[0,0,0,0]->何もしない
                        logging.debug('hoge')
                    elif next_board['2-1']!='0':
                        #[2,0,0,0]->[0,0,0,2]
                        next_board = self.move_tile(next_board,'2-1','2-4')
                elif next_board['2-2']!='0':# ok
                    if next_board['2-1']=='0':
                        #[0,2,0,0]->[0,0,0,2]
                        next_board = self.move_tile(next_board,'2-2','2-4')
                    elif next_board['2-1']!='0':
                        if next_board['2-1']==next_board['2-2']:
                            #[2,2,0,0]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'2-1','2-2',end)
                            next_board = self.move_tile(next_board,'2-2','2-4')
                        elif next_board['2-1']!=next_board['2-2']:
                            #[2,4,0,0]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'2-2','2-4')
                            next_board = self.move_tile(next_board,'2-1','2-3')
            elif next_board['2-3']!='0':# ok
                if next_board['2-2']=='0':# ok
                    if next_board['2-1']=='0':# ok
                        #[0,0,2,0]->[0,0,0,2]
                        next_board = self.move_tile(next_board,'2-3','2-4')
                    elif next_board['2-1']!='0':# ok
                        if next_board['2-1']==next_board['2-3']:# ok
                            #[2,0,2,0]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'2-1','2-3',end)
                            next_board = self.move_tile(next_board,'2-3','2-4')
                        elif next_board['2-1']!=next_board['2-3']:# ok
                            #[2,0,4,0]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'2-3','2-4')
                            next_board = self.move_tile(next_board,'2-1','2-3')
                elif next_board['2-2']!='0':# ok
                    if next_board['2-1']=='0':# ok
                        if next_board['2-2']==next_board['2-3']:# ok
                            #[0,2,2,0]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'2-2','2-3',end)
                            next_board = self.move_tile(next_board,'2-3','2-4')
                        elif next_board['2-2']!=next_board['2-3']:# ok
                            #[0,2,4,0]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'2-3','2-4')
                            next_board = self.move_tile(next_board,'2-2','2-3')
                    elif next_board['2-1']!='0':# ok
                        if next_board['2-2']==next_board['2-3']:# ok
                            #[2,2,2,0]->[0,0,2,4]
                            next_board = self.sum_tile(next_board,'2-2','2-3',end)
                            next_board = self.move_tile(next_board,'2-3','2-4')
                            next_board = self.move_tile(next_board,'2-1','2-3')
                        elif next_board['2-1']==next_board['2-2']:# ok
                            #[2,2,4,0]->[0,0,4,4]
                            next_board = self.sum_tile(next_board,'2-1','2-2',end)
                            next_board = self.move_tile(next_board,'2-3','2-4')
                            next_board = self.move_tile(next_board,'2-2','2-3')
                        else:# ok
                            #[2,4,8,0]->[0,2,4,8]
                            next_board = self.move_tile(next_board,'2-3','2-4')
                            next_board = self.move_tile(next_board,'2-2','2-3')
                            next_board = self.move_tile(next_board,'2-1','2-2')
        elif next_board['2-4']!='0':# ok
            if next_board['2-3']=='0':# ok
                if next_board['2-2']=='0':# ok
                    if next_board['2-1']=='0':# ok
                        #[0,0,0,2]->何もしない
                        logging.debug('hoge')
                    elif next_board['2-1']!='0':# ok
                        if next_board['2-1']==next_board['2-4']:# ok
                            #[2,0,0,2]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'2-1','2-4',end)
                        elif next_board['2-1']!=next_board['2-4']:# ok
                            #[2,0,0,4]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'2-1','2-3')
                elif next_board['2-2']!='0':# ok
                    if next_board['2-1']=='0':# ok
                        if next_board['2-2']==next_board['2-4']:# ok
                            #[0,2,0,2]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'2-2','2-4',end)
                        elif next_board['2-2']!=next_board['2-4']:# ok
                            #[0,2,0,4]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'2-2','2-3')
                    elif next_board['2-1']!='0':# ok
                        if next_board['2-1']==next_board['2-2']:# ok #ミス
                            #[2,2,0,4]->[0,0,4,4]
                            next_board = self.sum_tile(next_board,'2-1','2-2',end)
                            next_board = self.move_tile(next_board,'2-2','2-3')
                        elif next_board['2-1']!=next_board['2-2']:# ok
                            #[2,4,0,0]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'2-2','2-4')
                            next_board = self.move_tile(next_board,'2-1','2-3')
            elif next_board['2-3']!='0':# ok
                if next_board['2-2']=='0':# ok
                    if next_board['2-1']=='0':# ok
                        if next_board['2-3']==next_board['2-4']:# ok
                            #[0,0,2,2]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'2-3','2-4',end)
                        elif next_board['2-3']!=next_board['2-4']:# ok
                            #[0,0,2,4]->[0,0,2,4]
                            logging.debug('hoge')
                    elif next_board['2-1']!='0':# ok
                        if next_board['2-3']==next_board['2-4']:# ok
                            #[2,0,2,2]->[0,0,2,4]
                            next_board = self.sum_tile(next_board,'2-3','2-4',end)
                            next_board = self.move_tile(next_board,'2-1','2-3')
                        elif next_board['2-1']==next_board['2-3']:# ok
                            #[2,0,2,4]->[0,0,4,4]
                            next_board = self.sum_tile(next_board,'2-1','2-3',end)
                        else:# ok
                            #[2,0,4,8]->[0,2,4,8]
                            next_board = self.move_tile(next_board,'2-1','2-2')
                elif next_board['2-2']!='0':# ok
                    if next_board['2-1']=='0':# ok
                        if next_board['2-3']==next_board['2-4']:# ok
                            #[0,2,2,2]->[0,0,2,4]
                            next_board = self.sum_tile(next_board,'2-3','2-4',end)
                            next_board = self.move_tile(next_board,'2-2','2-3')
                        elif next_board['2-2']==next_board['2-3']:# ok
                            #[0,2,2,4]->[0,0,4,4]
                            next_board = self.sum_tile(next_board,'2-2','2-3',end)
                        else:# ok
                            #[0,2,4,8]->[0,2,4,8]
                            logging.debug('hoge')
                    elif next_board['2-1']!='0':#全部違う場合->ok
                        if next_board['2-3']==next_board['2-4']:# ok
                            if next_board['2-1']==next_board['2-2']:# ok
                                #[2,2,2,2]->[0,0,4,4]
                                next_board = self.sum_tile(next_board,'2-3','2-4',end)
                                next_board = self.sum_tile(next_board,'2-1','2-2',end)
                                next_board = self.move_tile(next_board,'2-2','2-3')
                            else:# ok
                                #[2,4,2,2]->[0,2,4,4]
                                next_board = self.sum_tile(next_board,'2-3','2-4',end)
                                next_board = self.move_tile(next_board,'2-2','2-3')
                                next_board = self.move_tile(next_board,'2-1','2-2')
                        elif next_board['2-2']==next_board['2-3'] and next_board['2-3']!=next_board['2-4']:# ok
                            #[2,2,2,4]->[0,2,4,4]
                            next_board = self.sum_tile(next_board,'2-2','2-3',end)
                            next_board = self.move_tile(next_board,'2-1','2-2')
                        elif next_board['2-1']==next_board['2-2'] and next_board['2-2']!=next_board['2-3'] and next_board['2-3']!=next_board['2-4']:# ok
                            #[2,2,4,8]->[0,4,4,8]
                            next_board = self.sum_tile(next_board,'2-1','2-2',end)
                        else:# ok
                            #[2,4,8,16]->[2,4,8,16]
                            logging.debug('hoge')

        if next_board['3-4']=='0':# ok
            if next_board['3-3']=='0':# ok
                if next_board['3-2']=='0':# ok
                    if next_board['3-1']=='0':
                        #[0,0,0,0]->何もしない
                        logging.debug('hoge')
                    elif next_board['3-1']!='0':
                        #[2,0,0,0]->[0,0,0,2]
                        next_board = self.move_tile(next_board,'3-1','3-4')
                elif next_board['3-2']!='0':# ok
                    if next_board['3-1']=='0':
                        #[0,2,0,0]->[0,0,0,2]
                        next_board = self.move_tile(next_board,'3-2','3-4')
                    elif next_board['3-1']!='0':
                        if next_board['3-1']==next_board['3-2']:
                            #[2,2,0,0]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'3-1','3-2',end)
                            next_board = self.move_tile(next_board,'3-2','3-4')
                        elif next_board['3-1']!=next_board['3-2']:
                            #[2,4,0,0]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'3-2','3-4')
                            next_board = self.move_tile(next_board,'3-1','3-3')
            elif next_board['3-3']!='0':# ok
                if next_board['3-2']=='0':# ok
                    if next_board['3-1']=='0':# ok
                        #[0,0,2,0]->[0,0,0,2]
                        next_board = self.move_tile(next_board,'3-3','3-4')
                    elif next_board['3-1']!='0':# ok
                        if next_board['3-1']==next_board['3-3']:# ok
                            #[2,0,2,0]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'3-1','3-3',end)
                            next_board = self.move_tile(next_board,'3-3','3-4')
                        elif next_board['3-1']!=next_board['3-3']:# ok
                            #[2,0,4,0]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'3-3','3-4')
                            next_board = self.move_tile(next_board,'3-1','3-3')
                elif next_board['3-2']!='0':# ok
                    if next_board['3-1']=='0':# ok
                        if next_board['3-2']==next_board['3-3']:# ok
                            #[0,2,2,0]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'3-2','3-3',end)
                            next_board = self.move_tile(next_board,'3-3','3-4')
                        elif next_board['3-2']!=next_board['3-3']:# ok
                            #[0,2,4,0]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'3-3','3-4')
                            next_board = self.move_tile(next_board,'3-2','3-3')
                    elif next_board['3-1']!='0':# ok
                        if next_board['3-2']==next_board['3-3']:# ok
                            #[2,2,2,0]->[0,0,2,4]
                            next_board = self.sum_tile(next_board,'3-2','3-3',end)
                            next_board = self.move_tile(next_board,'3-3','3-4')
                            next_board = self.move_tile(next_board,'3-1','3-3')
                        elif next_board['3-1']==next_board['3-2']:# ok
                            #[2,2,4,0]->[0,0,4,4]
                            next_board = self.sum_tile(next_board,'3-1','3-2',end)
                            next_board = self.move_tile(next_board,'3-3','3-4')
                            next_board = self.move_tile(next_board,'3-2','3-3')
                        else:# ok
                            #[2,4,8,0]->[0,2,4,8]
                            next_board = self.move_tile(next_board,'3-3','3-4')
                            next_board = self.move_tile(next_board,'3-2','3-3')
                            next_board = self.move_tile(next_board,'3-1','3-2')
        elif next_board['3-4']!='0':# ok
            if next_board['3-3']=='0':# ok
                if next_board['3-2']=='0':# ok
                    if next_board['3-1']=='0':# ok
                        #[0,0,0,2]->何もしない
                        logging.debug('hoge')
                    elif next_board['3-1']!='0':# ok
                        if next_board['3-1']==next_board['3-4']:# ok
                            #[2,0,0,2]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'3-1','3-4',end)
                        elif next_board['3-1']!=next_board['3-4']:# ok
                            #[2,0,0,4]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'3-1','3-3')
                elif next_board['3-2']!='0':# ok
                    if next_board['3-1']=='0':# ok
                        if next_board['3-2']==next_board['3-4']:# ok
                            #[0,2,0,2]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'3-2','3-4',end)
                        elif next_board['3-2']!=next_board['3-4']:# ok
                            #[0,2,0,4]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'3-2','3-3')
                    elif next_board['3-1']!='0':# ok
                        if next_board['3-1']==next_board['3-2']:# ok #ミス
                            #[2,2,0,4]->[0,0,4,4]
                            next_board = self.sum_tile(next_board,'3-1','3-2',end)
                            next_board = self.move_tile(next_board,'3-2','3-3')
                        elif next_board['3-1']!=next_board['3-2']:# ok
                            #[2,4,0,0]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'3-2','3-4')
                            next_board = self.move_tile(next_board,'3-1','3-3')
            elif next_board['3-3']!='0':# ok
                if next_board['3-2']=='0':# ok
                    if next_board['3-1']=='0':# ok
                        if next_board['3-3']==next_board['3-4']:# ok
                            #[0,0,2,2]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'3-3','3-4',end)
                        elif next_board['3-3']!=next_board['3-4']:# ok
                            #[0,0,2,4]->[0,0,2,4]
                            logging.debug('hoge')
                    elif next_board['3-1']!='0':# ok
                        if next_board['3-3']==next_board['3-4']:# ok
                            #[2,0,2,2]->[0,0,2,4]
                            next_board = self.sum_tile(next_board,'3-3','3-4',end)
                            next_board = self.move_tile(next_board,'3-1','3-3')
                        elif next_board['3-1']==next_board['3-3']:# ok
                            #[2,0,2,4]->[0,0,4,4]
                            next_board = self.sum_tile(next_board,'3-1','3-3',end)
                        else:# ok
                            #[2,0,4,8]->[0,2,4,8]
                            next_board = self.move_tile(next_board,'3-1','3-2')
                elif next_board['3-2']!='0':# ok
                    if next_board['3-1']=='0':# ok
                        if next_board['3-3']==next_board['3-4']:# ok
                            #[0,2,2,2]->[0,0,2,4]
                            next_board = self.sum_tile(next_board,'3-3','3-4',end)
                            next_board = self.move_tile(next_board,'3-2','3-3')
                        elif next_board['3-2']==next_board['3-3']:# ok
                            #[0,2,2,4]->[0,0,4,4]
                            next_board = self.sum_tile(next_board,'3-2','3-3',end)
                        else:# ok
                            #[0,2,4,8]->[0,2,4,8]
                            logging.debug('hoge')
                    elif next_board['3-1']!='0':#全部違う場合->ok
                        if next_board['3-3']==next_board['3-4']:# ok
                            if next_board['3-1']==next_board['3-2']:# ok
                                #[2,2,2,2]->[0,0,4,4]
                                next_board = self.sum_tile(next_board,'3-3','3-4',end)
                                next_board = self.sum_tile(next_board,'3-1','3-2',end)
                                next_board = self.move_tile(next_board,'3-2','3-3')
                            else:# ok
                                #[2,4,2,2]->[0,2,4,4]
                                next_board = self.sum_tile(next_board,'3-3','3-4',end)
                                next_board = self.move_tile(next_board,'3-2','3-3')
                                next_board = self.move_tile(next_board,'3-1','3-2')
                        elif next_board['3-2']==next_board['3-3'] and next_board['3-3']!=next_board['3-4']:# ok
                            #[2,2,2,4]->[0,2,4,4]
                            next_board = self.sum_tile(next_board,'3-2','3-3',end)
                            next_board = self.move_tile(next_board,'3-1','3-2')
                        elif next_board['3-1']==next_board['3-2'] and next_board['3-2']!=next_board['3-3'] and next_board['3-3']!=next_board['3-4']:# ok
                            #[2,2,4,8]->[0,4,4,8]
                            next_board = self.sum_tile(next_board,'3-1','3-2',end)
                        else:# ok
                            #[2,4,8,16]->[2,4,8,16]
                            logging.debug('hoge')

        if next_board['4-4']=='0':# ok
            if next_board['4-3']=='0':# ok
                if next_board['4-2']=='0':# ok
                    if next_board['4-1']=='0':
                        #[0,0,0,0]->何もしない
                        logging.debug('hoge')
                    elif next_board['4-1']!='0':
                        #[2,0,0,0]->[0,0,0,2]
                        next_board = self.move_tile(next_board,'4-1','4-4')
                elif next_board['4-2']!='0':# ok
                    if next_board['4-1']=='0':
                        #[0,2,0,0]->[0,0,0,2]
                        next_board = self.move_tile(next_board,'4-2','4-4')
                    elif next_board['4-1']!='0':
                        if next_board['4-1']==next_board['4-2']:
                            #[2,2,0,0]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'4-1','4-2',end)
                            next_board = self.move_tile(next_board,'4-2','4-4')
                        elif next_board['4-1']!=next_board['4-2']:
                            #[2,4,0,0]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'4-2','4-4')
                            next_board = self.move_tile(next_board,'4-1','4-3')
            elif next_board['4-3']!='0':# ok
                if next_board['4-2']=='0':# ok
                    if next_board['4-1']=='0':# ok
                        #[0,0,2,0]->[0,0,0,2]
                        next_board = self.move_tile(next_board,'4-3','4-4')
                    elif next_board['4-1']!='0':# ok
                        if next_board['4-1']==next_board['4-3']:# ok
                            #[2,0,2,0]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'4-1','4-3',end)
                            next_board = self.move_tile(next_board,'4-3','4-4')
                        elif next_board['4-1']!=next_board['4-3']:# ok
                            #[2,0,4,0]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'4-3','4-4')
                            next_board = self.move_tile(next_board,'4-1','4-3')
                elif next_board['4-2']!='0':# ok
                    if next_board['4-1']=='0':# ok
                        if next_board['4-2']==next_board['4-3']:# ok
                            #[0,2,2,0]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'4-2','4-3',end)
                            next_board = self.move_tile(next_board,'4-3','4-4')
                        elif next_board['4-2']!=next_board['4-3']:# ok
                            #[0,2,4,0]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'4-3','4-4')
                            next_board = self.move_tile(next_board,'4-2','4-3')
                    elif next_board['4-1']!='0':# ok
                        if next_board['4-2']==next_board['4-3']:# ok
                            #[2,2,2,0]->[0,0,2,4]
                            next_board = self.sum_tile(next_board,'4-2','4-3',end)
                            next_board = self.move_tile(next_board,'4-3','4-4')
                            next_board = self.move_tile(next_board,'4-1','4-3')
                        elif next_board['4-1']==next_board['4-2']:# ok
                            #[2,2,4,0]->[0,0,4,4]
                            next_board = self.sum_tile(next_board,'4-1','4-2',end)
                            next_board = self.move_tile(next_board,'4-3','4-4')
                            next_board = self.move_tile(next_board,'4-2','4-3')
                        else:# ok
                            #[2,4,8,0]->[0,2,4,8]
                            next_board = self.move_tile(next_board,'4-3','4-4')
                            next_board = self.move_tile(next_board,'4-2','4-3')
                            next_board = self.move_tile(next_board,'4-1','4-2')
        elif next_board['4-4']!='0':# ok
            if next_board['4-3']=='0':# ok
                if next_board['4-2']=='0':# ok
                    if next_board['4-1']=='0':# ok
                        #[0,0,0,2]->何もしない
                        logging.debug('hoge')
                    elif next_board['4-1']!='0':# ok
                        if next_board['4-1']==next_board['4-4']:# ok
                            #[2,0,0,2]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'4-1','4-4',end)
                        elif next_board['4-1']!=next_board['4-4']:# ok
                            #[2,0,0,4]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'4-1','4-3')
                elif next_board['4-2']!='0':# ok
                    if next_board['4-1']=='0':# ok
                        if next_board['4-2']==next_board['4-4']:# ok
                            #[0,2,0,2]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'4-2','4-4',end)
                        elif next_board['4-2']!=next_board['4-4']:# ok
                            #[0,2,0,4]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'4-2','4-3')
                    elif next_board['4-1']!='0':# ok
                        if next_board['4-1']==next_board['4-2']:# ok #ミス
                            #[2,2,0,4]->[0,0,4,4]
                            next_board = self.sum_tile(next_board,'4-1','4-2',end)
                            next_board = self.move_tile(next_board,'4-2','4-3')
                        elif next_board['4-1']!=next_board['4-2']:# ok
                            #[2,4,0,0]->[0,0,2,4]
                            next_board = self.move_tile(next_board,'4-2','4-4')
                            next_board = self.move_tile(next_board,'4-1','4-3')
            elif next_board['4-3']!='0':# ok
                if next_board['4-2']=='0':# ok
                    if next_board['4-1']=='0':# ok
                        if next_board['4-3']==next_board['4-4']:# ok
                            #[0,0,2,2]->[0,0,0,4]
                            next_board = self.sum_tile(next_board,'4-3','4-4',end)
                        elif next_board['4-3']!=next_board['4-4']:# ok
                            #[0,0,2,4]->[0,0,2,4]
                            logging.debug('hoge')
                    elif next_board['4-1']!='0':# ok
                        if next_board['4-3']==next_board['4-4']:# ok
                            #[2,0,2,2]->[0,0,2,4]
                            next_board = self.sum_tile(next_board,'4-3','4-4',end)
                            next_board = self.move_tile(next_board,'4-1','4-3')
                        elif next_board['4-1']==next_board['4-3']:# ok
                            #[2,0,2,4]->[0,0,4,4]
                            next_board = self.sum_tile(next_board,'4-1','4-3',end)
                        else:# ok
                            #[2,0,4,8]->[0,2,4,8]
                            next_board = self.move_tile(next_board,'4-1','4-2')
                elif next_board['4-2']!='0':# ok
                    if next_board['4-1']=='0':# ok
                        if next_board['4-3']==next_board['4-4']:# ok
                            #[0,2,2,2]->[0,0,2,4]
                            next_board = self.sum_tile(next_board,'4-3','4-4',end)
                            next_board = self.move_tile(next_board,'4-2','4-3')
                        elif next_board['4-2']==next_board['4-3']:# ok
                            #[0,2,2,4]->[0,0,4,4]
                            next_board = self.sum_tile(next_board,'4-2','4-3',end)
                        else:# ok
                            #[0,2,4,8]->[0,2,4,8]
                            logging.debug('hoge')
                    elif next_board['4-1']!='0':#全部違う場合->ok
                        if next_board['4-3']==next_board['4-4']:# ok
                            if next_board['4-1']==next_board['4-2']:# ok
                                #[2,2,2,2]->[0,0,4,4]
                                next_board = self.sum_tile(next_board,'4-3','4-4',end)
                                next_board = self.sum_tile(next_board,'4-1','4-2',end)
                                next_board = self.move_tile(next_board,'4-2','4-3')
                            else:# ok
                                #[2,4,2,2]->[0,2,4,4]
                                next_board = self.sum_tile(next_board,'4-3','4-4',end)
                                next_board = self.move_tile(next_board,'4-2','4-3')
                                next_board = self.move_tile(next_board,'4-1','4-2')
                        elif next_board['4-2']==next_board['4-3'] and next_board['4-3']!=next_board['4-4']:# ok
                            #[2,2,2,4]->[0,2,4,4]
                            next_board = self.sum_tile(next_board,'4-2','4-3',end)
                            next_board = self.move_tile(next_board,'4-1','4-2')
                        elif next_board['4-1']==next_board['4-2'] and next_board['4-2']!=next_board['4-3'] and next_board['4-3']!=next_board['4-4']:# ok
                            #[2,2,4,8]->[0,4,4,8]
                            next_board = self.sum_tile(next_board,'4-1','4-2',end)
                        else:# ok
                            #[2,4,8,16]->[2,4,8,16]
                            logging.debug('hoge')

        return next_board

    def rotate_right(self, next_board):
        # 右90度移動
        copy_board = copy.deepcopy(next_board)
        next_board['1-1'] = copy_board['1-4']
        next_board['1-2'] = copy_board['2-4']
        next_board['1-3'] = copy_board['3-4']
        next_board['1-4'] = copy_board['4-4']
        next_board['2-1'] = copy_board['1-3']
        next_board['2-2'] = copy_board['2-3']
        next_board['2-3'] = copy_board['3-3']
        next_board['2-4'] = copy_board['4-3']
        next_board['3-1'] = copy_board['1-2']
        next_board['3-2'] = copy_board['2-2']
        next_board['3-3'] = copy_board['3-2']
        next_board['3-4'] = copy_board['4-2']
        next_board['4-1'] = copy_board['1-1']
        next_board['4-2'] = copy_board['2-1']
        next_board['4-3'] = copy_board['3-1']
        next_board['4-4'] = copy_board['4-1']
        return next_board

    def rotate_left(self, next_board):
        # 左90度移動
        next_board = self.rotate_right(next_board)
        next_board = self.rotate_right(next_board)
        next_board = self.rotate_right(next_board)
        return next_board

    def flick_board(self, board, direction, end):
        # direction方向のフリックの結果を返す
        next_board = copy.deepcopy(board)

        if direction=='right':
            next_board = self.rotate_right(next_board)
            next_board = self.down_move(next_board,end)
            next_board = self.rotate_left(next_board)
        elif direction=='down':
            next_board = self.down_move(next_board,end)
        elif direction=='left':
            next_board = self.rotate_left(next_board)
            next_board = self.down_move(next_board,end)
            next_board = self.rotate_right(next_board)
        elif direction=='up':
            next_board = self.rotate_right(next_board)
            next_board = self.rotate_right(next_board)
            next_board = self.down_move(next_board,end)
            next_board = self.rotate_left(next_board)
            next_board = self.rotate_left(next_board)
        else:
            logging.debug('direction error')


        return next_board

    def new_tile_appear(self, board):
        zero_list = []
        for key,value in board.items():
            if value=='0':
                zero_list.append(key)
        random_num = randint(len(zero_list))
        key_selected = zero_list[random_num]

        two_or_four = randint(0,10)
        if two_or_four==9:
            board[key_selected] = '4'
        else:
            board[key_selected] = '2'
        return board

    def end_check(self):
        end_cnt = 0
        dirs = ['right','down','left','up']
        for direction in dirs:
            new_board = self.flick_board(self.board, direction,1)
            if self.board == new_board:
                end_cnt += 1
        if end_cnt==4:
            #どの方向に動かしても局面が変わらない＝詰み
            end_flag = True
        else:
            end_flag = False
        return end_flag

    def reset(self):
        self.board = {'1-1':'0','1-2':'0','1-3':'0','1-4':'0',\
                    '2-1':'0','2-2':'0','2-3':'0','2-4':'0',\
                    '3-1':'0','3-2':'0','3-3':'0','3-4':'0',\
                    '4-1':'0','4-2':'0','4-3':'0','4-4':'0'}# 初期設定は全て0
        #　はじめに二つのタイルを出現させる
        self.board = self.new_tile_appear(self.board)
        self.board = self.new_tile_appear(self.board)

        self.max_num = 0
        self.score = 0
        self.cnt = 0
        self.end_flag = False
        self.flag = False

    def step(self, action):

        # print("direction: {}".format(self.dirs[action]))
        if self.dirs[action] == 'r':
            new_board = self.flick_board(self.board, 'right', 0)
        elif self.dirs[action] == 'd':
            new_board = self.flick_board(self.board, 'down', 0)
        elif self.dirs[action] == 'l':
            new_board = self.flick_board(self.board, 'left', 0)
        elif self.dirs[action] == 'u':
            new_board = self.flick_board(self.board, 'up', 0)
        else:
            print("error")

        flag = not (self.board == new_board)

        print(flag)
        if flag:
            new_board = self.new_tile_appear(new_board)
        
        self.board = new_board

        numbers = np.array([int(value) for key, value in self.board.items()])
        self.max_num = max(numbers)

        self.end_flag = self.end_check()
