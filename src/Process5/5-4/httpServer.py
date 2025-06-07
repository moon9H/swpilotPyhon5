# 과정 5 - (문제4) "조금 더 나은 웹서버"

import http.client
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

# HTTP 서버 설정
PORT = 8080
server_address = ('', PORT)

# index.html 파일 경로
HTML_FILE_PATH = 'src/Process5/5-4/index.html'

# IPinfo.io API endpoint
IPINFO_API_HOST = 'ipinfo.io'
IPINFO_API_PATH = '/{ip}/json'

# HTTP 요청을 처리할 핸들러 클래스 정의
class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 요청 받은 시간
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 클라이언트의 IP 주소
        client_address = self.client_address[0]
        # IP 주소를 기반으로 위치 정보 조회
        location_info = self.get_location_info(client_address)
        
        # 서버 측에서 접속 정보 출력
        print(f'[{current_time}] 클라이언트 접속: {client_address}, 접속 위치 : {location_info}')
        
        # 응답 상태코드 200과 헤더 설정
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        # index.html 파일 읽기
        with open(HTML_FILE_PATH, 'rb') as file:
            html_content = file.read()
        
        # HTML 문서를 클라이언트에 전송
        self.wfile.write(html_content)
    
    def get_location_info(self, ip_address):                # 보너스 과제 - ip address기반으로 위치 정보 조회
        try:
            # 예외 처리: localhost에 접속한 경우
            if ip_address == '127.0.0.1' or ip_address == '::1':
                return 'Localhost'
            
            # HTTP 연결 설정
            conn = http.client.HTTPSConnection(IPINFO_API_HOST)
            url = IPINFO_API_PATH.format(ip=ip_address)
            
            # HTTP GET 요청 전송
            conn.request('GET', url)
            
            # HTTP 응답 가져오기
            response = conn.getresponse()
            
            # 응답 데이터 읽기
            data = response.read().decode('utf-8')
            
            # JSON 데이터 파싱
            location_data = json.loads(data)
            
            # 위치 정보 추출
            country = location_data.get('country', 'Unknown Country')
            city = location_data.get('city', 'Unknown City')
            
            location_info = f'{country}, {city}'
            
            # 연결 닫기
            conn.close()
            
            return location_info
        
        except Exception as e:
            print(f'Error fetching location information: {e}')
            return 'Location not available'


# HTTP 서버 실행 함수
def run(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    print(f'Starting HTTP server on port {port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    
    httpd.server_close()
    print('Stopping HTTP server...')

# 메인으로 실행할 경우 HTTP 서버 시작
if __name__ == '__main__':
    run()
    print()