import random

role2nl = {
    'WEREWOLF' : '人狼',
    'POSSESSED': '狂人',
    'SEER'     : '占い師',
    'VILLAGER' : '村人'
}
speci2nl = {
    'HUMAN'   : '人間',
    'WEREWOLF': '人狼'
}

def firstGreeting(mode):
    if mode == 0:
        r = random.randrange(2)
        if r == 0:
            text = 'みなさんはじめまして、徳島出身のIndigoです。よろしくね。'
        else:
            text = 'こんにちは、手加減はしないよ。'
    elif mode == 1:
        r = random.randrange(3)
        if r == 0:
            text = 'おはようございます。今回は最後まで生き延びたいな。'
        elif r == 1:
            text = 'こんにちは。人狼ゲームって難しいよね。'
        else:
            text = 'こんにちは。今度はだまされないぞ。'
    elif mode == 2:
        r = random.randrange(2)
        if r == 0:
            text = 'さて、連勝目指して頑張るぞ。'
        else:
            text = 'こんにちは、だんだん人狼分かってきた。'
    else:
        r = random.randrange(2)
        if r == 0:
            text = 'こんにちは、頑張るぞ。'
        else:
            text = 'こんにちは、今回も頑張るぞ。'
    return text

def greeting(day):
    r = random.randrange(3)
    if r == 0:
        text = 'おはよう。{}日目だね。'.format(day)
    elif r == 1:
        text = '{}日目の朝だね。'.format(day)
    else:
        text = '夜が明けたね'
    return text


# 2.1
def estimate(target, role):
    #return 'ESTIMATE Agent[' + "{0:02d}".format(target) + '] ' + role
    mode = random.randrange(4)
    if mode == 0:
        text = 'Agent[' + "{0:02d}".format(target) + ']が' + role2nl.get(role) + 'だと思うよ。'
    elif mode == 1:
        text = 'Agent[' + "{0:02d}".format(target) + ']が' + role2nl.get(role) + 'だと思うけどなぁ。'
    elif mode == 2:
        text = 'Agent[' + "{0:02d}".format(target) + ']が' + role2nl.get(role) + 'な気がする。'
    elif mode == 3:
        text = 'Agent[' + "{0:02d}".format(target) + ']が' + role2nl.get(role) + 'じゃないかな。'    

    return text

def comingout(target, role):
    #return 'COMINGOUT Agent[' + "{0:02d}".format(target) + '] ' + role
    #return 'Agent[' + "{0:02d}".format(target) + ']は' + role + 'です。'
    mode = random.randrange(4)
    if mode == 0:
        text = '私は' + role2nl.get(role) + 'だよ。'
    else:
        text = '私、' + role2nl.get(role) + 'COします。'
    
    return text

# 2.2
def divine(target):
    #return 'DIVINE Agent[' + "{0:02d}".format(target) + ']'
    return 'Agent[' + "{0:02d}".format(target) + ']を占うよ。'

# 5人村なので狩人はいない
#def guard(target):
#    return 'GUARD Agent[' + "{0:02d}".format(target) + ']'
    
def vote(target):
    #return 'VOTE Agent[' + "{0:02d}".format(target) + ']'
    return 'Agent[' + "{0:02d}".format(target) + ']に投票するよ。'

def attack(target):
    #return 'ATTACK Agent[' + "{0:02d}".format(target) + ']'
    return 'Agent[' + "{0:02d}".format(target) + ']を襲撃するよ。'

# 2.3
def divined(target, species):
    #return 'DIVINED Agent[' + "{0:02d}".format(target) + '] ' + species
    return 'Agent[' + "{0:02d}".format(target) + ']' + 'の占い結果は' + speci2nl.get(species) + 'だったよ。'

# 5人村なので霊能者はいない
#def identified(target, species):
#    return 'IDENTIFIED Agent[' + "{0:02d}".format(target) + '] ' + species

# 5人村なので狩人はいない
#def guarded(target):
#    return 'GUARDED Agent[' + "{0:02d}".format(target) + ']'

# 2.4
def agree(day, id):
    #return 'AGREE '+ talktype + ' day' + str(day) + ' ID:' + str(id)
    return str(day) + '日めの' + str(id) + '番目の発言に同意するよ。'

def disagree(day, id):
    #return 'DISAGREE '+ talktype + ' day' + str(day) + ' ID:' + str(id)
    return str(day) + '日めの' + str(id) + '番目の発言には同意しないね。'

# 2.5
# skipはそのまま使える
def skip():
    return 'Skip'

# overはそのまま使える
def over():
    return 'Over'

# 3
# requestはだいぶ手を加える必要があるのでとりあえずコメントアウト
#def request(text):
#    return 'REQUEST(' + text + ''

def reply(target, text):
    if text == 'Skip':
        r = random.randrange(3)
        if r == 0:
            text = 'Agent[{num:02}]さんの言ってることがよくわからないなぁ。'.format(num=target)
        elif r == 1:
            text = 'もう一度言ってもらえるかな？'
        else:
            text = 'うーん、どうしようかなぁ。'
    else:
        r = random.randrange(3)
        if r == 0:
            text = '今なんて言った？'
        elif r == 1:
            text = 'Agent[{num:02}]さんごめん、聞こえなかった。'.format(num=target)
        else:
            text = 'もう一度言って。'
    return '>>Agent[{num:02}] '.format(num=target) + text