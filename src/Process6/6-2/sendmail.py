# 과정 6 - (문제2) 감동의 메세지

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import ssl
import csv

# SMTP 서버 정보 설정
smtp_server = "smtp.gmail.com"
port = 587  # TLS 포트

# 보내는 사람 정보
sender_email = input('Enter Your Email-ID : ').strip()
sender_pw = input('Enter Your PW: ').strip()

# CSV 파일에서 수신자 목록 읽기 - 받는 사람에 여러명을 열거하는 방법
# receiver_emails = []
# with open('src/Process6/6-2/mail_target_list.csv', newline='', encoding='utf-8') as csvfile:
#     reader = csv.reader(csvfile)
#     next(reader)  # 헤더 건너뛰기
#     for row in reader:
#         receiver_emails.append(row[1])

# CSV 파일에서 수신자 목록 읽기 - 한번에 한 명씩 메일을 반복적으로 보내는 방법
receivers = []
with open('src/Process6/6-2/mail_target_list.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # 헤더 건너뛰기
    for row in reader:
        receivers.append((row[0], row[1]))

# 이메일 내용 작성 (HTML 형식)
subject = "테스트 HTML 메일"
html_body = """
<html>
<head></head>
<body>
    <p>안녕하세요,</p>
    <p>이것은 <b>테스트2 HTML 메일</b>입니다.</p>
    <p>감사합니다.</p>
</body>
</html>
"""

# 받는 사람에 여러명을 열거하는 방법

# MIME 객체 생성 및 설정
# msg = MIMEMultipart()
# msg["From"] = sender_email
# msg["To"] = ", ".join(receiver_emails)
# msg["Subject"] = subject
# msg.attach(MIMEText(html_body, "html"))

# try:
#     # SSL context 생성
#     context = ssl.create_default_context()

#     # SMTP 서버에 연결
#     with smtplib.SMTP(smtp_server, port) as server:
#         server.starttls(context=context)  # TLS(Transport Layer Security) 시작
#         server.login(sender_email, sender_pw)  # 로그인
#         server.sendmail(sender_email, receiver_emails, msg.as_string())  # 이메일 전송
#         print("메일이 성공적으로 보내졌습니다.")
# except FileNotFoundError:
#     print(f"파일을 찾을 수 없습니다: {attachment_path}")
# except smtplib.SMTPException as e:
#     print(f"SMTP 에러가 발생했습니다: {e}")
# except Exception as e:
#     print(f"일반 에러가 발생했습니다: {e}")


# 한번에 한 명씩 메일을 반복적으로 보내는 방법
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