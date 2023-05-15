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
            'value': line.split()[0],
            'notch': line.split()[1]
        }

        tables.append(table)
    f.close()
    
    #roter 세팅
    roter = list()

    for i in range(3):
        order= random.randint(1,8) #중복 생길 수 있음
        prime= random.randint(1,25)
        roter.append({'order':order, 'prime': prime})

    #plug 세팅
    plug = list()

    if(plugNum > 0):
        rand = random.sample(string.ascii_uppercase,plugNum*2)
        for i in range(plugNum):
            plug.append(''.join(s for s in rand[i*2:i*2+2]))
    

    setting ={
        'tables': tables,
        'roter': roter,
        'plug': plug,
    }

    return setting


def encoding(msg, setting):
    
    roters = parser(roter)
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
print(Setting(2))