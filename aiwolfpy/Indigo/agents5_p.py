from . import agents5_base
from . import GetSudachiOut
from . import contentbuilder as cb

class Agents5_p(agents5_base.Agents5_base):
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
                super().read_talklog(gamedf, i, gamedf.text[i])
    
    '''
    推定結果に応じて行動を選択する
    '''
    def action(self,act):
        return super().action(cb, act)