# 과정 6 - (문제1) SOS

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# 보너스 과제 - 첨부파일 추가를 위한 라이브러리
from email.mime.base import MIMEBase            
from email import encoders                      
import ssl

# SMTP 서버 정보 설정
smtp_server = "smtp.gmail.com"
port = 587  # TLS 포트

# 보내는 사람 정보
sender_email = input('Enter Your Email-ID : ').strip()
sender_pw = input('Enter Your PW: ').strip()

# 받는 사람 정보
receiver_email = input('보내고 싶은 분의 이메일을 입력하세요 : ')

# 이메일 내용 작성
subject = "Level 1 Test Email"
body = "Level 1 정상 작동 테스트 확인 메일입니다."

# MIME 객체 생성 및 설정
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

# [보너스 과제] - 첨부 파일 추가
filename = "sendmail.py"  # 첨부할 파일 이름
attachment_path = "src/Process6/6-1/sendmail.py"  # 파일 경로

try:
    # 파일을 바이너리 모드로 열기
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        
    # 파일을 base64로 인코딩
    encoders.encode_base64(part)
    
    # 헤더 추가
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    # 메시지에 첨부 파일 추가
    msg.attach(part)

    # SSL context 생성
    context = ssl.create_default_context()

    # SMTP 서버에 연결
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)  # TLS(Transport Layer Security) 시작
        server.login(sender_email, sender_pw)  # 로그인
        server.sendmail(sender_email, receiver_email, msg.as_string())  # 이메일 전송
        print("메일이 성공적으로 보내졌습니다.")
except FileNotFoundError:
    print(f"파일을 찾을 수 없습니다: {attachment_path}")
except smtplib.SMTPException as e:
    print(f"SMTP 에러가 발생했습니다: {e}")
except Exception as e:
    print(f"일반 에러가 발생했습니다: {e}")