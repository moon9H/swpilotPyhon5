# 과정 5 - (문제2) "통신장비에 채팅 기능 추가" (클라이언트)

import socket
import threading
import sys

HOST = socket.gethostname()
PORT = 9999

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            sys.stdout.write('\r' + ' ' * 80 + '\r')  # 현재 줄 클리어
            print(message.strip())
            sys.stdout.write(f'{username}> ')
            sys.stdout.flush()
        except:
            break

def main():
    global username

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # 서버에서 이름 요청 메시지 수신
    prompt = client_socket.recv(1024).decode('utf-8')
    print(prompt, end='')
    username = input()
    client_socket.sendall(username.encode('utf-8'))

    # 메시지 수신 쓰레드 시작
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    while True:
        sys.stdout.write(f'{username}> ')
        sys.stdout.flush()
        msg = input()
        if msg == '/종료':
            client_socket.sendall(msg.encode('utf-8'))
            break
        client_socket.sendall(msg.encode('utf-8'))

    client_socket.close()

if __name__ == '__main__':
    main()