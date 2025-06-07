# 과정 5 - (문제3) "나 혼자 보는 웹서버"

from http.server import BaseHTTPRequestHandler, HTTPServer

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # 요청 경로를 기반으로 파일 경로 결정
            if self.path == '/image':
                self.path = '/http_image.jpg'  # 보너스 과제 - 이미지 출력 : 경로에 /image 추가해서 해당 링크로 접속 시 이미지 출력
            
                with open('.' + self.path, 'rb') as file:
                    # 파일 확장자에 따라 Content-type 설정
                    if self.path.endswith('.jpg'):
                        self.send_response(200)
                        self.send_header('Content-type', 'image/jpeg')
                        self.end_headers()
                        # 파일 내용 읽어서 클라이언트에게 전송
                        self.wfile.write(file.read())
                
            else:                           # 다른 추가 링크가 없을 시 원래의 과제 수행
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                # 클라이언트에게 보낼 HTML 문서
                html_content = """
                <html>
                <body>
                    <h1>It is my HTTP server</h1>
                </body>
                </html>
                """
                self.wfile.write(html_content.encode('utf-8'))
        
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

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

if __name__ == '__main__':
    run()