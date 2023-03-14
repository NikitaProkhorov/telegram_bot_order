import asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN
from Sql import db_start

loop    = asyncio.new_event_loop()
bot     = Bot(BOT_TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp      = Dispatcher(bot, loop=loop, storage=storage)

async def on_startup(_):
     await db_start()

if __name__ == '__main__':

    from handler.handler_start import dp
    from handler.handler_pay import dp
    from keyboard.kb_num import dp
    from FSM.FSM_deliv import dp
    from sklearn.skl import dp
    
    executor.start_polling(dp, on_startup=on_startup)

