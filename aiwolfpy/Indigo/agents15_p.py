from . import agents15_base
from . import GetSudachiOut
from . import contentbuilder as cb

class Agents15_p(agents15_base.Agents15_base):
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
                pass
    
    '''
    推定結果に応じて行動を選択する
    '''
    def action(self,act):
        return super().action(cb, act)