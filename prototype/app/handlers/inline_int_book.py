from cgitb import text
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

from datetime import date, timedelta
import re

from database import db
from database.db_operations import DataBase

campuses = []
all_type_objects = []
all_name_objects = []
name_objects = []
db = DataBase()
aa = db.select_uniq_campus()
for i in aa:
    campuses.append(list(i)[0])
bb = db.select_types_for_user('Москва', 1919118841)
for i in bb:
    all_type_objects.append(list(i)[0])
bb = db.select_types_for_user('Новосибирск', 1919118841)
for i in bb:
    all_type_objects.append(list(i)[0])
bb = db.select_all_name_object()
for i in bb:
    all_name_objects.append(list(i)[0])


chosen = {}


def main_menu_keyboard():
    buttons = []
    buttons.append('Забронировать объект')
    buttons.append('Посмотреть мои бронирования')
    buttons.append('Посмотреть бронирования объекта')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


class Booking(StatesGroup):
    waiting_city = State()
    waiting_type = State()
    waiting_obj = State()
    waiting_time = State()
    waiting_ex_time = State()
    waiting_ex_time_set = State()
    waiting_confirm = State()
    insert_confirm = State()
    incert_cancel = State()


class BookingInfo:
    def __init__(self):
        self.id = ''
        self.campus = ''
        self.type = ''
        self.object = ''
        self.date = ''
        self.start_time = ''
        self.end_time = ''

    def add_id(self, id_o):
        self.id = id_o

    def add_campus(self, campus):
        self.campus = campus

    def add_type(self, type_o):
        self.type = type_o

    def add_object(self, object_o):
        self.object = object_o

    def add_date(self, date):
        self.date = date

    def add_start_time(self, start_time):
        self.start_time = start_time

    def add_end_time(self, end_time):
        self.end_time = end_time


global CurrentBooking
CurrentBooking = BookingInfo()
global userBooking
userBooking = {}
callback_numbers = CallbackData("fabnum", "action")


def all_zones(zon: list, type: str, choose: dict):
    out = []
    zone = zon.copy()
    for i in zone:
        for key in choose:
            if i[key] != choose[key]:
                zone.remove(i)
                continue
    for i in zone:
        if i[type] not in out:
            out.append(i[type])
    return out


def get_keyboard(zones):
    # Генерация клавиатуры.
    buttons = []
    for i in zones:
        buttons.append(types.InlineKeyboardButton(
            text=i, callback_data=callback_numbers.new(action=i)))
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def keyboard_date():
    buttons = []
    buttons.append(types.InlineKeyboardButton(
        text="Сегодня", callback_data=callback_numbers.new(action='tod')))
    buttons.append(types.InlineKeyboardButton(
        text="Завтра", callback_data=callback_numbers.new(action='tom')))
    buttons.append(types.InlineKeyboardButton(
        text="Другая дата",
             callback_data=callback_numbers.new(action='another')))
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard


async def book_start(message: types.Message):
    global zones
    global chosen
    chosen = {}
    buttons = []
    userBooking[message.from_id] = \
        userBooking.get(message.from_id, BookingInfo())

    await message.answer("Вы бронируете объект.",
                         reply_markup=types.ReplyKeyboardRemove())
    keyboard = get_keyboard(campuses)
    await message.answer('Выберите город:', reply_markup=keyboard)
    await Booking.waiting_city.set()


