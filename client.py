import socket

HOST = 'localhost'
PORT = 9150

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while True:
        print('-----------------------------------')
        print('모드를 선택하세요.')
        print('(0:종료, 1:업로드, 2:다운로드)')
        print('-----------------------------------')
        msg = input('입력) ')
        print('-----------------------------------')

        s.sendall(msg.encode('utf-8'))

        data = (s.recv(1024).decode('utf-8').split())
        if data[0] == "종료":
            print('서버)종료합니다.')
            print('-----------------------------------')
            break
        
        elif data[0] == "업로드":
            print('서버)업로드합니다.')
            print('문장을 입력하세요. ')
            print('-----------------------------------')
            while True:
                msg = input('입력) ')
                print('-----------------------------------')
                s.sendall(msg.encode('utf-8'))

                txt = list(s.recv(1024).decode('utf-8').split('/'))
                if(txt[0]=='재송신'):
                    print('다시 입력해주세요.')
                    print('-----------------------------------')
                    continue
                else:
                    break

            print(f'암호:{txt[0]}')
            print(f'키:{txt[1]}')

            continue

        elif data[0] == "다운로드":
            if data[1] == '0':
                print('서버)업로드된 암호가 없습니다.')
                continue

            print('서버)다운로드합니다.')
            print('-----------------------------------')

            while True:
                print(f'총 {data[1]}개의 암호가 있습니다.')
                print('다운로드 할 암호를 고르세요.')
                print('-----------------------------------')
                msg = input('입력) ')

                if(msg > data[1] or msg == '0'):
                    print('다시 입력해주세요.')
                    print('-----------------------------------')
                    continue
                else:
                    break

            s.sendall(msg.encode('utf-8'))

            txt = list(s.recv(1024).decode('utf-8').split('/'))
            
            print('-----------------------------------')
            print(f'암호:{txt[0]}')
            print(f'키:{txt[1]}')
            continue

        elif data[0] == "재송신":
            print('다시 입력해주세요.')
            continue