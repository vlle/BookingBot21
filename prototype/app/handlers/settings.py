from email import message
import logging
from time import sleep, time
import asyncio
from pickle import FALSE, TRUE
from typing import Type
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked
from aiogram.utils.callback_data import CallbackData
from os import getenv
from sys import exit
from aiogram.dispatcher.filters import Text

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from datetime import date, timedelta
import re
import database.db
import database.db_operations
from database.db_operations import DataBase


class SettingsState(StatesGroup):
    settings = State()
    wait_id = State()
    wait_book = State()
    conf_book = State()
    rm_book = State()
    wait_login = State()
    change_userrole = State()
    change_obj = State()
    confirm_change = State()
    confirm_change_strong = State()


class userData():

    def __init__(self):
        self.tg_id = ''
        self.login = ''
        self.role = ''
        self.book = ''

    def add_id(self, id_o):
        self.id = id_o

    def add_login(self, login):
        self.login = login

    def add_role(self, role):
        self.role = role

    def add_book(self, book):
        self.book = book


global currentUser
currentUser = userData()


async def get_settings(message: types.Message):
    await message.answer("Привет, admin. Что ты хочешь сделать?")
    await SettingsState.wait_id.set()


async def get_book(message: types.Message):
    await message.answer("Введи айди бронирования.")
    await SettingsState.conf_book.set()


async def get_id(message: types.Message):
    await message.answer("Введи айди юзера.")
    await SettingsState.wait_login.set()


async def get_login(message: types.Message):
    await message.answer("Введи новый логин юзера.")
    tg_id = message.text
    currentUser.add_id(tg_id)
    await SettingsState.confirm_change.set()


async def remove_book(message: types.Message):
    book = message.text
    currentUser.add_book(book)
    msg = (f'Подтверждаете удаление? (yes/cancel)\n')
    await message.answer(msg)
    await SettingsState.rm_book.set()


async def remove_book_hard(message: types.Message, state: FSMContext):
    db = DataBase()
    try:
        db.delete_booking(currentUser.book)
        await message.answer(f"Success!")
    except TypeError:
        await message.answer(f"Oh, fail!")
    await state.finish()


async def conf_data(message: types.Message):
    new_login = message.text
    currentUser.add_login(new_login)
    msg = (f'Подтверждаете изменения? (yes/cancel)\n')
    msg2 = (f'Ваши данные: {currentUser.login}\n{currentUser.id}')
    msg3 = msg + msg2
    await message.answer(msg3)
    await SettingsState.confirm_change_strong.set()


async def set_data(message: types.Message, state: FSMContext):
    db = DataBase()
    try:
        db.update_login(currentUser.login, currentUser.id)
        await message.answer(f"Success!")
    except TypeError:
        await message.answer(f"Oh, fail!")
    await state.finish()


def admin_handler(dp: Dispatcher):
    dp.register_message_handler(
            get_settings, commands="secret_admin", state="*")
    dp.register_message_handler(
            get_id, Text(equals="change"), state=SettingsState.wait_id)
    dp.register_message_handler(
            get_book, Text(equals="delete"), state=SettingsState.wait_id)
    dp.register_message_handler(
            get_login, state=SettingsState.wait_login)
    dp.register_message_handler(
            remove_book, state=SettingsState.conf_book)
    dp.register_message_handler(
            remove_book_hard,
            Text(equals="yes"), state=SettingsState.rm_book)
    dp.register_message_handler(
            conf_data, state=SettingsState.confirm_change)
    dp.register_message_handler(
            set_data, Text(equals="yes"),
            state=SettingsState.confirm_change_strong)
