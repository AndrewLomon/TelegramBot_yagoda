# This is a new Telegram Bot  - Education version
import time
import logging
from aiogram import Bot, Dispatcher, executor, types
from Config import TOKEN
import MessageBox


#Just warning that bot is working
print('Okay, lets go!')

# These are constant variables
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


# Here are all functions that bot is using
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    await message.answer(f'Привествую, {user_full_name}!\nКак я могу быть тебе полезен?\nУзнать список моих команд, ты можешь командой\n/help')
    await message.delete()

@dp.message_handler(commands=['help'])
async def command_help(message:types.Message):
    await message.reply(text=MessageBox.HELP_MESSAGE)
    await message.delete()

@dp.message_handler(commands=['info'])
async def command_info(message:types.Message):
    await message.reply(text=MessageBox.INFO_MESSAGE)
    await message.delete()




if __name__ == '__main__':
    executor.start_polling(dp)
