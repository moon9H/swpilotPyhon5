# 과정 6 - (문제4) 이제는 실시간 아닌 실시간 메세지

import requests
import json
# 보너스 과제를 위한 라이브러리
import imaplib
import email
from email.header import decode_header

# Gmail IMAP 서버 설정
imap_server = 'imap.gmail.com'
username = input('Enter Your Email-ID : ').strip()
password = input('Enter Your PW: ').strip()

# IMAP 서버에 연결
mail = imaplib.IMAP4_SSL(imap_server)
mail.login(username, password)

# Slack Incoming Webhook URL
webhook_url = 'https://hooks.slack.com/services/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'  # 여기에 본인이 얻은 웹훅 URL을 입력합니다

def sendMessageToSlack(msg) :
    # 메시지를 JSON 형식으로 변환
    payload = json.dumps(msg)

    # HTTP POST 요청으로 메시지 보내기
    response = requests.post(webhook_url, data=payload, headers={'Content-Type': 'application/json'})

    # 응답 확인
    if response.status_code == 200:
        print('메시지가 성공적으로 전송되었습니다.')
    else:
        print(f'오류가 발생했습니다. 오류 코드: {response.status_code}')
        print(response.text)

# 보너스 과제 - 3번 문제 연계 이메일 목록 읽어와서 slack으로 전송
mail.select('inbox')

status, response = mail.search(None, 'ALL')
mail_ids = response[0].split()

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
        date = msg['date']
        slack_message ={
            'text': f"새로운 [Goheung] 메일 도착!\n보낸 사람: {sender}\n제목: {decoded_subject}\n시간: {date}"
        } 
        # slack으로 메일 정보 전송
        sendMessageToSlack(slack_message)

# IMAP 연결 종료
mail.logout()