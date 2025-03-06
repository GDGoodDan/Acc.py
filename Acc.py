from telethon.sync import TelegramClient, events
import asyncio
import os

# Данные для авторизации (замени значениями)
API_ID = 29930267
API_HASH = "ac4b7df13786a48c2ea6951c50ce2727"
PHONE_NUMBER = "+79586480633"
STICKER_ID = "CAACAgIAAxkBAAEN_lpnyU1g6pi_82Umz-XX_mdFw6f2ZQACimEAAtj-SEousBIxo6gejDYE"

# Чаты, в которых бот работает
CHATS = {
    "Match4uBot": {
        "search": "Иcкать coбeceдника 🌀",
        "stop": "Остановить 💔",
        "found_message": "💭 Собеседник уже в диалоге"
    },
    "ZnakomstvaAnonimniyChatBot": {
        "search": "🔎 Найти собеседника",
        "stop_command": "/stop",
        "found_message": "Собеседник найден!"
    }
}

# Текст сообщения
MESSAGE_TEXT = (
    "Привет, геймер! Если ты фанат Geometry Dash, обожаешь испытания и хочешь окунуться "
    "в дружескую атмосферу единомышленников, то тебе точно сюда!\n\n"
    "На моём канале я делюсь своими успехами, прохожу самые сложные уровни — от Hard Demon до Extreme Demon, "
    "и создаю уникальные авторские уровни. Здесь ты найдёшь эпичные моменты, напряжённые прохождения и море эмоций!\n\n"
    "Присоединяйся и будь частью комьюнити! 🚀"
)

async def main():
    async with TelegramClient("anon", API_ID, API_HASH) as client:
        await client.start(PHONE_NUMBER)
        print("Бот запущен!")

        while True:
            for chat, actions in CHATS.items():
                entity = await client.get_entity(chat)

                # Начинаем поиск собеседника
                await client.send_message(entity, actions["search"])
                print(f"Ищем собеседника в {chat}")

                while True:
                    async for message in client.iter_messages(entity, limit=10):
                        if actions["found_message"] in message.text:
                            print(f"Собеседник найден в {chat}, отправляем сообщение...")
                            await client.send_message(entity, MESSAGE_TEXT)
                            await asyncio.sleep(2)
                            
                            # Отправка стикера
                            try:
                                await client.send_file(entity, STICKER_ID)
                            except Exception as e:
                                print(f"Ошибка при отправке стикера: {e}")
                            
                            await asyncio.sleep(2)

                            # Завершаем диалог
                            if "stop" in actions:
                                await client.send_message(entity, actions["stop"])
                            elif "stop_command" in actions:
                                await client.send_message(entity, actions["stop_command"])
                            break
                    
                    await asyncio.sleep(5)  # Ждём перед следующим поиском

if __name__ == "_main_":
    asyncio.run(main())