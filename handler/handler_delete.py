import asyncio

from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
from contextlib import suppress
from aiogram import types
from main import bot

#УДАЛЕНИЕ СООБЩЕНИЙ
async def self_delete_message(message: types.Message, sleep_time):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        bot.set_current(bot)
        await message.delete()