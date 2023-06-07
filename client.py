import socket

HOST = 'localhost'
PORT = 9150

# 업로드
def upload():
    while True:
        msg = input('입력(알파벳만 가능): ')
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
    
# 다운로드(data는 서버에서 받은 암호 개수)
def download(data):
    if data == list():
        print('서버)암호가 없습니다.')
        return

    print('서버)다운로드합니다.')

    print('-------------암호--------------')
    dateList = list(data.split('/'))
    for date in dateList:
        print(f'{date}')
    print('날짜를 고르세요.')
    print('---------------------------')
    
    # 날짜 선택
    while True:
        setDate = input('입력: ')
        if setDate in dateList:
            break
        else:
            print("다시 입력해주세요.")
            continue
    s.sendall(setDate.encode('utf-8'))
    print('---------------------------')
    
    codes = s.recv(1024).decode('utf-8')
    print(f'총 {codes}개의 암호가 있습니다.')

    print('다운로드 할 대상을 고르세요.')
    print('---------------------------')
    while True:
        index = int(input('입력:'))
        if(0< index <= int(codes)):
            index -= 1
            break
        else:
            print("다시 입력해주세요.")
            
    s.sendall(f"{index}".encode('utf-8'))

    txt = list(s.recv(1024).decode('utf-8').split('/'))
            
    print('---------------------------')
    print(f'암호:{txt[0]}')
    print(f'키:{txt[1]}')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while True:
        print('---------------------------')
        print('모드를 선택하세요.')
        print('(0:종료, 1:업로드, 2:다운로드)')
        print('---------------------------')
        msg = input('입력: ')
        print('---------------------------')

        
        if msg == "0":
            s.sendall(msg.encode('utf-8'))
            print('서버)종료합니다.')
            print('---------------------------')
            break
            
        elif msg == "1":
            s.sendall(msg.encode('utf-8'))
            print('서버)업로드합니다.')
            print('문장을 입력하세요. ')
            print('---------------------------')
            upload()
            continue

        elif msg == "2":
            s.sendall(msg.encode('utf-8'))
            data = s.recv(1024)
            download(data.decode('utf-8'))
            continue

        else:
            print('다시 입력해주세요.')
            continue
