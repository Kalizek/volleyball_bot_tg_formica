import csv
import os
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InputFile
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from numpy import meshgrid
from data import Token
bot = Bot(Token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


#Загрузка файла пользователю

# @dp.message_handler(lambda message: message.text == "меню")
# async def cmd_start(message: types.Message):
#     await bot.send_document(message.chat.id, open("Имя файлы", 'rb'))
#     await message.answer("Привет, что хочешь сделать?")

@dp.message_handler(lambda message: message.text == "меню")
async def cmd_start(message: types.Message):
    file_id=message.document
    file = await bot.get_file(file_id)
    file_path = file.file_path




if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
