import csv
import os
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from engine import write_csv, write_csv_Offer, render
from Video_redactor import gluing, conversion
from data import Token
bot = Bot(Token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    name = State()
    time = State()

class Offers(StatesGroup):
    Offer = State()

def read_txt(text):
    file_open = open("messages/" + text,"r",encoding="utf-8")
    text = file_open.read()
    return(text)

@dp.message_handler(commands=['start'])
async def menu(message):
    start_menu = types.ReplyKeyboardMarkup(True, True)
    start_menu.row('меню')
    await bot.send_message(message.chat.id,read_txt("welcome_message.txt"), reply_markup=start_menu)


@dp.message_handler(commands=['help'])
async def menu(message):
    start_menu = types.ReplyKeyboardMarkup(True, True)
    start_menu.row('меню')
    await bot.send_message(message.chat.id,"заглушечка)", reply_markup=start_menu)

@dp.message_handler(lambda message: message.text == "меню")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Посмотреть список видео", "Отправить список","Предложение идей"]
    keyboard.add(*buttons)
    await message.answer("Привет, что хочешь сделать?", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Админка")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Рендер)","Рендер всего", "Конвертация видео"]
    keyboard.add(*buttons)
    await message.answer("Привет, что хочешь сделать?", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Конвертация видео")
async def without_puree(message: types.Message):
    conversion("start_video")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["меню"]
    keyboard.add(*buttons)
    await message.answer("Сконвертированно", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Посмотреть список видео")
async def without_puree(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["меню"]
    keyboard.add(*buttons)
    await message.answer("Все видео на https://disk.yandex.ru/d/hKpsQZ4V0hqV-g", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Рендер всего")
async def without_puree(message: types.Message):
    gluing()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["меню"]
    keyboard.add(*buttons)
    await message.answer(list, reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Рендер)")
async def without_puree(message: types.Message):
    render()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["меню"]
    keyboard.add(*buttons)
    await message.answer("Закончил рендер успешно", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Отправить список")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    temp = os.listdir(r"C:\Users\Kalizek\YandexDisk\Video_volleyball")
    print(temp)
    temp.append("/cancel")
    buttons = temp
    keyboard.add(*buttons)
    await message.answer("Выбери нужное видео", reply_markup=keyboard)
    await Form.name.set()

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["меню"]
    keyboard.add(*buttons)
    await message.answer("Закрыл выбор видео, вернитесь в меню", reply_markup=keyboard)

@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Form.next()
    await message.reply("Напишите отрезок времени")

@dp.message_handler(state=Form.time)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text
        name = data['name']
        time = data['time']
        f = write_csv(name + ","+ time)
        print(f)
        if f == True:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["меню"]
            keyboard.add(*buttons)
            await bot.send_message(message.chat.id, "Ответ записан", reply_markup=keyboard)
            await state.finish()
        if f == False:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["меню"]
            keyboard.add(*buttons)
            await bot.send_message(message.chat.id, "Ошибка ввода, проверьте знак - разделитель (Должна быть \",\"). Проверьте количество цифр", reply_markup=keyboard)
            await state.finish()

# 
@dp.message_handler(lambda message: message.text == "Предложение идей")
async def cmd_start(message: types.Message):
    await bot.send_message(message.chat.id, "Опиши свою идею", reply_markup=types.ReplyKeyboardRemove())
    await Offers.Offer.set()

@dp.message_handler(state=Offers.Offer)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Offer'] = message.text
        name = data['Offer']
        write_csv_Offer(name)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["меню"]
    keyboard.add(*buttons)
    await bot.send_message(message.chat.id, "Ответ записан", reply_markup=keyboard)
    await state.finish()
# 
if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)