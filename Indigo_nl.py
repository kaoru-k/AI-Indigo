import aiwolfpy

myname = 'Indigo'

import aiwolfpy.Indigo

class SampleAgent(object):
    
    def __init__(self, agent_name):
        # myname
        self.myname = agent_name
        self.agent = aiwolfpy.Indigo.Agents5_nl()
        
    def getName(self):
        return self.myname
    
    def initialize(self, base_info, diff_data, game_setting):
        self.base_info = base_info
        # game_setting
        self.game_setting = game_setting
        # print(base_info)
        # print(diff_data)
        self.agent.initialize(base_info, game_setting)
        
    def update(self, base_info, diff_data, request):
        self.base_info = base_info
        # print(base_info)
        # print(diff_data)
        self.agent.update(base_info,diff_data,request)
        
    def dayStart(self):
        self.agent.dayStart()
        return None
    
    def talk(self):
        return self.agent.action('talk')
    
    def whisper(self):
        return 'Over'
        
    def vote(self):
        return self.agent.action('vote')
    
    def attack(self):
        return self.agent.action('attack')
    
    def divine(self):
        return self.agent.action('divine')
    
    def guard(self):
        return self.base_info['agentIdx']
    
    def finish(self):
        self.agent.finish()
        return None

agent = SampleAgent(myname)
# run
if __name__ == '__main__':
    aiwolfpy.connect_parse(agent)
    