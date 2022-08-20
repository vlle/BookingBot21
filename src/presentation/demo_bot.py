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

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import date, timedelta
import re

bot_token = "5364674659:AAHdsuguCkMva00NYX0TCNXMiiJrBan4Zvc" 
if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)


class videoState(StatesGroup):
    state_1 = State()
    state_2 = State()
    state_3 = State()
    state_4 = State()


async def state_00(message: types.Message):
    await message.answer("Привет!")
    await videoState.state_1.set()


async def state_01(message: types.Message):
    await message.answer("Конечно, именно я в таких случаях и нужен!")
    await message.answer("Ты можешь забронировать любую игру или помещение на нужное тебе время через меня. Тогда я смогу сказать всем, что в это время будешь играть именно ты, и никого не подпущу.")
    await message.answer("Чтобы забронировать, просто нажми кнопку «Забронировать объект»")
    await videoState.state_2.set()


async def state_02(message: types.Message):
    await message.answer("Я могу и это!")
    await message.answer("Просто нажми «Показать бронирования объекта», выбери свой объект, и я покажу тебе, когда он занят, а когда свободен и тебя ничего не ограничит.")
    await videoState.state_3.set()


async def state_03(message: types.Message):
    await message.answer("Разумеется!")
    await message.answer("За 15 минут до начала я пришлю тебе напоминание о твоем бронировании.")
    await videoState.state_4.set()


async def state_04(message: types.Message, state: FSMContext):
    await message.answer("Конечно, ты же занятой человек, я все понимаю!")
    await message.answer("В таком случае ты сможешь просто отменить свое бронирование, отправив мне \"/cancel\" при бронировании, или удалить свое бронирование позже.")
    await state.finish()


def inline_register_handlers_booking(dp: Dispatcher):
    dp.register_message_handler(state_00, commands="start", state="*")
    dp.register_message_handler(state_01, state=videoState.state_1)
    dp.register_message_handler(state_02, state=videoState.state_2)
    dp.register_message_handler(state_03, state=videoState.state_3)
    dp.register_message_handler(state_04, state=videoState.state_4)

def main():
    inline_register_handlers_booking(dp)
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    # Запускаем бота и пропускаем все накопленые входящие
    main()
