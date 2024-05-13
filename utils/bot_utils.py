MAX_MESSAGE_LENGTH = 4096


async def send_big_message(bot, user_id, text, *args, **kwargs):
    for i in range(0, len(text), MAX_MESSAGE_LENGTH):
        await bot.send_message(user_id, text[i:i + MAX_MESSAGE_LENGTH], *args, **kwargs)
