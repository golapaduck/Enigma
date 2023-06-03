import time
import os


def today():
    t =  time.localtime()

    date = '{:04}-{:02}-{:02}'.format(t.tm_year,t.tm_mon,t.tm_mday)

    return date


def getDate(path):
    fileList = os.listdir(path)
    txtList = list(file for file in fileList if 'tables' not in file)

    codeList = dict()

    for name in txtList:
        filePath = f'{path}/{name}'
        lines = list()

        #파일을 열고, 각 라인(암호)를 리스트 형태로 저장
        with open(filePath, "r") as f:

            while(True):
                line = f.readline()
                if not line:
                    break
                # 라인별 \n 삭제 후 추가
                lines.append(line.split('\n')[0])

                
        code = {name[0:10]: lines}
        codeList.update(code)

    return codeList

def fileReader():
    dataList = getDate('./database')

    dataKey = dataList.keys()
    date = today()
    
    new = dict()
    old = dict()
    for key in dataKey:
        if key == date:
            new.update({'value':dataList[key]})
            new.update({'date':key})
        else:
            old.update({key:dataList[key]})
    if new == {}:
        new.update({'date':today()})
        new.update({'value':list()})
    return {'new':new, 'old':old}

def fileWriter(text):
    filePath = f'./database/{today()}.txt'
    
    with open(filePath,'w') as f:
        for i in range(0,len(text)):
            data = text[i]
            f.write(f'{data}\n')

# print(fileReader())