import socket
import signal
import threading

import module.database as db
import module.encoder as en

HOST = ''
PORT = 9150
MODE = [0,1,2]


code_list = db.fileReader()
new = code_list['new']

ids = list()

def upload(conn, id):
    print(f'user{id}: 업로드')

    while True:
        data = conn.recv(1024).decode('utf-8')
        try:
            data = data.upper()
            msg = en.encoding(data)
            conn.sendall(msg.encode('utf-8'))
            new['value'].append(msg)
            print(f'user{id}: 업로드 {msg}')
            db.fileWriter(new['value'])
            print(f'데이터 저장...')
                        
            break
        except:
            conn.sendall(f'재송신/'.encode('utf-8'))
            continue

def download(conn,id):

    dateList = list(code_list['old'].keys())
    days = ""
    for date in dateList:
        days += f"{date +'/'}"
    days +=f"{new['date']}"
    conn.sendall(f'{days}'.encode('utf-8'))
    print(f'user{id}: 다운로드')

    setDate = conn.recv(1024).decode('utf-8')
    
    if setDate in list(code_list['old'].keys()):
        dataList = code_list['old'][setDate]
        codes = len(dataList)
    elif setDate == new['date']:
        dataList = code_list['new']['value']
        codes =  len(dataList)
    
    conn.sendall(str(codes).encode('utf-8'))
        
    index = conn.recv(1024).decode('utf-8')
    
    conn.sendall(f"{dataList[int(index)]}".encode('utf-8'))
    print(f"user{id}: 다운로드 {dataList[int(index)]}")
    
def runClient(conn,id):
    print(f"user{id}가 접속하였습니다.")
    while True:
        code_list = db.fileReader()
        new = code_list['new']
        
        try:
            code = conn.recv(1024).decode('utf-8')
        except ConnectionResetError:
            print(f'user{id}가 강제로 종료되었습니다.')
            break
        else:
            if code == '0' or code == '종료':
                print(f'user{id} 종료')
                break
                
            elif code == '1' or code == '업로드':
                t= threading.Thread(target=upload,args=(conn,id))
                t.daemon = True
                t.start()
                t.join()
                
            elif code == '2' or code == '다운로드':
                t= threading.Thread(target=download,args=(conn,id))
                t.daemon = True
                t.start()
                t.join()

    if conn in ids:
        ids.remove(conn)
        
    conn.close()
    db.fileWriter(new['value'])
    print(f'데이터 저장...')

def main():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        s.bind((HOST, PORT))
        s.listen(5)
        print('서버가 시작되었습니다.')

        while True:
            conn,addr = s.accept()
            ids.append(conn)
            id = len(ids)-1
            t= threading.Thread(target=runClient,args=(conn,id))
            t.daemon = True
            t.start()
            
            t.join()
            
            if(len(ids)==0):
                print('서버를 종료합니다.')
                break

if __name__ == "__main__":
    main()