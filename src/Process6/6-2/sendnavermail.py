# 과정 6 - (문제2) 감동의 메세지 
# [보너스 과제] - NAVER로 이메일 전송하기 (SMTP 서버 정보 설정)

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import ssl
import csv

smtp_server = "smtp.naver.com"
port = 587  # TLS 포트

# 보내는 사람 정보
sender_email = input('Enter Your Email-ID : ').strip()
sender_pw = input('Enter Your PW: ').strip()

# CSV 파일에서 수신자 목록 읽기
receivers = []
with open('src/Process6/6-2/mail_target_list.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # 헤더 건너뛰기
    for row in reader:
        receivers.append((row[0], row[1]))

# 이메일 내용 작성 (HTML 형식)
subject = "[Goheung Universe Center] Message To Mars"
html_body = """
<html>
<head></head>
<body>
    <p>안녕하세요, {name}님</p>
    <p>이것은 <b>테스트 HTML 메일</b>입니다.</p>
    <p>감사합니다.</p>
</body>
</html>
"""

# SSL context 생성
context = ssl.create_default_context()

for name, email in receivers:
    # MIME 객체 생성 및 설정
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body.format(name=name), "html"))

    try:
        # SMTP 서버에 연결
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)  # TLS(Transport Layer Security) 시작
            server.login(sender_email, sender_pw)  # 로그인
            server.sendmail(sender_email, email, msg.as_string())  # 이메일 전송
            print(f"메일이 성공적으로 {name}님에게 보내졌습니다.")
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {attachment_path}")
    except smtplib.SMTPException as e:
        print(f"SMTP 에러가 발생했습니다: {e}")
    except Exception as e:
        print(f"일반 에러가 발생했습니다: {e}")
