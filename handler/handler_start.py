import logging
import time
import random

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Command

from Sql import logg
from keyboard.kb_client import Start, Menu, Klas, Raf, Tea, Proch, Fresh, Card, Bread, Zakaz
from main import dp

#КОМАНДЫ
@dp.message_handler(Command('start'))
async def start_hand(message: Message):
    photo = open('C:/Users/1353194/Desktop/Новая папка (2)/media/Фото1.jpg', 'rb')
    user_id = message.from_user.id
    user_full = message.from_user.full_name
    user_name = message.from_user.first_name
    logging.info(f'{user_id} {user_full} {user_name} {time.asctime()}')

    await logg(user_id=message.from_user.id, user_name=message.from_user.first_name, user_surname=message.from_user.last_name, time=time.asctime())
   
    await message.answer_photo(photo=photo, caption=f'Привет, {user_name}!\n\nЯ бот уютной кофейни Monolyte Coffee!'
    '\n\nЧерез меня, вы можете выбрать и заказать свои любимые напитки и не только!'
    '\n\nВыбери пункт "Меню", чтобы выбрать необхдимый товар', reply_markup=Start)

@dp.message_handler(Command('card'))
async def start_hand(message: Message):
    photo = open('C:/Users/1353194/Desktop/Новая папка (2)/media/Фото1.jpg', 'rb')
   
    await message.answer_photo(photo=photo, caption=f'Здесь вы можете просмотреть свои товары в корзине и оплатить их!' 
     '\n\nА также просмотореть свои заказы за всё время', reply_markup=Card)

@dp.message_handler(Command('menu'))
async def start_hand(message: Message):
    photo = open('C:/Users/1353194/Desktop/Новая папка (2)/media/Фото1.jpg', 'rb')
   
    await message.answer_photo(photo=photo, caption=f'Выбери нужную категорию из списка:', reply_markup=Menu)

@dp.message_handler(Command('pay'))
async def start_hand(message: Message):
    photo = open('C:/Users/1353194/Desktop/Новая папка (2)/media/Фото1.jpg', 'rb')

    await message.answer_photo(photo=photo, caption=f'Для оформления нажмите на клавиатуру:', reply_markup=Zakaz)

#КНОПКИ МЕНЮ
@dp.callback_query_handler(text_contains='Меню')
async def menu_hand(call: CallbackQuery):

     await call.message.edit_caption(caption=f'Выбери нужную категорию из списка:', reply_markup=Menu)

@dp.callback_query_handler(text_contains='Назад')
async def back_hand(call: CallbackQuery):
    
     await call.message.edit_caption(caption=f'Выбери нужную категорию из списка:', reply_markup=Menu)

@dp.callback_query_handler(text_contains='Отмена')
async def back_hand(call: CallbackQuery):
    
     await call.message.delete()

@dp.callback_query_handler(text_contains='Вернуться на главную')
async def glav_hand(call: CallbackQuery):
     user_name = call.from_user.first_name
     await call.message.edit_caption(caption=f'Привет, {user_name}!\n\n Я бот уютной кофейни Monolyte Coffee!'
    '\n\nЧерез меня, вы можете выбрать и заказать свои любимые напитки и не только!'
    '\n\nВыбери пункт "Меню", чтобы выбрать понравившийся товар', reply_markup=Start)

@dp.callback_query_handler(text_contains='Корзина')
async def card_hand(call: CallbackQuery):

     await call.message.edit_caption(caption=f'Здесь вы можете просмотреть свои товары в корзине и оплатить их!' 
     '\n\nА также просмотореть свои заказы за всё время', reply_markup=Card)

@dp.callback_query_handler(text_contains='Наш сайт')
async def sait_hand(call: CallbackQuery):

     await call.message.edit_caption(caption=f'Здесь вы можете просмотреть свои товары в корзине и оплатить их!' 
     '\n\nА также просмотореть свои заказы за всё время', reply_markup=Start)

@dp.callback_query_handler(text_contains='Помощь')
async def help_hand(call: CallbackQuery):

     await call.message.edit_caption(caption=f'Здесь будет пошаговая инструкция работы с ботом и контактные данные для тех.поддержки!', reply_markup=Start)

@dp.callback_query_handler(text_contains='Рассказать анекдот')
async def Anekdot_hand(call: CallbackQuery):
     user_name = call.from_user.first_name

     F = open('C:/Users/1353194/Desktop/Новая папка (2)/media/Анекдоты.txt', encoding='UTF-8')
     Anek = F.read().split('\n')
     F.close()
     An = random.choices(Anek)

     await call.message.edit_caption(caption=f'Привет, {user_name}!\n\n Я бот уютной кофейни Monolyte Coffee!'
    '\n\nЧерез меня, вы можете выбрать и заказать свои любимые напитки и не только!'
    '\n\nВыбери пункт "Меню", чтобы выбрать понравившийся товар''\n\nАнекдот:'f'\n\n {An}', reply_markup=Start)


#КНОПКИ РАЗДЕЛОВ
@dp.callback_query_handler(text_contains='Классический Кофе')
async def klas(call: CallbackQuery):
    
     await call.message.edit_caption(caption=f'Выбери понравившийся кофе:', reply_markup=Klas)

@dp.callback_query_handler(text_contains='Авторский Раф')
async def raf(call: CallbackQuery):
    
     await call.message.edit_caption(caption=f'Выбери понравившийся раф:', reply_markup=Raf)

@dp.callback_query_handler(text_contains='Авторские Чаи')
async def tea(call: CallbackQuery):
    
     await call.message.edit_caption(caption=f'Выбери понравившийся чай:', reply_markup=Tea)
    
@dp.callback_query_handler(text_contains='Прочие Напитки')
async def proch(call: CallbackQuery):
    
     await call.message.edit_caption(caption=f'Выбери понравившийся напиток:', reply_markup=Proch)

@dp.callback_query_handler(text_contains='Фреш')
async def frash(call: CallbackQuery):
    
     await call.message.edit_caption(caption=f'Выбери понравившийся фреш:', reply_markup=Fresh)

@dp.callback_query_handler(text_contains='Выпечка')
async def bread(call: CallbackQuery):
    
     await call.message.edit_caption(caption=f'Выбери понравившийся товар:', reply_markup=Bread)