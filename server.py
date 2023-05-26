import socket
import select
import encoder

HOST = ''
PORT = 9150
MODE = [0,1,2]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('서버가 시작되었습니다.')

    readsocks = [s]
    ids = {}
    id = 1
    code_list = []

    while True:
        readables, writeables, excpetions = select.select(readsocks, [], [])
        for sock in readables:
            if sock == s:  # 신규 클라이언트 접속
                newsock, addr = s.accept()
                print(f'클라이언트가 접속했습니다:{addr}, id는 {id} 입니다.')
                readsocks.append(newsock)
                ids[newsock] = id  # 클라이언트 별 id 배정
                id = id + 1
            else:  # 이미 접속한 클라이언트의 요청
                conn = sock
                code = conn.recv(1024).decode('utf-8')
                print(f'user{ids[conn]}: {code}')

                if code == '0' or code == '종료':
                    conn.sendall(f"종료".encode('utf-8'))
                    print(f'user{ids[conn]} 종료')
                    conn.close()
                    readsocks.remove(conn)  # 클라이언트 접속 해제시 readsocks에서 제거

                elif code == '1' or code == '업로드':
                    conn.sendall(f"업로드".encode('utf-8'))
                    
                    while True:
                        data = conn.recv(1024).decode('utf-8')
                        try:
                            data = data.upper()
                            msg = encoder.encoding(data)
                            conn.sendall(msg.encode('utf-8'))
                            code_list.append(msg)
                            break
                        except:
                            conn.sendall(f'재송신/'.encode('utf-8'))
                            continue    
                
                elif code == '2' or code == '다운로드':
                    conn.sendall(f"다운로드 {len(code_list)}".encode('utf-8'))
                    
                    if(len(code_list) == 0):
                        break
                    index = conn.recv(1024).decode('utf-8')

                    try:
                        conn.sendall(f"{code_list.pop(index - 1)}".encode('utf-8'))

                    except:
                        conn.sendall(f"{code_list.pop(0)}".encode('utf-8'))
                    continue

                else:
                    conn.sendall(f'재송신'.encode('utf-8'))
                    continue