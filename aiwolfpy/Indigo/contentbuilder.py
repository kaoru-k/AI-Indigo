# 2.1
def estimate(target, role):
    return 'ESTIMATE Agent[' + "{0:02d}".format(target) + '] ' + role
    #return 'Agent[' + "{0:02d}".format(target) + ']' + 'が' + role + 'だと思う。'

def comingout(target, role):
    return 'COMINGOUT Agent[' + "{0:02d}".format(target) + '] ' + role
    #return 'Agent[' + "{0:02d}".format(target) + ']' + 'は' + role + 'です。'
    #return '私は' + role + 'です。'

# 2.2
def divine(target):
    return 'DIVINE Agent[' + "{0:02d}".format(target) + ']'
    #return 'Agent[' + "{0:02d}".format(target) + ']' + 'を占います。'

# 5人村なので狩人はいない
#def guard(target):
#    return 'GUARD Agent[' + "{0:02d}".format(target) + ']'

def vote(target):
    return 'VOTE Agent[' + "{0:02d}".format(target) + ']'
    #return 'Agent[' + "{0:02d}".format(target) + ']に投票します'

def attack(target):
    return 'ATTACK Agent[' + "{0:02d}".format(target) + ']'
    #return 'Agent[' + "{0:02d}".format(target) + ']を襲撃します'

# 2.3
def divined(target, species):
    return 'DIVINED Agent[' + "{0:02d}".format(target) + '] ' + species
    #return 'Agent[' + "{0:02d}".format(target) + '] ' + 'の占い結果は' + species + 'でした。'

# 5人村なので霊能者はいない
#def identified(target, species):
#    return 'IDENTIFIED Agent[' + "{0:02d}".format(target) + '] ' + species

# 5人村なので狩人はいない
#def guarded(target):
#    return 'GUARDED Agent[' + "{0:02d}".format(target) + ']'

# 2.4
def agree(talktype, day, id):
    return 'AGREE '+ talktype + ' day' + str(day) + ' ID:' + str(id)
    #return str(day) + '日めの' + str(id) + '番目の発言に同意します。'

def disagree(talktype, day, id):
    return 'DISAGREE '+ talktype + ' day' + str(day) + ' ID:' + str(id)
    #return str(day) + '日めの' + str(id) + '番目の発言に同意しません。'

# 2.5
# skipはそのまま使える
def skip():
    return 'Skip'

# overはそのまま使える
def over():
    return 'Over'

# 3
def request(text):
    return 'REQUEST(' + text + ''