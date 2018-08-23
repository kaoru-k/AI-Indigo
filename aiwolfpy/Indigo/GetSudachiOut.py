# coding:utf-8

# getSudachiOut.py
#
# author Kaoru Kimura

'''
まだできていないこと
・精度アップ
'''

import json
import sudachipy
from sudachipy import dictionary
from . import contentbuilder as cb

wordList = {
    '思う' : 'est',
    'です' : 'co',
    'ＣＯ': 'co',
    'CO' : 'co',
    'カミングアウト' : 'co',
    'だ' : 'co',
    '占い' : 'div',
    '占う' : 'div',
    '占' : 'div',
    '結果' : 'divd',
    '投票' : 'vote',
    '僕' : 'my',
    '私' : 'my',
    '俺' : 'my',
}

class GetSudachiOut(object):
    def __init__(self):
        with open(sudachipy.config.SETTINGFILE, 'r', encoding='utf-8') as f:
            sudachi_settings = json.load(f)
        dict = dictionary.Dictionary(sudachi_settings)
        self.sudachi_instance = dict.create()
        self.nameList = {
            '1' : '一郎',
            '2' : '二郎',
            '3' : '三郎',
            '4' : '四郎',
            '5' : '五郎',
            }

    def initialize(self,idxlist):
        self.idxlist = idxlist
        self.nameList = {
            self.idxlist[0] : '一郎',
            self.idxlist[1] : '二郎',
            self.idxlist[2] : '三郎',
            self.idxlist[3] : '四郎',
            self.idxlist[4] : '五郎',
            }
    
    '''
    形態素解析のためにAgent[xx]〜[xx]を一郎〜五郎に書き換える
    '''
    def txt2Nl(self,text):
        while True:
            textIdx = text.find('Agent[')
            if textIdx != -1:
                name = self.nameList.get(int(text[textIdx+6:textIdx+8]))
                if name is None:
                    text = text[:textIdx] + text[textIdx+9:]
                else:
                    text = text[:textIdx] + name + text[textIdx+9:]
            else:
                break
        return text

    '''
    形態素解析を行う
    '''
    def tokenize(self,text):
        tokenized = self.sudachi_instance.tokenize(self.sudachi_instance.SplitMode.A,text)
        return tokenized

    '''
    自然言語から人狼知能プロトコルに変換する
    '''
    def nl2Aiwp(self, subject, target, text, flag, repTarget):
        role = None
        species = None
        flg_subj = False
        flg_est  = False
        flg_co   = False
        flg_div  = False
        flg_divd = False
        flg_vote = False
        flg_question = False
        talks = []
        tList = []

        while True:    
            textIdx = text.find('、') # '、'で文章を分割
            if textIdx != -1:
                textIdx = text.find('。')
            if textIdx != -1:
                talks.append(text[:textIdx])
                text = text[textIdx+1:]
            else:
                talks.append(text)
                break

        # 分割した文章ごとに処理する
        for t in talks:
            tokenized = self.tokenize(t)
            
            # 単語の認識
            for w in tokenized:
                normalized_form = w.normalized_form()
                wl = wordList.get(normalized_form)

                # subject確認
                if wl == 'my':
                    target = subject
                    flg_subj = True

                # target判別
                if normalized_form[1:2] == '郎':
                    if normalized_form[:1] == '一':
                        target = self.idxlist[0]
                    elif normalized_form[:1] == '二':
                        target = self.idxlist[1]
                    elif normalized_form[:1] == '三':
                        target = self.idxlist[2]
                    elif normalized_form[:1] == '四':
                        target = self.idxlist[3]
                    elif normalized_form[:1] == '五':
                        target = self.idxlist[4]

                # role判別
                if normalized_form.find('狼') != -1:
                    role = 'WEREWOLF'
                elif normalized_form == '村人' or normalized_form == '村':
                    role = 'VILLAGER'
                elif normalized_form == '占い師':
                    role = 'SEER'
                elif normalized_form == '狂人':
                    role = 'POSSESSED'

                # species判別
                if normalized_form.find('狼') != -1 or normalized_form == '黒':
                    species = 'WEREWOLF'
                elif normalized_form.find('人間') != -1 or normalized_form == '白':
                    species = 'HUMAN'
                
                # talk判別
                if wl == 'est':
                    flg_est = True
                elif wl == 'co':
                    flg_co = True
                elif wl == 'div':
                    flg_div = True
                elif wl == 'divd':
                    flg_divd = True
                elif wl == 'vote':
                    flg_vote = True
                
                if w == '？':
                    flg_question = True

            # 単語の認識結果からプロトコルに変換
            if target is not None:
                if flg_vote == True:
                    if target != subject:
                        if flg_question == True:
                            tList.append(cb.skip())
                        else:
                            tList.append(cb.vote(target))
                        flg_vote = False
                        target = None                    
                elif flg_divd == True:
                    if species == 'WEREWOLF' or species == 'HUMAN':
                        tList.append(cb.divined(target,species))
                        flg_divd = False
                        flg_div = False
                        species = None
                        role = None                        
                elif flg_div == True:
                    if target != subject:
                        tList.append(cb.divine(target))
                        flg_div = False
                        target = None
                elif flg_co == True or flg_est == True:
                    if role is not None and flg_subj == True:
                        if flg_question == True:
                            tList.append(cb.skip())
                        else:
                            tList.append(cb.comingout(subject, role))
                        flg_co = False
                        target = None
                        role = None
                    elif target != subject and role is not None:
                        if flg_question == True:
                            tList.append(cb.skip())
                        else:
                            tList.append(cb.estimate(target, role))
                        flg_est = False
                        target = None
                        role = None
            elif target is None and flg_co == True and role is not None:
                if flg_div == False and flg_divd == False and flg_est == False and flg_subj == False and flg_vote == False:
                    if flg_question == True:
                        tList.append(cb.skip())
                    else:
                        tList.append(cb.comingout(subject, role))            
        
        if target is not None:
            if flg_vote == True:
                if target != subject:
                    tList.append(cb.vote(target))
            elif flg_divd == True:
                if species == 'WEREWOLF' or species == 'HUMAN':
                    tList.append(cb.divined(target,species))
            elif flg_div == True:
                if target != subject:
                    tList.append(cb.divine(target))
            elif flg_co == True or flg_est == True:
                if flg_subj == True and role is not None:
                    tList.append(cb.comingout(subject, role))
                elif target != subject and role is not None:
                    tList.append(cb.estimate(target, role))
        
        if len(tList) == 0:
            tList.append(cb.skip())
        
        if flag == True:
            tmpList = []
            for t in tList:
                tmpList.append('>>Agent[{num:02}] '.format(num=repTarget) + t)
            tList = tmpList
        return tList

    '''
    txt2Nl後nl2aiwpを行う
    '''
    def txt2Aiwp(self,subject,text):
        target = None
        flag = False
        repTarget = None
        if text[:8] == '>>Agent[':
            target = int(text[8:10])
            repTarget = target
            text = text[12:]
            flag = True
     
        return self.nl2Aiwp(subject, target, self.txt2Nl(text), flag, repTarget)