#!/usr/bin/python3
import os, csv
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

# Этот файл программы должен храниться на Rasberry. Он овечает за постоянное
# общение с клиентами телеграмм бота и за получение списков от них.
# После получения списков эта программа отправляет CSV файлы на пк (в PC.py)

bot = Bot("5119368416:AAFyMffcZMb8WztB-RVldWmmNAK47y5qjFg")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage) #создание бота (задаем токен, определяем хранилище)

def write_csv_Offer(name): # Запись замечаний и предложений в файл Offer.csv
    temp = []
    temp.append(name)
    with open("/home/myprogramm/Offer.csv", 'a', newline = '', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=";")
                    writer.writerow([temp[0]])

def write_csv(name): # Проверка на правильность ввода и запись таймингов в DB.csv
    mas = name.split(",")
    temp = []
    print(mas)
    print(len(mas))
    try:
        if (len(mas) % 2 == 0 and len(mas) >= 2):
            return(False)
        for i in range(1,len(mas)):
            if ":" in mas[i]:
                temp = mas[i].split(":")
                mas[i] = int(temp[0]) * 60 + int(temp[1])
                print(mas[i])
        with open("/home/myprogramm/DB.csv", 'a', newline = '', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=";")
                    for i in range(1,len(mas)-1, 2):
                        print(i)
                        writer.writerow([mas[0],mas[i],mas[i+1]])
                    return(True)
    except:
        return(False)

class Form(StatesGroup): # Создание класа для получения сообщений - ответов (данная форма нужна для получения списка)
    name = State() # Название видео
    time = State() # Получение времени

class Offers(StatesGroup):
    Offer = State() # Получение ответа с пожеланием или предложением

class Video_ID(StatesGroup):
    id = State() # Получение ответа с пожеланием или предложением

def read_txt(text): # Чтение txt файлов, где записанны сообщения
    file_open = open("messages/" + text,"r",encoding="utf-8")
    text = file_open.read()
    return(text)

@dp.message_handler(commands=['start']) # Указания на реагирование если поступила команда "/start"
async def menu(message):
    start_menu = types.ReplyKeyboardMarkup(True, True) # Создание массива типа клавиатура
    start_menu.row('меню') # Добавление кнопки "Меню"
    await bot.send_message(message.chat.id,read_txt("welcome_message.txt"), reply_markup=start_menu) # Выводим сообщение из "welcome_message.txt" и клавиатуру


@dp.message_handler(commands=['help'])
async def menu(message):
    start_menu = types.ReplyKeyboardMarkup(True, True)
    start_menu.row('меню')
    await bot.send_message(message.chat.id,"заглушечка)", reply_markup=start_menu)

@dp.message_handler(lambda message: message.text == "меню") # Указания на реагирование если поступил текст "меню" (Нажатие на кнопку "меню", которую 
async def cmd_start(message: types.Message):                # мы выводим в 64,65,66 строчках является вводом текста), так же пользователь может просто написать "меню"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True) # Создание клавиатуры
    buttons = ["Посмотреть список видео", "Отправить список","Предложение идей"] # Добавление кнопок (Клавиатура - это массив)
    keyboard.add(*buttons) # Добавление массива кнопок в массив "keyboard"
    await message.answer("Привет, что хочешь сделать?", reply_markup=keyboard) # Вывод сообщения и вывод клавиатуры

@dp.message_handler(lambda message: message.text == "Админка") # Аналогично строке 75
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Загрузка видео"]
    keyboard.add(*buttons)
    await message.answer("Привет, что хочешь сделать?", reply_markup=keyboard)

# Доработка после изучения библиотеки Socket

@dp.message_handler(lambda message: message.text == "Посмотреть список видео") # Аналогично строке 75
async def without_puree(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["меню"]
    keyboard.add(*buttons)
    await message.answer("Все видео на https://disk.yandex.ru/d/hKpsQZ4V0hqV-g", reply_markup=keyboard)


# Доработка после изучения библиотеки Socket
@dp.message_handler(lambda message: message.text == "Отправить список") # При поступлении команды "Отправить список"
async def cmd_start(message: types.Message):
    global video_id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    print(video_id)
    buttons = video_id
    keyboard.add(*buttons)
    await message.answer("Выбери нужное видео", reply_markup=keyboard) # Выводим клавиатуру
    await Form.name.set() # Начинаем опрос созданный на 50 строчке

@dp.message_handler(state='*', commands='cancel') # Если команда "Закрыть" то прекращаем опрос (state.finish()) игнорируя стадию,предлагаем кнопку "меню"
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

@dp.message_handler(state=Form.name) # после начала опроса (133 строчка) программы ожидает ввод "name", если опрос не завершен функцией на 135 строчке
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text # Полученное сообщение = name
    await Form.next() # Переходим к следующему этапу
    await message.reply("Напишите отрезок времени")

@dp.message_handler(state=Form.time) # Следующий этап опроса, пользователь вводит время
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text # Время = полученное сообщение 
        name = data['name']
        time = data['time']
        f = write_csv(name + ","+ time) # Отправка названия видео и времени в запись CSV, получение ответа от функуции True - записл, False - ошибка ввода
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

@dp.message_handler(lambda message: message.text == "Загрузка видео") # Аналогично 124 строчке
async def cmd_start(message: types.Message):
    await bot.send_message(message.chat.id, "Напиши список видео", reply_markup=types.ReplyKeyboardRemove())
    await Video_ID.id.set()

@dp.message_handler(state=Video_ID.id)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        global video_id
        data['Offer'] = message.text
        name = data['Offer']
        video_id = name.split(" ")
        video_id.append("/cancel")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["меню"]
    keyboard.add(*buttons)
    await bot.send_message(message.chat.id, "Ответ записан", reply_markup=keyboard)
    await state.finish()

@dp.message_handler(lambda message: message.text == "Предложение идей") # Аналогично 124 строчке
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

if __name__ == "__main__": # Запуск бота (обязательно в конце программы)
    executor.start_polling(dp, skip_updates=True)