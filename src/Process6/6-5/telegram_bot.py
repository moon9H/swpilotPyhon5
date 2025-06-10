# 과정 6 - (문제5) 또 다른 메신저

import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# API 키 설정
TELEGRAM_API_KEY = '6951569916:AAGaaFCXoZ9N3U5QB-5we871X3zHuL8L424'  # 여기에 Bot Father가 제공한 API 키를 입력합니다.

# /start 명령어 처리 함수
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('안녕하세요! 텔레그램 봇이 활성화되었습니다. 메시지를 입력해보세요.')

# 일반 메시지 처리 함수
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    received_message = update.message.text
    if received_message.lower() == '안녕':  # [보너스 과제] - 메시지가 '안녕'인 경우 응답
        await update.message.reply_text('응 안녕')
    else:  # 그 외의 메시지는 에코
        await update.message.reply_text(f'받은 메시지: {received_message}')

# 에러 처리 함수
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'업데이트 {update} 에러: {context.error}')

async def main() -> None:
    # Application 객체 생성
    application = ApplicationBuilder().token(TELEGRAM_API_KEY).build()

    # 핸들러 등록
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # 에러 핸들러 등록
    application.add_error_handler(error)

    # 봇 시작
    await application.initialize()  # 애플리케이션 초기화
    await application.start()  # 애플리케이션 시작
    print("봇이 시작되었습니다.")
    
    # 봇을 종료하지 않도록 대기
    await asyncio.Future()  # 이 라인을 추가하여 계속 실행되도록 대기

if __name__ == '__main__':
    # asyncio.run(main())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
