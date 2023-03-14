import sqlite3
import asyncio

from aiogram import types
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from handler.handler_delete import self_delete_message
from config import PAY_TOKEN_MASTER, CHAT_ID_MELNIK, CHAT_ID_AIVA, CHAT_ID_CITY_MOLL, CHAT_ID_MATRESHKA
from keyboard.kb_client import Card
from main import dp, bot

#ОПЛАТА
@dp.callback_query_handler(text_contains='Оплатить')
async def buy(call: CallbackQuery):
     connect = sqlite3.connect('bot.db')
     cursor = connect.cursor()
     data = cursor.execute("""SELECT user_id, prod_id, price FROM card WHERE user_id=(?)""", [call.from_user.id]).fetchall()
     cursor.close()
     connect.commit()
     cursor = connect.cursor()
     new_data = []
     for i in range(len(data)):
          new_data.append(cursor.execute("""SELECT * FROM card WHERE prod_id=(?)""", [data[i][1]]).fetchall())
     cursor.close()
     connect.commit()
     connect.close
     new_data = [new_data[i][0] for i in range(len(new_data))]
     price = [LabeledPrice(label=i[1], amount=i[2]*100) for i in new_data]

     if price == []:
          msg = await bot.send_message(call.from_user.id, 'Добавьте хотя бы один товар!')
          asyncio.create_task(self_delete_message(msg, 2))
     
     elif price != []:
          await bot.send_invoice(call.from_user.id,
               title='Monolyte / Оплата', 
               description='Нажмите кнопку "Заплатить", чтобы подтвердить оплату',
               provider_token=PAY_TOKEN_MASTER,
               currency='rub',
               max_tip_amount = 100000,
               suggested_tip_amounts = [5000, 10000, 20000, 30000],
               need_email=True,
               need_phone_number=True,
               prices=price, 
               start_parameter='example', 
               payload='some_invoice')
     

@dp.pre_checkout_query_handler(lambda q: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
     await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def pay(message: Message):
     connect = sqlite3.connect('bot.db')
     cursor = connect.cursor()
     cursor.execute("""INSERT INTO classific 
                       SELECT user_id, prod_id, value
                       FROM card
                       WHERE user_id=(?)""", [message.chat.id])
     
     user_id = message.from_user.url
     user_name = message.chat.first_name
     sum = cursor.execute("""SELECT SUM(price) FROM card WHERE user_id=(?)""", [message.chat.id]).fetchone()[0]
     prod = cursor.execute("""SELECT prod_id, price, value FROM card WHERE user_id=(?)""", [message.chat.id]).fetchall()
     deliv = cursor.execute("""SELECT * FROM deliv WHERE user_id=(?)""", [message.chat.id]).fetchall()
     address = cursor.execute("""SELECT address FROM deliv WHERE user_id=(?)""", [message.chat.id]).fetchone()[0]

     c = []
     for i in prod:
          c.append(f"{i[0]} × {i[2]}шт. - {i[1]}₽")
     res = ("\n    ".join(map(str, c)))

     d = []
     for i in deliv:
          d.append(f"<b>Способ получения:</b>\n    {i[1]}\n\n"
                   f"<b>Кофейня:</b>\n    {i[2]}\n\n"
                   f"<b>Время:</b>\n    {i[3]}\n\n"
                   f"<b>Время:</b>\n    {i[4]}:{i[5]}\n\n"
                   f"<b>Комментарий:</b>\n    {i[6]}")
     r = ("".join(map(str, d)))

     if address == 'Мельникайте 106':
          await bot.send_message(CHAT_ID_MELNIK, text=f'<b>Заказ пользователя:</b>\n    {user_id} - {user_name}\n\n'
                            f'<b>Заказ на сумму:</b>\n    {sum}₽\n\n'
                            f'<b>Заказ:</b>\n    {res}\n\n'
                            f'{r}')
     
     elif address == 'ТРЦ "Сити Молл"':
          await bot.send_message(CHAT_ID_CITY_MOLL, text=f'<b>Заказ пользователя:</b>\n    {user_id} - {user_name}\n\n'
                            f'<b>Заказ на сумму:</b>\n    {sum}₽\n\n'
                            f'<b>Заказ:</b>\n    {res}\n\n'
                            f'{r}')
          
     elif address == 'ТРЦ "Матрешка"':
          await bot.send_message(CHAT_ID_MATRESHKA, text=f'<b>Заказ пользователя:</b>\n    {user_id} - {user_name}\n\n'
                            f'<b>Заказ на сумму:</b>\n    {sum}₽\n\n'
                            f'<b>Заказ:</b>\n    {res}\n\n'
                            f'{r}')
          
     elif address == 'ЖК "Айвазовский"':
          await bot.send_message(CHAT_ID_AIVA, text=f'<b>Заказ пользователя:</b>\n    {user_id} - {user_name}\n\n'
                            f'<b>Заказ на сумму:</b>\n    {sum}₽\n\n'
                            f'<b>Заказ:</b>\n    {res}\n\n'
                            f'{r}')

     cursor.execute("""DELETE FROM card WHERE user_id=(?)""", [message.chat.id])
     cursor.close()
     connect.commit()
     connect.close()








#ПРОСМОТР КОРЗИНЫ
@dp.callback_query_handler(text_contains='Просмотреть Корзину')
async def card(call: CallbackQuery):
     connect = sqlite3.connect('bot.db')
     cursor = connect.cursor()
     
     sum = cursor.execute("""SELECT SUM(price) FROM card WHERE user_id=(?)""", [call.from_user.id]).fetchone()[0]
     prod = cursor.execute("""SELECT prod_id, price, value FROM card WHERE user_id=(?)""", [call.from_user.id]).fetchall()
     card = []
     for i in prod:
          card.append(f"{i[0]} × {i[2]}шт. - {i[1]}₽")
     res = ("\n    ".join(map(str, card)))

     cursor.close()
     connect.commit()

     await call.message.edit_caption(caption=f'<b>Товаров на сумму:</b>\n    {sum}₽\n\n<b>В корзине:</b>\n    {res}', reply_markup=Card)

#ОЧИСТКА КОРЗИНЫ
@dp.callback_query_handler(text_contains='Очистить Корзину')
async def clear(call: CallbackQuery):
     connect = sqlite3.connect('bot.db')
     cursor = connect.cursor()
     cursor.execute("""DELETE FROM card WHERE user_id=(?)""", [call.from_user.id])
     cursor.close()
     connect.commit()
     connect.close()

     await call.message.edit_caption(caption=f'Здесь вы можете просмотреть свои товары в корзине и оплатить их!' 
     '\n\nА также просмотореть свои заказы за всё время', reply_markup=Card)
     
     msg = await bot.send_message(call.from_user.id, 'Ваша корзина успешно очищена!')
     asyncio.create_task(self_delete_message(msg, 2))