async def type_chosen(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    chosen['city'] = action
    userBooking[call.from_user.id].add_campus(action)
    userBooking[call.from_user.id].add_id(call.from_user.id)
    db = DataBase()
    type_objects = []
    try:
        bb = db.select_types_for_user(
                userBooking[call.from_user.id].campus, call.from_user.id)
        for i in bb:
            type_objects.append(list(i)[0])
    except TypeError:
        print("ERRAR")
    keyboard = get_keyboard(type_objects)
    await call.message.edit_text("Выберите, что будете бронировать",
                                 reply_markup=keyboard)
    await Booking.waiting_type.set()
    await call.answer()


async def obj_chosen(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    chosen['type'] = action
    userBooking[call.from_user.id].add_type(action)
    db = DataBase()
    names = []
    try:
        vb = db.select_objects_name(
                userBooking[call.from_user.id].campus,
                userBooking[call.from_user.id].type)
        for i in vb:
            names.append(list(i)[0])
    except TypeError:
        print("ERR: typerr")
    keyboard = get_keyboard(names)
    await call.message.edit_text("Пожалуйста, выберите:",
                                 reply_markup=keyboard)
    await Booking.waiting_obj.set()
    await call.answer()


async def date_chosen(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    chosen['name'] = action
    userBooking[call.from_user.id].add_object(action)
    keyboard = keyboard_date()
    await call.message.edit_text("Когда хотите?", reply_markup=keyboard)
    await Booking.waiting_time.set()
    await call.answer()


async def time_chosen(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == 'another':
        await call.message.edit_text('Введите дату в формате ГГГГ-ММ-ДД:')
        await Booking.waiting_ex_time_set.set()
        await call.answer()
    else:
        if action == 'tod':
            data = str(date.today())
            userBooking[call.from_user.id].add_date(data)
        elif action == 'tom':
            data = str(date.today()+timedelta(days=1))
            userBooking[call.from_user.id].add_date(data)
        await call.message.edit_text('Введите время в формате ЧЧ-ЧЧ. '
                                     'Например, 09-18:')
        await Booking.waiting_confirm.set()
        await call.answer()


async def ex_date_chosen_set(message: types.Message):
    match = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', message.text)
    if not match:
        await message.answer("Введите дату в правильном формате!")
        return
    else:
        listmatch = match[0].split('-')
        if (int(listmatch[0]) < 2022 or
                int(listmatch[0]) > 3022 or int(listmatch[1]) > 12 or
                int(listmatch[2]) > 31):
            await message.answer("Введите дату в правильном формате!")
            return
        chosen['date'] = match.group(0)
        userBooking[message.from_id].add_date(chosen['date'])
        await message.answer("Введите время в формате ЧЧ-ЧЧ. Например, 09-18:")
        await Booking.waiting_confirm.set()


async def check_time(message: types.Message):
    match = re.search(r'[0-9]{2}-[0-9]{2}', message.text)
    if (not match or 0 > int(message.text.split('-')[0]) or
            int(message.text.split('-')[0]) >= int(message.text.split('-')[1])
            or int(message.text.split('-')[1]) > 24):
        await message.answer("Введите время в правильном формате!")
        return
    else:
        time = match[0].split('-')
        chosen['start_time'] = time[0]
        chosen['end_time'] = time[1]
        userBooking[message.from_id].add_start_time(time[0])
        userBooking[message.from_id].add_end_time(time[1])
        # тут нужна функция сравнения времени с остальными временами объекта
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        buttons = []
        buttons.append(types.InlineKeyboardButton(
            text="Подтвердить",
                 callback_data=callback_numbers.new(action='confirm_booking')))
        buttons.append(types.InlineKeyboardButton(
            text="Отменить",
                 callback_data=callback_numbers.new(action='cancel_booking')))
        keyboard.add(*buttons)
        msg = (f'Вы выбрали:\n<b>' +
               f'Город:</b> {userBooking[message.from_id].campus}\n' +
               f'<b>Тип</b>: {userBooking[message.from_id].type}\n' +
               f'<b>Объект:</b> {userBooking[message.from_id].object}\n' +
               f'<b>Дата: </b>{userBooking[message.from_id].date}\n' +
               f'<b>Время:</b> {userBooking[message.from_id].start_time}-' +
               f'{userBooking[message.from_id].end_time}\n\n')
        await message.answer(msg, reply_markup=keyboard)
        await Booking.insert_confirm.set()


async def check_confirm(call: types.CallbackQuery,
                        callback_data: dict, state: FSMContext):
    action = callback_data["action"]
    if action == 'confirm_booking':
        # тут идет отправка запроса в бд
        db = DataBase()
        db.insert_booking(
                userBooking[call.from_user.id].id,
                userBooking[call.from_user.id].object,
                userBooking[call.from_user.id].type,
                userBooking[call.from_user.id].start_time,
                userBooking[call.from_user.id].end_time,
                userBooking[call.from_user.id].date)
        msg = (f'Вы выбрали:\n<b>Город: </b>' +
               f'{userBooking[call.from_user.id].campus}\n' +
               f'<b>Тип</b>: {userBooking[call.from_user.id].type}\n' +
               f'<b>Объект:</b> {userBooking[call.from_user.id].object}\n' +
               f'<b>Дата:</b> {userBooking[call.from_user.id].date}\n' +
               f'<b>Время:</b> {userBooking[call.from_user.id].start_time}' +
               f'-{userBooking[call.from_user.id].end_time}\n\n' +
               'Успешно подтверждено. ☺️')
        await call.message.edit_text(msg)
    else:
        await call.message.edit_text('Вы отменили бронь.')
    await call.answer()
    sleep(1)
    await call.message.answer("Вы в главном меню.",
                              reply_markup=main_menu_keyboard())
    await state.finish()


def inline_register_handlers_booking(dp: Dispatcher):
    db = DataBase()
    dp.register_message_handler(book_start, Text(
        equals='Забронировать объект'), state="*")
    dp.register_callback_query_handler(type_chosen, callback_numbers.filter(
        action=campuses), state=Booking.waiting_city)
    dp.register_callback_query_handler(obj_chosen, callback_numbers.filter(
        action=all_type_objects), state=Booking.waiting_type)
    dp.register_callback_query_handler(date_chosen, callback_numbers.filter(
        action=all_name_objects), state=Booking.waiting_obj)
    dp.register_callback_query_handler(time_chosen, callback_numbers.filter(
        action=['tod', 'tom', 'another']), state=Booking.waiting_time)
    dp.register_message_handler(
        ex_date_chosen_set, state=Booking.waiting_ex_time_set)
    dp.register_message_handler(
        check_time, state=Booking.waiting_confirm)
    dp.register_callback_query_handler(check_confirm, callback_numbers.filter(
                                       action=['confirm_booking',
                                               'cancel_booking']),
                                       state=Booking.insert_confirm)
