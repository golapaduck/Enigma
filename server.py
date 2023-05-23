import socket
import select
import encoder

HOST = ''
PORT = 9150

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('서버가 시작되었습니다.')

    readsocks = [s]
    ids = {}
    id = 1

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
                data = conn.recv(1024).decode('utf-8')
                print(f'데이터:{data}')

                try:
                    msg = list(data.split('/'))
                    code = msg[0]
                    if(len(msg)==2):
                        key = msg[1]
                    else:
                        key=''
                except ValueError:
                    conn.sendall(f'입력값이 올바르지 않습니다:{data}'.encode('utf-8'))
                    continue

                if code == '0' or code == '종료' and key =='':
                    conn.sendall(f"종료".encode('utf-8'))
                    conn.close()
                    readsocks.remove(conn)  # 클라이언트 접속 해제시 readsocks에서 제거
                elif key != '':
                    conn.sendall(('결과:' + encoder.encoding(code,key = key)).encode('utf-8'))
                elif code:
                    conn.sendall(('결과:' + encoder.encoding(code)).encode('utf-8'))