from aiogram import Bot, Dispatcher, executor, types
import redis
import settings

bot = Bot(token=settings.BOT_API_TOKEN)
dp = Dispatcher(bot)
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
redis_instance.info()  # test connection


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message) -> None:
    message_text = 'У вас есть вопросы?\n' + \
                   'Можете задать их тут.\n' + \
                   'Вам ответит первый освободившийся косультант.'
    await bot.send_message(message.from_user.id, message_text)


@dp.message_handler(content_types=types.ContentType.ANY, chat_type=types.ChatType.PRIVATE)
async def private_chat_message_handler(message: types.Message) -> None:
    msg = await bot.forward_message(settings.CHAT_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    redis_instance.set(msg.message_id, message.chat.id)


@dp.message_handler(content_types=types.ContentType.TEXT, chat_type=types.ChatType.GROUP, is_reply=True)
async def group_chat_text_message_handler(message: types.Message) -> None:
    if message.reply_to_message.is_forward():
        if chat_id := redis_instance.get(message.reply_to_message.message_id):
            await bot.send_message(int(chat_id), message.text)
        else:
            message_text = 'Сообщение отсутствует в базе.'
            await bot.send_message(message.chat.id, message_text, reply_to_message_id=message.message_id)


@dp.message_handler(content_types=types.ContentType.ANY, chat_type=types.ChatType.GROUP, is_reply=True)
async def group_chat_any_message_handler(message: types.Message) -> None:
    if message.reply_to_message.is_forward():
        if chat_id := redis_instance.get(message.reply_to_message.message_id):
            await bot.forward_message(int(chat_id), from_chat_id=message.chat.id, message_id=message.message_id)
        else:
            message_text = 'Сообщение отсутствует в базе.'
            await bot.send_message(message.chat.id, message_text, reply_to_message_id=message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp)
