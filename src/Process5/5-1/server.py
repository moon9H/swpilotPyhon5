# 과정 5 - (문제1) "통신장비와 통신" (서버)

import socket

HOST = socket.gethostname()
PORT = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('소켓 생성완료')

server_socket.bind((HOST, PORT))

# 커넥션 3개로 제한
server_socket.listen(3)

print(f'호스트 이름: {HOST}')
print(f'{PORT}번 포트에서 연결 대기 중...')

# [보너스과제] - 챗봇용 응답 키워드
chatbot_responses = {
    'hello': '안녕하세요! 반가워요!',
    'name': '저는 에코봇입니다.',
    'weather': '오늘 날씨는 맑음입니다.'
}

while True:
    client_socket, addr = server_socket.accept()
    print('클라이언트와 연결 되었습니다.')

    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        print(f'클라이언트로부터 받은 메시지: {data}')

        if data.lower() == 'quit':
            client_socket.send('연결을 종료합니다.'.encode('utf-8'))
            break

        response = chatbot_responses.get(data.strip(), data)  # echo or chatbot
        client_socket.send(response.encode('utf-8'))

    client_socket.close()
    print('클라이언트 연결 종료')
