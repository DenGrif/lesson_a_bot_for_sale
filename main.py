import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

from config import *
from keyboards import *
import texts

logging.basicConfig(level=logging.INFO)
bot = Bot(token = API)
dp = Dispatcher(bot, storage= MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    # Обрабатываем случай, если фамилия может быть не указана
    full_name = f"{first_name} {last_name}" if last_name else first_name
    await message.answer(f"Добро пожаловать, {full_name}!\n" + texts.start, reply_markup=start_kb)


#message.answer_photo
#.answer_video
#.answer_file


@dp.message_handler(text="О нас")
async def price(message):
    with open('About.jpg', "rb") as img:
        await message.answer_photo(img, texts.about, reply_markup=start_kb)

@dp.message_handler(text="Стоимость")
async def info(message):
    await message.answer("Что вас интересует?", reply_markup=catalog_kb)

@dp.callback_query_handler(text = "medium")
async def buy_m(call):
    await call.message.answer(texts.Mgame, reply_markup=buy_kb)
    await call.answer() # Чтоб закрыть работу кнопки

@dp.callback_query_handler(text = "big")
async def buy_l(call):
    await call.message.answer(texts.Lgame, reply_markup=buy_kb)
    await call.answer() # Чтоб закрыть работу кнопки

@dp.callback_query_handler(text = "mega")
async def buy_xl(call):
    await call.message.answer(texts.XLgame, reply_markup=buy_kb)
    await call.answer() # Чтоб закрыть работу кнопки

@dp.callback_query_handler(text = "other")
async def buy_other(call):
    await call.message.answer(texts.other, reply_markup=buy_kb)
    await call.answer() # Чтоб закрыть работу кнопки

@dp.callback_query_handler(text="back_to_catalog")
async def back(call):
    await call.message.answer("Что вас интересует?", reply_markup=catalog_kb)
    await call.answer()  # Чтоб закрыть работу кнопки

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)