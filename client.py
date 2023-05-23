import socket

HOST = 'localhost'
PORT = 9150

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while True:
        msg = input("문장을 입력하세요:")
        if(msg.find('/') == -1):
            msg = msg+'/'
        if not msg.strip():
            print("입력값이 잘못되었습니다.")
            continue
        s.sendall(msg.encode('utf-8'))
        data = s.recv(1024).decode('utf-8')
        print(f'서버:{data}')
        if data == "종료":
            break
