from cgitb import text
from curses import keyname
from email import message
import logging
from time import sleep, time
import asyncio
from pickle import FALSE, TRUE
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked
from aiogram.utils.callback_data import CallbackData
from os import getenv
from sys import exit
from aiogram.dispatcher.filters import Text

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from database import db
from database.db_operations import DataBase
from datetime import date, timedelta
import re

users_accs = []
users_accs.append({})
users_accs[0]['tg_id'] = 609105930
users_accs[0]['login'] = 'maykitbo'
users_accs[0]['role'] = 1
# users_accs.append({})
# users_accs[1]['tg_id'] = 918616493
# users_accs[1]['login'] = 'arrowwhi'
# users_accs[1]['role'] = 4


class Mainmenu(StatesGroup):
    waiting_login = State()
    main_menu = State()


def main_menu_keyboard():
    buttons = []
    buttons.append('Забронировать объект')
    buttons.append('Посмотреть мои бронирования')
    buttons.append('Посмотреть бронирования объекта')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


async def registration(message: types.Message, state: FSMContext):
    base = DataBase()
    access = True
    print(users_accs)
    check = base.select_login_by_tg_id(message.from_id)
    try:
        log = check.first()[0]
    except TypeError:
        access = False
    if not access:
        await message.answer("Привет! Пожалуйста, введи свой школьный логин:")
        await Mainmenu.waiting_login.set()
    else:
        await message.answer(f"Привет, {log}! "
                             f"Ты находишься в главном меню.",
                             reply_markup=main_menu_keyboard())
        await state.finish()


async def login_user(message: types.Message, state: FSMContext):
    base = DataBase()
    login = message['text']
    # здесь добавляем юзера в бд
    ln = len(users_accs)
    users_accs.append({})
    users_accs[ln]["tg_id"] = message.from_id
    users_accs[ln]["login"] = message.text
    users_accs[ln]["role"] = 1
    base.insert_user(message.from_id, message.text, 2)
    await message.answer(f"Привет, {login}! "
                         f"Ты находишься в главном меню.",
                         reply_markup=main_menu_keyboard())
    await state.finish()


def main_menu_start(dp: Dispatcher):
    dp.register_message_handler(registration, commands="start", state="*")
    dp.register_message_handler(login_user, state=Mainmenu.waiting_login)
