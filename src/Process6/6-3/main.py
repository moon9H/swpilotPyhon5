# 과정 6 - (문제3) 중요한 메일만 골라내기

import imaplib
import email
from email.header import decode_header
import csv

# Gmail IMAP 서버 설정
imap_server = 'imap.gmail.com'
username = input('Enter Your Email-ID : ').strip()
password = input('Enter Your PW: ').strip()

# CSV 파일 이름
csv_filename = 'src/Process6/6-3/high_priority_mail_contents.csv'

# IMAP 서버에 연결
mail = imaplib.IMAP4_SSL(imap_server)
mail.login(username, password)

# 받은 편지함 선택
mail.select('inbox')

# 최근 메일 가져오기
status, response = mail.search(None, 'ALL')
mail_ids = response[0].split()

# CSV 파일에 저장할 데이터 준비
mail_data = []

print("Finding [Goheung] mails (in Recent 50 mails)....")

for num in reversed(mail_ids[-50:]):  # 최근 50개의 메일
    status, data = mail.fetch(num, '(RFC822)')
    raw_email = data[0][1]
    
    msg = email.message_from_bytes(raw_email)
    subject = msg['subject']
    
    # MIME 형식으로 인코딩된 제목 디코딩
    decoded_part = decode_header(subject)
    decoded_subject = ''
    for decoded_bytes, charset in decoded_part:
        if isinstance(decoded_bytes, bytes):
            decoded_bytes = decoded_bytes.decode(charset or 'utf-8', errors='ignore')
        else:
            decoded_bytes = str(decoded_bytes)
        decoded_subject += decoded_bytes
    
    # '[Goheung]'이 제목에 포함된 경우에만 처리
    if 'Goheung' in decoded_subject:
        # 보너스 과제 - 발신자 가져오기
        sender = msg['from']
        
        # 보너스 과제 -  본문을 가져오는 반복문
        content = None
        for part in msg.walk():
            content_type = part.get_content_type()
            if 'text/plain' in content_type:
                charset = part.get_content_charset()
                if charset:
                    content = part.get_payload(decode=True).decode(charset, 'ignore')
                else:
                    content = part.get_payload(decode=True).decode('utf-8', 'ignore')
                break
            elif 'text/html' in content_type:
                charset = part.get_content_charset()
                if charset:
                    content = part.get_payload(decode=True).decode(charset, 'ignore')
                else:
                    content = part.get_payload(decode=True).decode('utf-8', 'ignore')
                break
    
        # CSV 파일에 저장할 데이터 추가
        mail_data.append([decoded_subject, sender, content])

# IMAP 연결 종료
mail.logout()

# 보너스 과제 - CSV 파일에 메일 제목, 보낸 사람, 내용 저장
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Mail Subject', 'Sender', 'Content'])
    for data in mail_data:
        writer.writerow(data)

print(f"메일 제목, 보낸 사람, 내용이 {csv_filename} 파일에 저장되었습니다.")

# [보너스 과제] - CSV 파일에서 메일 제목, 보낸 사람, 내용 출력
print('-----------------메일 목록-----------------')
with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # 첫 번째 행(헤더) 건너뛰기
    for row in reader:
        mail_subject, sender, content = row
        print(f"메일 제목: {mail_subject}")
        print(f"보낸 사람: {sender}")
        print(f"내용: {content}")
        print('----------------------------------------')
