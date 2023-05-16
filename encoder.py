import random
import string

#아스키코드에서 65~90: 대문자, 97~122: 소문자
# 원하는 table 모양notch는 회전자 목적, value는 변환목적

# tables =[
#     {'value':'EKMFLGDQVZNTOWYHXUSPAIBRCJ','notch':1},
#     {'value':'AJDKSIRUXBLHWTMCQGZNPYFVOE','notch':3},
#     {'value':'BDFHJLCPRTXVZNYEIWGAKMUSQO','notch':9},
#     {'value':'ESOVPZJAYQUIRHXLNFTGKDCMWB','notch':7},
#     {'value':'VZBRGITYUPSDNHLXAWMJQOFECK','notch':8},
#     {'value':'JPGVOUMFYQBENHZRDKASXLICTW','notch':4},
#     {'value':'NZJHGRCXMYSWBOUFAIVLPEKQDT','notch':6},
#     {'value':'FKQHTLXOCBJSPDZRAMEWNIUYGV','notch':2}
# ]


def parser(key):
    key_list = list()
    key_data = key
    
    while(key_data > 0):
        key_list.append(key_data%10)
        key_data = key_data //10

    return key_list

#setting: 회전판 순서, 회전판 초기 세팅, [플러그보드 설정]

def Setting(plugNum=False):
    #table 세팅
    tables = list()
    f = open('./tables.txt','r')
    

    while(True):
        line = f.readline()
        if not line:
            break

        table ={
            'value': line.split(',')[0],
            'notch': line.split(',')[1]
        }

        tables.append(table)
    f.close()
    
    #roter 세팅
    roter = list()
    buffer =list()

    for i in range(3):
        order = random.randint(1,8)
        while(order in buffer):
            order = random.randint(1,8)
        buffer.append(order)

        prime= random.randint(1,26)
        roter.append({'order':order, 'prime': prime})

    #plug 세팅
    plug = list()

    if(plugNum > 0):
        plug = random.sample(string.ascii_uppercase,plugNum*2)

    #setting 선언
    setting ={
        'tables': tables,
        'roter': roter,
        'plug': plug,
    }

    return setting

def toKey(setting):
    roters = setting['roter']
    plugs = setting['plug']

    origin = 0
    for roter in roters:
        origin = origin*1000 + roter['order']*100 + roter['prime']

    key = str(hex(origin)).lstrip('0x')

    if(len(key) <8):
        key = '0' + key

    origin = str()

    if(len(plugs) != 0):
        for plug in plugs:
            index = ord(plug) - 65
            if(index < 10):
                origin = origin + '0' + str(index)
            else:
                origin = origin + str(index)

        key = key + str(hex(int(origin))).lstrip('0x')
    
    return key


def encoding(msg, setting):


    data = list(msg)

    for roter in roters:
        code = data
        table = list(tables[roter]['value'])
        for i in range(len(code)):
            if(code[i] ==' '):
                continue
            else:
                index = ord(code[i]) - 65
                if(index <= 25):
                    code[i] = table[index]
                else:
                    code[i] = table[index - 32].lower()
        data = code
    
    print(data)


#encoding('test Text',1)
print(Setting(1))