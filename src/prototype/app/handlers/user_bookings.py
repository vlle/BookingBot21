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

from .inline_int_book import Booking
from database import db
from app.handlers.inline_int_book import get_keyboard
from database.db_operations import DataBase


class MyBook(StatesGroup):
    check_answer = State()
    all_bookings = State()
    date_bookings = State()
    ret_main_menu = State()
    waiting_cancel_id = State()


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


async def booking_choice(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Показать все мои бронирования',
               'Показать мои бронирования на определенный день']
    keyboard.add(*buttons)
    await message.answer('Что хотите сделать?', reply_markup=keyboard)
    await MyBook.check_answer.set()


async def all_my_bookings(message: types.Message):
    len = 1

    await message.answer('Вот все бронирования:',
                         reply_markup=types.ReplyKeyboardRemove())
    sleep(0.5)
    db = DataBase()
    aa = db.select_user_bookingName(message.from_id)
    lst = []
    for i in aa:
        lst.append(list(i)[0])
    keyboard = get_keyboard(lst)
    await message.answer(lst)
    return
    if mes == 'w':
        await message.answer("Бронирований не найдено",
                             reply_markup=return_main_keyboard())
        await MyBook.ret_main_menu.set()
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ['Отменить бронирование', 'Вернуться на главную']
        keyboard.add(*buttons)
        await message.answer("Что хотите сделать?",
                             reply_markup=keyboard)
        await MyBook.ret_main_menu.set()


async def cancel_booking(message: types.Message):
    await message.answer("Введите id бронирования, который хотите отменить:",
                         reply_markup=types.ReplyKeyboardRemove())
    await MyBook.waiting_cancel_id.set()


async def cancel_booking_id(message: types.Message):
    try:
        sol_id = int(message.text)
    except ValueError:
        await message.answer("Введите только id!")
        return
    for i in range(len(boo)):
        if (boo[i]['id'] == sol_id and
                boo[i]['user_id'] == str(message.from_id)):
            boo.pop(i)
            await message.answer('Бронирование успешно отменено',
                                 reply_markup=return_main_keyboard())
            await MyBook.ret_main_menu.set()
            return
    await message.answer('Бронирования с таким id на ваше имя не найдено.')
    return


async def all_my_bookings_day(message: types.Message):
    await message.answer("Введите дату поиска в формате ГГГГ-ММ-ДД:",
                         reply_markup=types.ReplyKeyboardRemove())
    await MyBook.date_bookings.set()


async def print_day_bookings(message: types.Message):
    match = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', message['text'])
    if not match:
        await message.answer("введите дату в правильном формате!")
        return
    else:
        listmatch = match[0].split('-')
        if (int(listmatch[0]) < 2022 or
                int(listmatch[0]) > 3022 or int(listmatch[1]) > 12
                or int(listmatch[2]) > 31):
            await message.answer("введите дату в правильном формате!")
            return
        chosen_date = match[0]
        my_id = message['from']['id']
        # Здесь вытаскивается таблица по tg_id
        await message.answer(f"Вот ваши бронирования на {message.text}:")
        messi = "w"
        for i in boo:
            if (i['date'] == message.text and i['user_id'] == str(my_id)):
                messi = ''
                for key in i:
                    if key != 'user_id':
                        messi += key+': ' + str(i[key]) + '\n'
                await message.answer(messi)
                sleep(0.5)
        if messi == "w":
            await message.answer("бронирований на эту дату не найдено.",
                                 reply_markup=return_main_keyboard())
            await MyBook.ret_main_menu.set()


async def return_main_menu(message: types.message, state: FSMContext):
    await message.answer("Вы в главном меню.",
                         reply_markup=main_menu_keyboard())
    await state.finish()


def my_bookings_handlers_register(dp: Dispatcher):
    dp.register_message_handler(
        booking_choice, Text(equals="Посмотреть мои бронирования"), state="*")
    dp.register_message_handler(all_my_bookings,
                                Text(equals="Показать все мои бронирования"),
                                state=MyBook.check_answer)
    dp.register_message_handler(all_my_bookings_day,
                                Text(equals="Показать мои "
                                     "бронирования на определенный день"),
                                state=MyBook.check_answer)
    dp.register_message_handler(print_day_bookings,
                                state=MyBook.date_bookings)
    dp.register_message_handler(return_main_menu,
                                Text(equals="Вернуться на главную"),
                                state=MyBook.ret_main_menu)
    dp.register_message_handler(cancel_booking,
                                Text(equals="Отменить бронирование"),
                                state=MyBook.ret_main_menu)
    dp.register_message_handler(cancel_booking_id,
                                state=MyBook.waiting_cancel_id)
