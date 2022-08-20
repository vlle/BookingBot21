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


class ChangeState(StatesGroup):
    change = State()
    check_login = State()


def change_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Изменить логин', 'Вернуться на главную']
    keyboard.add(*buttons)
    return keyboard


def main_menu_keyboard():
    buttons = []
    buttons.append('Забронировать объект')
    buttons.append('Посмотреть мои бронирования')
    buttons.append('Посмотреть бронирования объекта')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


def return_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Вернуться на главную']
    keyboard.add(*buttons)
    return keyboard


async def request_login(message: types.Message):
    login = ''
    db = DataBase()
    try:
        sel = db.select_login_by_tg_id(message.from_id)
        login = str(sel.first()[0])
        msg = (f"Твой текущий логин: {login}\nХочешь его изменить?")
        await message.answer(msg, reply_markup=change_keyboard())
        await ChangeState.change.set()
    except TypeError:
        await message.answer("err")
        await state.finish()


async def update_login(message: types.Message):
    msg = "Введите новый логин:"
    await message.answer(msg, reply_markup=types.ReplyKeyboardRemove())
    await ChangeState.check_login.set()


async def update_login_db(message: types.Message):
    new_login = message.text
    db = DataBase()
    db.update_login(new_login, message.from_id)
    msg = "Успешно изменено."
    await message.answer(msg, reply_markup=return_main_keyboard())
    await ChangeState.change.set()
    return


async def return_menu(message: types.message, state: FSMContext):
    msg = "Вы в главном меню."
    await message.answer(msg, reply_markup=main_menu_keyboard())
    await state.finish()


def change_login_handlers_register(dp: Dispatcher):
    pass
    dp.register_message_handler(
        request_login, commands="change_login", state="*")
    dp.register_message_handler(
        update_login, Text(equals="Изменить логин"), state=ChangeState.change)
    dp.register_message_handler(
        update_login_db, state=ChangeState.check_login)
    msg = "Вернуться на главную"
    dp.register_message_handler(
        return_menu, Text(equals=msg), state=ChangeState.change)
