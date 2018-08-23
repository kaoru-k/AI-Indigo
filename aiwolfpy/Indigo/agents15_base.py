import pandas as pd
import random

class Agents15_base(object):
    def __init__(self):
        self.prob = pd.read_csv('result_prob15.csv',index_col='VERB')
        self.roleEst = pd.DataFrame(
            {'WEREWOLF': [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0],
            'POSSESSED': [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0],
            'SEER'     : [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0],
            'VILLAGER' : [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0],
            'MEDIUM'   : [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0],
            'BODYGUARD': [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]},
            columns = ['WEREWOLF','POSSESSED','SEER','VILLAGER','MEDIUM','BODYGUARD'],
            index = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

    def initialize(self, base_info, game_setting):
        self.game_setting = game_setting
        self.base_info = base_info
        self.agentIdx = self.base_info['agentIdx']
        self.idxlist = []
        for k in base_info['statusMap'].keys():
            self.idxlist.append(int(k))
        self.roleEst = pd.DataFrame(
            {'WEREWOLF': [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0],
            'POSSESSED': [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0],
            'SEER'     : [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0],
            'VILLAGER' : [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0],
            'MEDIUM'   : [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0],
            'BODYGUARD': [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]},
            columns = ['WEREWOLF','POSSESSED','SEER','VILLAGER','MEDIUM','BODYGUARD'],
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
        
        self.firstTalk = False # 初日の挨拶をしたかどうか
        self.esttalk = False   # ESTIMATE発言をしたかどうか
        self.seeridx = None    # 占い結果を報告した人の番号
        self.divdidx = None    # DIVINEDしてきたプレイヤー番号 
        self.divrepo = False   # 占い結果を報告したかどうか
        self.divresult = ''    # 占い結果
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
                        self.divresult = 'divine Agent[' + '{0:02d}'.format(i) + '] HUMAN'
                        break

        self.base_info = base_info
        # print(base_info)

    def read_talklog(self, gamedf, i, t):
        content = t.split()
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

    def finish(self):
        if self.gamefin == False:
            self.gamefin = True
            print(self.base_info['myRole'] ,self.base_info['statusMap'][str(self.agentIdx)],flush=True)

    '''
    推定結果に応じて行動を選択する
    '''
    def action(self, cb, act):
        # print(act)
        if act == 'talk':
            return 'Skip'
        
        elif act == 'vote':
            while True:
                i = random.choice(self.idxlist)
                if i != self.agentIdx:
                    return i
        
        elif act == 'whisper':
            while True:
                i = random.choice(self.idxlist)
                if i != self.agentIdx:
                    return i
        
        elif act == 'guard':
            while True:
                i = random.choice(self.idxlist)
                if i != self.agentIdx:
                    return i

    def probably(self,role):
        return self.roleEst.idxmax()[role]