import time
import os


def today():
    timeData =  time.localtime()

    date = f'{timeData.tm_year}-{timeData.tm_mon}-{timeData.tm_mday}'

    return date

def fileManager(path):
    fileList = os.listdir(path)
    txtList = list(file for file in fileList if 'tables' not in file)

    codeList = list()

    for name in txtList:
        filePath = f'{path}/{name}'
        lines = list()

        #파일을 열고, 각 라인(암호)를 리스트 형태로 저장
        with open(filePath, "r") as f:

            while(True):
                line = f.readline()
                if not line:
                    break

                lines.append(line)
                
        code = {name: lines}
        codeList.append(code)



    return txtList


print(fileManager('./database'))