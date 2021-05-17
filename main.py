from os import getenv

from aiogram import Bot, Dispatcher, executor, types

BOT_API_TOKEN = getenv('BOT_API_TOKEN')
CHAT_ID = int(getenv('CHAT_ID'))

if not BOT_API_TOKEN:
    raise Exception('BOT_API_TOKEN must be defined.')
if not CHAT_ID:
    raise Exception('CHAT_ID must be defined.')

bot = Bot(token=BOT_API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message) -> None:
    message_text = 'У вас есть вопросы?\n' + \
                   'Можете задать их тут.\n' + \
                   'Вам ответит первый освободившийся косультант.'
    await bot.send_message(message.from_user.id, message_text)


@dp.message_handler(content_types=types.ContentType.ANY, chat_type=types.ChatType.PRIVATE)
async def private_chat_message_handler(message: types.Message) -> None:
    await bot.forward_message(CHAT_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    # TODO: redis.set(msg.message_id, message.chat.id)


@dp.message_handler(content_types=types.ContentType.TEXT, chat_type=types.ChatType.GROUP, is_reply=True)
async def group_chat_text_message_handler(message: types.Message) -> None:
    if message.reply_to_message.is_forward():
        chat_id = message.reply_to_message.forward_from.id  # TODO: chat_id = redis.get(message.reply_to_message.message_id)
        await bot.send_message(chat_id, message.text)


@dp.message_handler(content_types=types.ContentType.ANY, chat_type=types.ChatType.GROUP, is_reply=True)
async def group_chat_any_message_handler(message: types.Message) -> None:
    if message.reply_to_message.is_forward():
        chat_id = message.reply_to_message.forward_from.id  # TODO: chat_id = redis.get(message.reply_to_message.message_id)
        await bot.forward_message(chat_id, from_chat_id=message.chat.id, message_id=message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp)
