import random
import string

#아스키코드에서 65~90: 대문자
# ' '는 27번째, .은 28번째
# 원하는 table 모양 notch는 회전자 목적, value는 변환목적

ref  = list('.RGEDYCUXZTSNMV WBLKHOQIFJPA')

#setting: 회전판 순서, 회전판 초기 세팅, [플러그보드 설정]

def setting(plugNum=False):
    #table 세팅
    tables = list()
    f = open('./tables.txt','r')
    

    while(True):
        line = f.readline()
        if not line:
            break

        value = list(line.split(',')[0])

        table ={
            'value': value,
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

    # test용
    # roter.append({'order': 8,'prime':23})
    # roter.append({'order': 3,'prime':3})
    # roter.append({'order': 5,'prime':1})

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
#회전자 대입
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

#회전자 회전
def notchFunc(table):
    old_table  = table
    new_table = list()

    
    for roter in old_table:
        rachet = roter['notch']
        first = roter['value'][0]

        buffer = roter['value']
        buffer.insert(0,buffer.pop())

        ready = {'value': buffer, 'notch' : rachet}

        new_table.append(ready)
        
        if(rachet != first):
            break
        else:
            continue

    count = 0

    for roter in new_table:
        old_table[count] = roter
        count = count + 1

    return old_table

def reverseFunc(table):
    old = table['value']
    notch = table['notch']
    val= list(0 for i in range(0,28))

    count = 65
    for value in old:
        
        if(value == ' '):
            buffer = 26
        elif(value == '.'):
            buffer = 27
        else:
            buffer = ord(value) - 65
        
        if(count<=90):
            val[buffer] = chr(count)
        elif(count == 91):
            val[buffer] = ' '
        elif(count == 92):
            val[buffer] = '.'

        count  = count +1
    
    new = {'value':val, 'notch': notch}

    return new

def mech(msg,tables,roters):
    use = list()
    data = msg

    #use 리스트에 초기값 저장
    for roter in roters:
        index = roter['order'] - 1
        buffer = tables[index]['value']
        
        #notch를 찾기 편하게 알파벳으로 치환
        notch = tables[index]['notch']
        no_char = buffer[int(notch)]

        #prime 값으로 table 재구축
        for i in range(roter['prime']):
            buffer.insert(0,buffer.pop())

        ready = {'value':buffer, 'notch': no_char}

        use.append(ready)

    #회전자 구동부분
    code = list(data)
    new = list()

    #회전자 1회 구동
    for word in code:
        newWord = word

        #회전자
        for table in use:
            newWord = roterFunc(newWord, table['value'])

        #반사판
        newWord = roterFunc(newWord,ref)

        #회전자 역방향
        rev_use = reversed(use)

        for table in rev_use:
            rev_table = reverseFunc(table)
            newWord = roterFunc(newWord, rev_table['value'])
        
        new.append(newWord)

        use = notchFunc(use)

    code = new


    data = code

    return data
        
def encoding(msg, setting):

    set = setting
    data = list(msg)

    print(set['roter'])
    print(set['plug'])

    # data = plugBoard(data,set['plug'])

    data = mech(data, set['table'],set['roter'])

    # data = plugBoard(data,set['plug'])

    return ''.join(s for s in data)

code = encoding('HELLO',setting(0))


print(code)