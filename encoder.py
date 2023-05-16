import random
import string

#아스키코드에서 65~90: 대문자
# ' '는 27번째, .은 28번째
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

def setting(plugNum=False):
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

        prime= random.randint(1,28)
        roter.append({'order':order, 'prime': prime})

    #plug 세팅
    plug = list()

    if(14 > plugNum > 0):
        plug = random.sample(string.ascii_uppercase,plugNum*2)
    elif(plugNum > 13):
        plug = random.sample(string.ascii_uppercase,26)

    #setting 선언
    setting ={
        'table': tables,
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

def plugBoard(msg, plug):
    count = 0
    plugs = plug
    data = msg

    for word in data:
        if(word in plugs):
            index = plugs.index(word)

            if(index%2==1):
                data[count] = plugs[index-1]
            else:
                data[count] = plugs[index+1]
        count = count + 1
    
    return data

def roterFunc(word,table):
    data = word
    buffer = table

    if(data == ' '):
        data = buffer[26]
    elif(data == '.'):
        data = buffer[27]
    else:
        index = ord(data) - 65
        data = buffer[index]
    return data

def mech(msg,tables,roters):
    use = list()
    data = msg

    #use 리스트에 초기값 저장
    for roter in roters:
        index = roter['order'] - 1
        buffer = list(tables[index]['value'])
        
        #notch를 찾기 편하게 알파벳으로 치환
        notch = tables[index]['notch']
        no_char = buffer[int(notch)]

        #prime 값으로 table 재구축
        for i in range(roter['prime']):
            buffer.insert(0,buffer.pop())

        ready = {'table':buffer, 'notch': no_char}

        use.append(ready)

    #회전자 구동부분
    code = list(data)
    new = list()

    #회전자 1회 구동
    for word in code:
        newWord = word

        for table in use:
            newWord = roterFunc(newWord, table['table'])
        
        new.append(newWord)
        
        

    code = new


    data = ''.join(s for s in code)

    return data
        
def encoding(msg, setting):
    
    set = setting
    data = list(msg)
    
    #print(set)

    data = plugBoard(data,set['plug'])

    print(mech(msg, set['table'],set['roter']))

    #return ''.join(s for s in data)

code = encoding('HELLO',setting(4))

print(code)