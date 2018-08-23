import pandas as pd
import random

class Agents5_base(object):
    def __init__(self):
        self.prob = pd.read_csv('result_prob.csv',index_col='VERB')
        self.roleEst = pd.DataFrame(
            {'WEREWOLF': [1.0,1.0,1.0,1.0,1.0],
            'POSSESSED': [1.0,1.0,1.0,1.0,1.0],
            'SEER'     : [1.0,1.0,1.0,1.0,1.0],
            'VILLAGER' : [1.0,1.0,1.0,1.0,1.0],},
            columns = ['WEREWOLF','POSSESSED','SEER','VILLAGER'],
            index = [1,2,3,4,5])
        self.lastGame = 'newtral'

    def initialize(self, base_info, game_setting):
        self.game_setting = game_setting
        self.base_info = base_info
        self.agentIdx = self.base_info['agentIdx']
        self.idxlist = []
        for k in base_info['statusMap'].keys():
            self.idxlist.append(int(k))
        self.roleEst = pd.DataFrame(
            {'WEREWOLF': [1.0,1.0,1.0,1.0,1.0],
            'POSSESSED': [1.0,1.0,1.0,1.0,1.0],
            'SEER'     : [1.0,1.0,1.0,1.0,1.0],
            'VILLAGER' : [1.0,1.0,1.0,1.0,1.0],},
            columns = ['WEREWOLF','POSSESSED','SEER','VILLAGER'],
            index = self.idxlist)
        for i in self.idxlist:
            for column in self.roleEst.columns:
                if i == self.agentIdx:
                    if column == base_info['myRole']:
                        self.roleEst.at[i,column] = 1.0
                    else:
                        self.roleEst.at[i,column] = 0.0
                elif column == base_info['myRole']:
                    self.roleEst.at[i,column] = 0.0
        
        self.firstTalk = False   # 初日の挨拶をしたかどうか
        self.dayGreeting = False # 1日の始まりに挨拶をしたか
        self.esttalk1 = False     # ESTIMATE発言をしたかどうか1
        self.esttalk2 = False     # ESTIMATE発言をしたかどうか2
        self.seeridx = None      # 占い結果を報告した人の番号
        self.divdidx = None      # DIVINEDしてきたプレイヤー番号 
        self.divrepo = False     # 占い結果を報告したかどうか
        self.divresult = ''      # 占い結果
        self.liedividx = None    # 嘘の占い結果を言った対象のID
        self.talkFrom = -1       # 誰かから話しかけられたか（デフォルト:-1）
        self.talkContent = ''    # 話しかけられた内容

        self.foundwolf = None # 自分が占い師の時のみ　狼を見つけた場合の狼のプレイヤー番号
        self.foundhuman = None #　自分が占い師の時のみ　人間を見つけた場合のそのプレイヤー番号
        self.possessedCO = None # 自分が狼の時のみ　狂人COしたプレイヤー番号
        self.maybepossessed = None # 自分が狼/村人時のみ　占い結果的に狂人なプレイヤー番号
        self.maybeseer = None # 自分が狼/村人時のみ　自分を狼の占い結果を言ったプレイヤー番号

        self.estlist ={
            self.idxlist[0] : '',
            self.idxlist[1] : '',
            self.idxlist[2] : '',
            self.idxlist[3] : '',
            self.idxlist[4] : '',
        } # ESTIMATEした役職名
        self.coedlist ={
            self.idxlist[0] : '',
            self.idxlist[1] : '',
            self.idxlist[2] : '',
            self.idxlist[3] : '',
            self.idxlist[4] : '',
        } # COMINGOUTした役職名
        self.divdlist = {
            self.idxlist[0] : '',
            self.idxlist[1] : '',
            self.idxlist[2] : '',
            self.idxlist[3] : '',
            self.idxlist[4] : '',
        } # DIVINEされた種族名
        self.gamefin = False # ゲームがfinishしたかどうか

        print('My agentidx = {}, role = {}'.format(self.agentIdx, self.base_info['myRole']))

    def update(self,base_info, diff_data, request):
        if request == 'DAILY_INITIALIZE':
            for i in range(diff_data.shape[0]):
                # DIVINE
                if diff_data['type'][i] == 'divine':
                    self.divresult = diff_data['text'][i]
                
            # POSSESSED
            if self.base_info['myRole'] == 'POSSESSED':
                while True:
                    i = random.choice(self.idxlist)
                    if self.probably('SEER') != i and i != self.agentIdx:
                        self.divresult = 'divine Agent[' + '{0:02d}'.format(i) + '] WEREWOLF'
                        break

        self.base_info = base_info
        # print(base_info)

    def read_talklog(self, gamedf, i, t):
        content = t.split()
        # 文頭にアンカーが付いているときの処理
        if content[0][:8] == '>>Agent[':
            if int(content[0][8:10]) == self.agentIdx:
                self.talkFrom = gamedf.agent[i]
                self.talkContent = content[1:]
            content = content[1:]
        
        if content[0] == 'ESTIMATE':
            self.estlist[gamedf.agent[i]] = content[2]
            if gamedf.agent[i] != self.agentIdx:
                self.update_est(gamedf.agent[i],content[0] + '(' + content[2] + ')')
        elif content[0] == 'COMINGOUT':
            self.coedlist[gamedf.agent[i]] = content[2]
            if gamedf.agent[i] != self.agentIdx:
                self.update_est(gamedf.agent[i],content[0] + '(' + content[2] + ')')
        elif content[0] == 'VOTE':
            if gamedf.agent[i] != self.agentIdx:
                self.update_est(gamedf.agent[i],'VOTE')
        elif content[0] == 'DIVINED':
            n = int(content[1][6:8])
            if self.divdlist[n] == '':
                self.divdlist[n] = content[2]
            elif self.divdlist[n] == 'HUMAN' and content[2] == 'HUMAN':
                self.divdlist[n] = 'HUMAN_EX'
            elif self.divdlist[n] == 'HUMAN' and content[2] == 'WEREWOLF':
                self.divdlist[n] = 'PANDA'
            elif self.divdlist[n] == 'WEREWOLF' and content[2] == 'HUMAN':
                self.divdlist[n] = 'PANDA'
            elif self.divdlist[n] == 'WEREWOLF' and content[2] == 'WEREWOLF':
                self.divdlist[n] = 'WEREWOLF_EX'
            if gamedf.agent[i] != self.agentIdx:
                self.seeridx = gamedf.agent[i]
                self.update_est(gamedf.agent[i],'DIVINED(' + content[2] + ')')
                if self.base_info['myRole'] == 'WEREWOLF':
                    if n == self.agentIdx:
                        if content[2] == 'WEREWOLF':
                            self.maybeseer = gamedf.agent[i]
                        elif content[2] == 'HUMAN':
                            self.maybepossessed = gamedf.agent[i]
                    elif n != self.agentIdx:
                        if content[2] == 'WEREWOLF':
                            self.maybepossessed = gamedf.agent[i]
                elif self.base_info['myRole'] == 'VILLAGER':
                    if n == self.agentIdx:
                        if content[2] == 'WEREWOLF':
                            self.maybepossessed = gamedf.agent[i]

        elif content[0] == 'Over' or content == 'Skip':
            if gamedf.agent[i] != self.agentIdx:
                self.update_est(gamedf.agent[i],content[0])
        else:
            pass
    
    '''
    役職推定データを更新
    '''
    def update_est(self,i,text):
        for role in ['WEREWOLF', 'POSSESSED', 'SEER', 'VILLAGER']:
            self.roleEst.at[i,role] *= self.prob.at[text,role]

    def dayStart(self):
        self.divrepo = False
        self.gamefin = False
        self.dayGreeting = False

    def finish(self):
        if self.gamefin == False:
            self.gamefin = True
            print(self.base_info['myRole'] ,self.base_info['statusMap'][str(self.agentIdx)],flush=True)
            if self.base_info['myRole'] == 'WEREWOLF' and self.base_info['statusMap'][str(self.agentIdx)] == 'ALIVE':
                self.lastGame = 'win'
            elif self.base_info['statusMap'][str(self.agentIdx)] == 'DEAD':
                self.lastGame = 'lose'

    '''
    推定結果に応じて行動を選択する
    '''
    def action(self, cb, act):
        # print(act)
        if act == 'talk':
            # 0日目
            if self.base_info['day'] == 0:
                return cb.over()
            
            # 1日目
            elif self.base_info['day'] == 1:
                if self.base_info['myRole'] == 'WEREWOLF':
                    if self.divdlist[self.agentIdx][:8] == 'WEREWOLF' and self.coedlist[self.agentIdx] == '':
                        self.coedlist[self.agentIdx] = 'VILLAGER'
                        return cb.comingout(self.agentIdx, 'VILLAGER')
                    elif self.divdlist[self.agentIdx][:8] == 'WEREWOLF' and self.esttalk1 == False and self.maybeseer != None:
                        self.esttalk1 = True
                        self.estlist[self.agentIdx] = 'WEREWOLF'
                        return cb.estimate(self.maybeseer,'WEREWOLF')
                    elif self.maybepossessed != None and self.esttalk2 == False: 
                        self.esttalk2 = True
                        return cb.estimate(self.maybepossessed,'SEER')
                    else:
                        return cb.skip()
                
                if self.base_info['myRole'] == 'VILLAGER':
                    if self.divdlist[self.agentIdx][:8] == 'WEREWOLF' and self.coedlist[self.agentIdx] == '':
                        self.coedlist[self.agentIdx] = 'VILLAGER'
                        return cb.comingout(self.agentIdx, 'VILLAGER')
                    elif self.esttalk1 == False and self.maybepossessed != None:
                        self.esttalk1 = True
                        return cb.estimate(self.maybepossessed , 'POSSESSED')
                    else:
                        return cb.skip()
                
                elif self.base_info['myRole'] == 'POSSESSED':
                    #if self.seeridx is not None:
                        if self.coedlist[self.agentIdx] == '':
                            self.coedlist[self.agentIdx] = 'SEER'
                            return cb.comingout(self.agentIdx, 'SEER')
                        elif self.divrepo == False:
                            for i in self.idxlist:
                                if self.divdlist[i][:8] == 'WEREWOLF':
                                    while True:
                                        j = random.choice(self.idxlist)
                                        #if j == i and j != self.agentIdx:
                                        #    self.divrepo = True
                                        #    return cb.divined(j,'HUMAN')
                                        if j != i and j != self.agentIdx and j != self.probably('SEER'):
                                            self.divrepo = True
                                            self.liedividx = j
                                            return cb.divined(j,'WEREWOLF')
                                elif self.divdlist[i][:8] == 'HUMAN':
                                    while True:
                                        j = random.choice(self.idxlist)
                                        if j != self.probably('WEREWOLF') and j != self.probably('SEER') and j != self.agentIdx:
                                            self.divrepo = True
                                            self.liedividx = j
                                            return cb.divined(j,'WEREWOLF')
                            return cb.skip()
                        elif self.esttalk1 == False:
                            for i in self.idxlist:
                                if self.coedlist[i] == 'SEER' and i != self.agentIdx:
                                    self.esttalk1 = True
                                    return cb.estimate(i,'POSSESSED')
                            return cb.skip()
                        elif self.esttalk2 == False:
                            for i in self.idxlist:
                                if self.coedlist[i] == 'WEREWOLF' and i != self.agentIdx and i != self.liedividx:
                                    self.esttalk2 = True
                                    return cb.estimate(i,'VILLAGER')
                            return cb.skip()
                        else:
                            return cb.skip()
                    #else:
                    #    return cb.skip()
                
                elif self.base_info['myRole'] == 'SEER':
                    if True: # self.seeridx is not None:
                        if self.coedlist[self.agentIdx] == '':
                            self.coedlist[self.agentIdx] = 'SEER'
                            return cb.comingout(self.agentIdx, 'SEER')
                        elif self.divrepo == False:
                            self.divrepo = True
                            d = self.divresult.split()
                            if d[2] == 'WEREWOLF':
                                self.foundwolf = int(d[1][6:8])      
                                # 後追加するなら
                                # ・初日占い先が占いCOした時の分岐
                            elif d[2] == 'HUMAN':
                                self.foundhuman = int(d[1][6:8])

                            #if self.coedlist[int(d[1][6:8])] != 'SEER':
                            #    return cb.divined(int(d[1][6:8]),d[2])
                            #elif self.coedlist[int(d[1][6:8])] == 'SEER':
                            #    if d[2] == 'HUMAN':
                            #        i = random.choice(self.idxlist)
                            #        if i != int(d[1][6:8]) and self.divdlist[i] != 'WEREWOLF' and i == self.probably('WEREWOLF'):
                            #            return cb.divined(i,'WEREWOLF')
                            #    elif d[2] == 'WEREWOLF':
                            #        return cb.divined(int(d[1][6:8]),d[2])
                            return cb.divined(int(d[1][6:8]),d[2])       
                        elif self.esttalk1 == False:
                            for i in self.idxlist:
                                if self.coedlist[i] == 'SEER' and i != self.agentIdx :
                                    self.esttalk1 = True
                                    if i != self.foundwolf:
                                        return cb.estimate(i,'POSSESSED')
                                    else:
                                        return cb.estimate(i,'WEREWOLF')
                            return cb.skip()
                        elif self.esttalk2 == False:
                            for i in self.idxlist:
                                if self.divdlist[i] == 'WEREWOLF' and self.divdlist[i] != self.foundwolf:
                                    self.esttalk2 = True
                                    return cb.estimate(i,'VILLAGER')
                            return cb.skip()
                        else:
                            return cb.skip()
                    else:
                        return cb.skip()
                else:
                    return cb.skip()
            
            # 2日目
            else:
                if self.base_info['myRole'] == 'SEER' and self.coedlist[self.agentIdx] != 'WEREWOLF' and self.coedlist[self.agentIdx] != 'POSSESSED':
                    if self.divrepo == False:
                        self.divrepo = True
                        d = self.divresult.split()
                        return cb.divined(int(d[1][6:8]),d[2])
                    # elif self.base_info['statusMap'][str(self.probably('POSSESSED'))] == 'ALIVE':
                    #     self.coedlist[self.agentIdx] = 'WEREWOLF'
                    #     return cb.comingout(self.agentIdx, 'WEREWOLF')
                    # else:
                    #     self.coedlist[self.agentIdx] = 'POSSESSED'
                    #     return cb.comingout(self.agentIdx, 'POSSESSED')
                    else:
                        return cb.skip()
                
                elif self.base_info['myRole'] == 'POSSESSED' and self.coedlist[self.agentIdx] != 'POSSESSED' :
                    self.coedlist[self.agentIdx] = 'POSSESSED'
                    return cb.comingout(self.agentIdx, 'POSSESSED')

                elif self.base_info['myRole'] == 'WEREWOLF':
                    for i in self.idxlist:
                        if self.coedlist[i] == 'POSSESSED' and i != self.agentIdx and self.possessedCO == None and i == self.maybepossessed:
                            self.possessedCO = i
                            return cb.comingout(self.agentIdx, 'WEREWOLF')
                        else:
                            break
                    if self.divdlist[self.agentIdx][:8] == 'WEREWOLF' and self.coedlist[self.agentIdx] == '':
                        self.coedlist[self.agentIdx] = 'VILLAGER'
                        return cb.comingout(self.agentIdx, 'VILLAGER')
                    elif self.divdlist[self.agentIdx][:8] == 'WEREWOLF' and self.esttalk1 == False:
                        self.esttalk1 = True
                        self.estlist[self.agentIdx] = 'WEREWOLF'
                        return cb.estimate(self.seeridx,'WEREWOLF')
                    else:
                        return cb.skip()
                
                elif self.base_info['myRole'] == 'VILLAGER' and self.coedlist[self.agentIdx] != 'WEREWOLF' and self.coedlist[self.agentIdx] != 'POSSESSED':
                    # if self.base_info['statusMap'][str(self.probably('POSSESSED'))] == 'ALIVE':
                    #     self.coedlist[self.agentIdx] = 'WEREWOLF'
                    #     return cb.comingout(self.agentIdx, 'WEREWOLF')
                    # else:
                    #     self.coedlist[self.agentIdx] = 'POSSESSED'
                    #     return cb.comingout(self.agentIdx, 'POSSESSED')
                    if self.divdlist[self.agentIdx][:8] == 'WEREWOLF' and self.coedlist[self.agentIdx] == '':
                        self.coedlist[self.agentIdx] = 'VILLAGER'
                        return cb.comingout(self.agentIdx, 'VILLAGER')
                    else:
                        return cb.skip()

                else:
                    return cb.skip()
        
        elif act == 'vote':
            if self.base_info['myRole'] == 'WEREWOLF':
                p = self.probably('POSSESSED')                
                for i in self.idxlist:
                    if self.base_info['day'] == 2 and (self.maybepossessed != None or self.possessedCO != None):
                        if i != self.agentIdx and i != self.maybepossessed and i != self.possessedCO:
                            return i
                    elif (self.divdlist[i] == 'WEREWOLF' or self.divdlist[i] != 'WEREWOLF_EX') and i != self.agentIdx and i != p:
                        return i
                    elif self.divdlist[i] == 'HUMAN' or self.divdlist[i] == 'HUMAN_EX':
                        if i != p and i != self.agentIdx and i != p:
                            return i
                while True:
                    i = random.choice(self.idxlist)
                    if i != p:
                        return i
            elif self.base_info['myRole'] == 'POSSESSED':
                p = self.probably('WEREWOLF')
                while True:
                    i = random.choice(self.idxlist)# 修正　自分の占い結果はdivd にはいっているか？
                    if self.base_info['day'] == 1:
                        if (self.divdlist[i] != 'WEREWOLF' or self.divdlist != 'WEREWOLF_EX') and i != p and i != self.agentIdx:
                            return i
                    elif self.base_info['day'] == 2:
                        if self.coedlist[i] != 'WEREWOLF' and i != p and i != self.agentIdx:
                            return i
                    
                    if i != p and i != self.agentIdx:
                        return i
            elif self.base_info['myRole'] == 'SEER':
                if self.foundwolf != None:
                    return self.foundwolf
            #   elif 'WEREWOLF_EX' in self.divdlist:
            #       for i in self.idxlist:
            #           if self.divdlist[i] == 'WEREWOLF_EX' and i != self.agentIdx:
            #               return i
            #    elif 'WEREWOLF' in self.divdlist or self.divdlist != 'WEREWOLF_EX':
            #        for i in self.idxlist:
            #           if (self.divdlist[i] == 'WEREWOLF' or self.divdlist[i] != 'WEREWOLF_EX') and i != self.agentIdx and i == self.foundwolf:
            #                return i
                for i in self.idxlist:
                    if i == self.probably('WEREWOLF') and i != self.foundhuman and i != self.agentIdx:
                        return i
                for i in self.idxlist:
                    if i != self.foundhuman and i != self.agentIdx:
                        return i
            elif self.base_info['myRole'] == 'VILLAGER':
                for i in self.idxlist:
                    if self.divdlist[i] == 'WEREWOLF_EX' and i != self.agentIdx:
                            return i
                for i in self.idxlist:
                        if self.divdlist[i] == 'WEREWOLF'  and i != self.agentIdx and i == self.probably('WEREWOLF'):
                            return i
                for i in self.idxlist:
                        if self.divdlist[i] == 'PANDA' and i != self.agentIdx and i == self.probably('WEREWOLF'):
                            return i
                return self.probably('WEREWOLF')
        elif act == 'divine':
            if self.base_info['day'] == 0:
                while True:
                    i = random.choice(self.idxlist)
                    if i != self.agentIdx:
                        return i
            else:
                if self.foundwolf != None:
                    while True:
                        i = random.choice(self.idxlist)
                        if i != self.agentIdx and i != self.foundwolf:
                            return i
                elif self.foundhuman != None:
                    while True:
                        i = random.choice(self.idxlist)
                        if i != self.agentIdx and i != self.foundwolf and i != self.foundhuman:
                            return i
                else:
                    while True:
                        i = random.choice(self.idxlist)
                        if i != self.agentIdx :
                            return i

                
        
        elif act == 'attack':
            #　while True:
            #    i = random.choice(self.idxlist)
            #    if i != self.agentIdx and i != self.probably('POSSESSED'):
            #        return i
            if self.base_info['day'] == 1:
                if self.maybepossessed != None:
                    if 'HUMAN' in self.divdlist or 'HUMAN_EX' in self.divdlist:
                        for i in self.idxlist:
                            if (self.divdlist[i] == 'HUMAN' or self.divdlist[i] == 'HUMAN_EX') and i != self.maybepossessed:
                                return i
                    else:
                        while True:
                            i = random.choice(self.idxlist)
                            if i != self.maybepossessed and self.probably('POSSESSED'):
                                return i
                elif 'HUMAN' in self.divdlist or 'HUMAN_EX' in self.divdlist:
                    for i in self.idxlist:
                        if (self.divdlist[i] == 'HUMAN' or self.divdlist[i] == 'HUMAN_EX') and i != self.probably('POSSESSED'):
                            return i
                else:
                    return self.probably('SEER')            
            elif self.base_info['day'] == 2:
                if self.maybeseer != None:
                    for i in self.idxlist:
                        if i == self.maybeseer:
                            return i
                elif self.maybepossessed != None:
                    for i in self.idxlist:
                        if i != self.maybepossessed:
                            return i
                else:
                    #p = self.probably('POSSESSED')
                    #for i in self.idxlist:
                    #    if i != p and i == self.agentIdx:
                    #        return i
                    return self.probably('SEER')  


    def probably(self,role):
        return self.roleEst.idxmax()[role]