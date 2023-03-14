import matplotlib
import datetime
import numpy as np
import pandas as pd
from matplotlib import colors
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt, numpy as np
import sys
import warnings
import pandas as pd
import sqlite3
import aiogram
from aiogram.types import Message, CallbackQuery
from main import dp

@dp.callback_query_handler(text_contains='X')
async def skl_hand(call: CallbackQuery):

    con = sqlite3.connect("bot.db")
    df = pd.read_sql_query("SELECT * FROM classific", con)
    print(df.head())

    # skl = []
    # for i in df:
    #     skl.append(f"{i[0]} — {i[1]} — {i[2]}")
    # res = ("\n    ".join(map(str, skl)))
    
    con.close()
    await call.message.answer(f'Заказы: \n\n{df}')


# # Read sqlite query results into a pandas DataFrame
# con = sqlite3.connect("bot.db")
# df = pd.read_sql_query("SELECT * FROM classific", con)

# # Verify that result of SQL query is stored in the dataframe
# print(df.head())


# con.close()
