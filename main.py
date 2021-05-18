from aiogram import Dispatcher, executor, types

import settings
from app import ConsultantBot

bot = ConsultantBot()
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message) -> None:
    message_text = 'У вас есть вопросы?\n' + \
                   'Можете задать их тут.\n' + \
                   'Вам ответит первый освободившийся косультант.'
    await bot.send_message(message.from_user.id, message_text)


@dp.message_handler(content_types=types.ContentType.ANY, chat_type=types.ChatType.PRIVATE)
async def private_chat_message_handler(message: types.Message) -> None:
    await bot.forward_message(settings.CHAT_ID, message.chat.id, message.message_id)


@dp.message_handler(content_types=types.ContentType.TEXT, chat_type=types.ChatType.GROUP, is_reply=True)
async def group_chat_text_message_handler(message: types.Message) -> None:
    if message.reply_to_message.is_forward() \
            and (chat_id := await bot.get_sender_chat_id_from_reply(message)):
        await bot.send_message(chat_id, message.text)


@dp.message_handler(content_types=types.ContentType.ANY, chat_type=types.ChatType.GROUP, is_reply=True)
async def group_chat_any_message_handler(message: types.Message) -> None:
    if message.reply_to_message.is_forward() \
            and (chat_id := await bot.get_sender_chat_id_from_reply(message)):
        await bot.forward_message(int(chat_id), from_chat_id=message.chat.id, message_id=message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp)
