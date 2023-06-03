import socket
import selectors
import threading

import module.database as db
import module.encoder as en

HOST = ''
PORT = 9150
sel = selectors.DefaultSelector()


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
    print(f"user{id}: 암호 접속:{setDate}")
    
    index = conn.recv(1024).decode('utf-8')
    
    conn.sendall(f"{dataList[int(index)]}".encode('utf-8'))
    print(f"user{id}: 다운로드 암호:{dataList[int(index)]}")
    
def run(conn):
    id =ids.index(conn)
    
    code_list = db.fileReader()
    new = code_list['new']
    
    try:
        code = conn.recv(1024).decode('utf-8')
    
    except ConnectionResetError:
            print(f'user{id}가 강제로 종료되었습니다.')
    
    if code == '0' or code == '종료':
        print(f'user{id} 종료')
        
        if conn in ids:
            ids.remove(conn)
        
        sel.unregister(conn)
        conn.close()
    
        db.fileWriter(new['value'])
        print(f'데이터 저장...')
        
    elif code == '1' or code == '업로드':
        t= threading.Thread(target=upload,args=(conn,id))
        t.daemon = True
        t.start()
                
    elif code == '2' or code == '다운로드':
        t= threading.Thread(target=download,args=(conn,id))
        t.daemon = True
        t.start()
                

    
def serv(socket):
    conn,addr = socket.accept()
    sel.register(conn,selectors.EVENT_READ, run)
    ids.append(conn)
    print(f"user{ids.index(conn)}가 접속하였습니다.")


def main():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        s.bind((HOST, PORT))
        s.listen(5)
        print('서버가 시작되었습니다.')
        sel.register(s, selectors.EVENT_READ,serv)
        
        con = True
        
        while True:
            if(len(ids)==0 and con == False):
                break
            events = sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj)
                con = False

        sel.unregister(s)
        s.close()
        print("서버를 종료합니다.")

if __name__ == "__main__":
    main()