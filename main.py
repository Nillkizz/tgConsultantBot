from aiogram import Bot, types
from aiogram import Dispatcher, executor
from redis import StrictRedis

import settings

bot = Bot(token=settings.BOT_API_TOKEN)
dp = Dispatcher(bot)
redis = StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
redis.ping()  # Check redis connection


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message) -> None:
    message_text = 'У вас есть вопросы?\n' + \
                   'Можете задать их тут.\n' + \
                   'Вам ответит первый освободившийся косультант.'
    await bot.send_message(message.from_user.id, message_text)


@dp.message_handler(content_types=types.ContentType.ANY, chat_type=types.ChatType.PRIVATE)
async def forward_to_chat(message: types.Message) -> None:
    from_chat_id = message.chat.id
    forwarded_message = await bot.forward_message(settings.CHAT_ID, message.chat.id, message.message_id)
    redis.set(forwarded_message.message_id, from_chat_id)


@dp.message_handler(content_types=types.ContentType.ANY, chat_type=types.ChatType.GROUP, is_reply=True)
async def copy_message_to_private(message: types.Message) -> None:
    replied_message_id = message.reply_to_message.message_id
    if recipient_chat_id := redis.get(replied_message_id):
        await message.send_copy(int(recipient_chat_id))
    else:
        message_text = 'Сообщение отсутствует в базе.'
        await send_message(message.chat.id, message_text, reply_to_message_id=message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp)
