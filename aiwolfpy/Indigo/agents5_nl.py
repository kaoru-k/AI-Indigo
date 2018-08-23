from . import agents5_base
from . import GetSudachiOut
from . import contentbuilder_nl as cb

class Agents5_nl(agents5_base.Agents5_base):
    def __init__(self):
        super().__init__()
        self.ma = GetSudachiOut.GetSudachiOut()
        self.firstGame = True

    def initialize(self, base_info, game_setting):
        super().initialize(base_info, game_setting)
        self.ma.initialize(self.idxlist)
    
    def update(self,base_info, diff_data, request):
        super().update(base_info, diff_data, request)
        self.update_data(diff_data)
    
    '''
    ゲームデータを更新
    '''
    def update_data(self, gamedf):
        # print(gamedf.type[i])
        # read log
        for i in range(gamedf.shape[0]):
            # print(gamedf.type[i])
            # vote
            if gamedf.type[i] == 'vote' and gamedf.turn[i] == 0:
                pass
            # execute
            elif gamedf.type[i] == 'execute':
                pass
            # attacked
            elif gamedf.type[i] == 'dead':
                pass
            # talk
            elif gamedf.type[i] == 'talk':
                text = []
                if gamedf.text[i] == 'Over':
                    text.append('Over')
                elif gamedf.text[i] == 'Skip':
                    text.append('Skip')
                else:
                    text = self.ma.txt2Aiwp(gamedf.agent[i],gamedf.text[i])
                
                for t in text:
                    print(gamedf.agent[i], gamedf.text[i], '->', t)
                    super().read_talklog(gamedf, i, t)
    
    '''
    推定結果に応じて行動を選択する
    '''
    def action(self,act):
        # print(act)
        if act == 'talk' and self.base_info['day'] == 0 and self.firstTalk == False:
            self.firstTalk = True
            self.dayGreeting = True
            if self.firstGame == True:
                self.firstGame = False
                mode = 0
            elif self.lastGame == 'lose':
                self.lastGame = 'newtral'
                mode = 1
            elif self.lastGame == 'win':
                self.lastGame = 'newtral'                
                mode = 2
            else:
                mode = 3
            return cb.firstGreeting(mode)
        # 返信を最優先
        elif act == 'talk' and self.talkFrom != -1:
            if self.talkContent[0] == 'Skip':
                text = cb.reply(self.talkFrom, 'skip')
            else:
                text = cb.reply(self.talkFrom, 'est')
            self.talkFrom = -1
            self.talkContent = ''
            return text
        
        elif act == 'talk' and self.dayGreeting == False and self.base_info['myRole'] != 'POSSESSED' and self.base_info['myRole'] != 'SEER':
            self.dayGreeting = True
            return cb.greeting(self.base_info['day'])
        else:
            return super().action(cb, act)
