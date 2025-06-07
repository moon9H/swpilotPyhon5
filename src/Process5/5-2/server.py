# 과정 5 - (문제2) "통신장비에 채팅 기능 추가" (서버)

import socket
import threading

HOST = socket.gethostname()
PORT = 9999

clients = {}
lock = threading.Lock()

def broadcast(message, sender_name=None):
    with lock:
        for name, conn in clients.items():
            if name != sender_name:
                try:
                    conn.sendall(message.encode('utf-8'))
                except:
                    pass

def handle_client(conn, addr):
    try:
        conn.send('이름을 입력하세요: '.encode('utf-8'))
        name = conn.recv(1024).decode('utf-8').strip()

        with lock:
            clients[name] = conn
        welcome_msg = f'{name}님이 입장하셨습니다.\n'
        broadcast(welcome_msg)
        print(f'{name}님 연결됨. ({addr})')

        while True:
            msg = conn.recv(1024).decode('utf-8').strip()
            if not msg:
                continue
            if msg == '/종료':
                with lock:
                    del clients[name]
                exit_msg = f'{name}님이 퇴장하셨습니다.\n'
                print(exit_msg.strip())
                broadcast(exit_msg)
                break
            elif msg.startswith('/귓속말'):
                parts = msg.split(' ', 2)
                if len(parts) < 3:
                    conn.send('사용법: /귓속말 대상이름 메시지\n'.encode('utf-8'))
                else:
                    target, whisper = parts[1], parts[2]
                    with lock:
                        target_conn = clients.get(target)
                    if target_conn:
                        whisper_msg = f'[귓속말] {name} > {whisper}\n'
                        try:
                            target_conn.send(whisper_msg.encode('utf-8'))
                        except:
                            pass
                    else:
                        conn.send('해당 사용자가 없습니다.\n'.encode('utf-8'))
            else:
                broadcast_msg = f'{name} > {msg}\n'
                print(broadcast_msg.strip())
                broadcast(broadcast_msg, sender_name=name)
    except ConnectionResetError:
        pass
    finally:
        with lock:
            if name in clients:
                del clients[name]
        disconnect_msg = f'{name}님이 연결을 종료하셨습니다.\n'
        print(disconnect_msg.strip())
        broadcast(disconnect_msg)
        conn.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f'서버 시작됨. 호스트: {HOST}, 포트: {PORT}')

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == '__main__':
    main()