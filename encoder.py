import random
import string

#아스키코드에서 65~90: 대문자
# ' '는 27번째, .은 28번째
# 원하는 table 모양 notch는 회전자 목적, value는 변환목적

ref  = list('.RGEDYCUXZTSNMV WBLKHOQIFJPA')

#setting: 회전판 순서, 회전판 초기 세팅, [플러그보드 설정]
def setting(key=False,plugNum=False):
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
    
    if(key):
        roter = toSet(key)['roter']
        plug = toSet(key)['plug']
    
    else:
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
        # roter.append({'order': 4,'prime':10})
        # roter.append({'order': 6,'prime':10})
        # roter.append({'order': 3,'prime':27})

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

#setting값을 key형태로 암호화
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

def toSet(key):
    #key를 앞 8개와 나머지로 쪼개고, 각각 10진법화 한다. 그 이후 앞 8자리는 그대로 회전자 데이터, 뒤에 남은 데이터는 그대로 플러그보드값
    roter_key = key[0:8]
    plug_key = key[8:]
    roter_list = list()
    plug_list =list()
    
    roter = str(int(roter_key,base=16))
    
    for i in range(0,3):
        buffer = roter[i*3:(i+1)*3]
        roter_list.append({'order': int(buffer[0]),'prime': int(buffer[1:3])})

    if(plug_key):
        plug = str(int(plug_key,base=16))

        if(len(plug)%2 == 1):
            plug = '0'+plug

        for i in range(0,len(plug)//2):
            buffer = int(plug[i*2:(i+1)*2]) + 65
            
            plug_list.append(chr(buffer))

    

    set = {
        'roter': roter_list,
        'plug': plug_list
    }
    return set 
#플러그보드 대입
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

#반사된 회전자
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

#회전자 메카니즘
def mech(msg,tables,roters):
    use = list()
    data = msg

    #use 리스트에 초기값 저장
    for roter in roters:
        index = roter['order'] - 1
        buffer = tables[index]['value']
        
        #notch를 찾기 편하게 알파벳으로 치환
        notch = tables[index]['notch']
        no_char = buffer[int(notch)-1]

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

    return code

#인코딩(플러그보드 + 회전자 + 반사판)
def encoding(msg, key=False):

    if(key):
        set = key
    else:
        set = setting(plugNum=1)
    data = list(msg)

    # print(set)

    data = plugBoard(data,set['plug'])

    data = mech(data, set['table'],set['roter'])

    data = plugBoard(data,set['plug'])

    value= ''.join(s for s in data)
    code_key = toKey(set)

    code = (value+'/'+code_key)

    return code

#예시
# msg = 'KIM CHANG HO'
# print(msg + '를 변환합니다.')

# set = setting(plugNum=1)
# code = encoding(msg, set)
# print('========암호화 결과========')
# print('암호문= ' + code)

# msg = list(code.split('/'))

# test_code = encoding(msg[0],setting(key = msg[1]))

# print('========복호화 결과========')
# print('문장= ' + test_code)