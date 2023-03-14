import asyncio
import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from main import dp, bot
from config import BOT_TOKEN
from handler.handler_delete import self_delete_message
from keyboard.kb_client import deliv, adres, time, Start, hourse, min, Card, pay


class Form(StatesGroup):
    dostavka = State() 
    comment = State()
    address = State()
    time = State()  
    hourse = State()
    min = State()
    pay = State()
    

@dp.callback_query_handler(text_contains='Оформить заказ')
async def dev(call: CallbackQuery):

    connect = sqlite3.connect('bot.db')
    cursor = connect.cursor()
    cursor.execute("""DELETE FROM deliv WHERE user_id=(?)""", [call.from_user.id])
    sum = cursor.execute("""SELECT SUM(price) FROM card WHERE user_id=(?)""", [call.from_user.id]).fetchone()[0]
    prod = cursor.execute("""SELECT prod_id, price, value FROM card WHERE user_id=(?)""", [call.from_user.id]).fetchall()
    card = []
    for i in prod:
        card.append(f"{i[0]} × {i[2]}шт. - {i[1]}₽")
    res = ("\n    ".join(map(str, card)))

    cursor.close()
    connect.commit()

    if card == []:
          msg = await bot.send_message(call.from_user.id, 'Добавьте хотя бы один товар!')
          asyncio.create_task(self_delete_message(msg, 2))
     
    elif card != []:
        await Form.dostavka.set()
        await call.message.answer(f'<b>Ваш заказ:</b>\n    {res}\n\n<b>Cумма заказа:</b> \n    {sum}₽\n\n<b>Как хотите получить заказ?</b>', reply_markup=deliv)


@dp.callback_query_handler(text_contains="Отмена", state='*')
@dp.message_handler(Text(equals='Отмена', ignore_case=True), state='*')
async def cancel_handler(call: CallbackQuery, state: FSMContext):
    connect = sqlite3.connect('bot.db')
    cursor = connect.cursor()
    cursor.execute("""DELETE FROM deliv WHERE user_id=(?)""", [call.from_user.id])
    connect.commit()
    cursor.close()

    current_state = await state.get_state()
    if current_state is None:
       return
    
    await state.finish()

@dp.callback_query_handler(state=Form.dostavka)
async def process_dostavka(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['dostavka'] = call.data

    if call.data == "Заберу Сам":
        await Form.comment.set()
        await call.message.edit_text("Можете оставить любой комментарий или пожелание к своему заказу:")

    elif call.data == "Доставка":
        await Form.comment.set()
        await call.message.edit_text("Обратите внимание!\n\nДоставка производится, только в пределах помещений:\n\n"
                                        "Мельникайте 106\nТРЦ 'Сити Молл'\nТРЦ 'Матрешка'\nЖК 'Айвазовский'\n\n"
                                        "Отправьте сообщение с названием офиса или описанием вашего местонахождения:\n")

@dp.message_handler(state=Form.comment)
async def process_comment(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['comment'] = message.text

    await Form.address.set()
    await message.answer("Выберите кофейню, которая находится ближе всего:", reply_markup=adres)


@dp.callback_query_handler(state=Form.address)
async def process_address(call: CallbackQuery, state: FSMContext):
    
    async with state.proxy() as data:
        data['tochka'] = call.data
                         
    await Form.time.set()
    await call.message.edit_text("Когда заказ должен быть готов?", reply_markup=time)


@dp.callback_query_handler(state=Form.time)
async def process_time(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
            data['vrem'] = call.data
            data['id']   = call.from_user.id
    

    if call.data == "Как можно скорее":
            connect = sqlite3.connect('bot.db')
            cursor = connect.cursor()
     
            sum = cursor.execute("""SELECT SUM(price) FROM card WHERE user_id=(?)""", [call.from_user.id]).fetchone()[0]
            prod = cursor.execute("""SELECT prod_id, price, value FROM card WHERE user_id=(?)""", [call.from_user.id]).fetchall()
            cursor.execute("""INSERT INTO deliv (user_id, dostavka, address, time, comment) VALUES(?,?,?,?,?)""", (data['id'], data['dostavka'], data['tochka'], data['vrem'], data['comment']))
           
            card = []
            for i in prod:
                card.append(f"{i[0]} × {i[2]}шт. - {i[1]}₽")
            res = ("\n    ".join(map(str, card)))

            cursor.close()
            connect.commit()
            
            await call.message.edit_text(
                        f"<b>Ваш заказ:</b>\n    {res}\n\n<b>Cумма заказа:</b> \n    {sum}₽\n\n"
                        f"Способ получения: \n    {data['dostavka']}\n\n"
                        f"Время:\n    {data['vrem']}\n\n"
                        f"Адрес:\n    {data['tochka']}", reply_markup=pay)
            await state.finish()

    elif call.data == "Указать время":
        await Form.hourse.set()
        await call.message.edit_text("Выберите час:", reply_markup=hourse)


@dp.callback_query_handler(state=Form.hourse)
async def process_hourse(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['hourse'] = call.data

    await call.message.edit_text("Выберите минуту:", reply_markup=min) 
    await Form.min.set()

@dp.callback_query_handler(state=Form.min)
async def process_min(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['min'] = call.data
        data['id']  = call.from_user.id
    connect = sqlite3.connect('bot.db')
    cursor = connect.cursor()
     
    sum = cursor.execute("""SELECT SUM(price) FROM card WHERE user_id=(?)""", [call.from_user.id]).fetchone()[0]
    prod = cursor.execute("""SELECT prod_id, price, value FROM card WHERE user_id=(?)""", [call.from_user.id]).fetchall()
    cursor.execute("""INSERT INTO deliv (user_id, dostavka, address, time, hours, min, comment) VALUES(?,?,?,?,?,?,?)""", (data['id'], data['dostavka'], data['tochka'],data['vrem'], data['hourse'], data['min'], data['comment']))
    card = []
    for i in prod:
        card.append(f"{i[0]} × {i[2]}шт. - {i[1]}₽")
    res = ("\n    ".join(map(str, card)))

    cursor.close()
    connect.commit()
            
    await call.message.edit_text(
                        f"<b>Ваш заказ:</b>\n    {res}\n\n<b>Cумма заказа:</b>\n    {sum}₽\n\n"
                        f"Способ получения: \n    {data['dostavka']}\n\n"
                        f"Время:\n    {data['hourse']}:{data['min']}\n\n"
                        f"Адрес:\n    {data['tochka']}", reply_markup=pay)
    
    await state.finish()


