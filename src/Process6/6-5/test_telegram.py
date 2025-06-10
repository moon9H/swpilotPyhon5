# 과정 6 - (문제5) 또 다른 메신저

import asyncio
import telegram

bot = telegram.Bot(token='6951569916:AAGaaFCXoZ9N3U5QB-5we871X3zHuL8L424')

chat_id_list = []

async def recmsg():
    offset = None
    
    while True:
        updates = await bot.get_updates(offset=offset, timeout=60)  # 60초마다 확인
        
        for update in updates:
            offset = update.update_id + 1  # 다음 업데이트를 위해 offset 업데이트
            chat_id = update.message.chat.id
            msg = update.message.text
            sender = update.message.chat.first_name + update.message.chat.last_name
            date = update.message.date.strftime('%Y-%m-%d %H:%M:%S')

            print(f'{sender}({chat_id}) ({date}) : {msg}')
            
            # [보너스 과제] - 사용자가 ‘안녕’ 이라고 하면 ‘응 안녕’과 같이 자동으로 응답하는 기능
            if msg == '안녕':
                await bot.send_message(chat_id=chat_id, text='응 안녕')

async def main():
    await recmsg()

if __name__ == '__main__':
    asyncio.run(main())