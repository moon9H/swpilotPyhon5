# 과정 5 - (문제1) "통신장비와 통신" (클라이언트)

import socket

def main():
    # 서버 주소 및 포트 설정
    host = socket.gethostname()
    port = 9999

    # 소켓 생성 및 연결
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print('클라이언트와 연결 되었습니다.')

        while True:
            # 사용자 입력
            message = input('메시지 입력 (종료하려면 "quit"): ')
            client_socket.send(message.encode('utf-8'))

            if message.lower() == 'quit':
                print('연결을 종료합니다.')
                break

            # 서버로부터 회신 수신
            response = client_socket.recv(1024).decode('utf-8')
            print(f'서버 응답: {response}')

    except ConnectionRefusedError:
        print('서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.')

    finally:
        client_socket.close()

if __name__ == '__main__':
    main()