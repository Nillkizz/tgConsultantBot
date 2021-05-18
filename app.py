import redis
from aiogram import Bot, types

import settings


class ConsultantBot(Bot):
    def __init__(self, token=settings.BOT_API_TOKEN, *args, **kwargs):
        self.redis_instance = redis.StrictRedis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        self.redis_instance.info()  # test connection
        super().__init__(token, *args, *kwargs)

    async def forward_message(self, *args, **kwargs) -> types.Message:
        msg = await super(ConsultantBot, self).forward_message(*args, **kwargs)
        from_chat_id = kwargs.get('from_chat_id') or args[1]
        chat_id = kwargs.get('chat_id') or args[0]
        if chat_id == settings.CHAT_ID:
            self.redis_instance.set(msg.message_id, from_chat_id)
        return msg

    async def get_sender_chat_id_from_reply(self, message):
        if chat_id := self.redis_instance.get(message.reply_to_message.message_id):
            return int(chat_id)
        message_text = 'Сообщение отсутствует в базе.'
        await self.send_message(message.chat.id, message_text, reply_to_message_id=message.message_id)
