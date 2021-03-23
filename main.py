import logging
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, getWeather
import json

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    if message.text == '/start':
        await bot.send_sticker(message.chat.id,
                               sticker='CAACAgIAAxkBAAEIvIBgVNZjagxkOvlvXi7anBFll4Ls5AACZwADHwFMFQMvnzs0dPL6HgQ')
        await message.reply('Salom ' + message.from_user.first_name + '. Botimizga xush kelibsiz!')
    else:
        await message.reply("Bu dunyoning istalgan joyida ob-xavo ma'lumotlarini ko'rishingiz mumkun bo'lgan bot.")


def get_response(city):
    r = getWeather(city)
    return r


city = ''


@dp.message_handler(lambda message: message.text not in ['Maximal temperature', 'Minimal temperature', 'Wind speed', 'Pressure', 'Humidity', 'Cancel'])
async def echo(message: types.Message):
    global city
    city = message.text

    r = get_response(city)
    if r.status_code == 200:
        response = json.loads(r.content)

        temp = str(response['main']['temp'])

        msg = 'The current weather in ' + city + ' ' + temp + '°C'
        # inline = types.InlineKeyboardMarkup()
        # max_temp_keyboard = types.InlineKeyboardButton(text='Maximal temperature', callback_data='max')
        # min_temp_keyboard = types.InlineKeyboardButton(text='Minimal temperature', callback_data='min')
        # wind_speed_keyboard = types.InlineKeyboardButton(text='Wind speed', callback_data='wind')
        # pressure_keyboard = types.InlineKeyboardButton(text='Pressure', callback_data='pressure')
        # humidity_keyboard = types.InlineKeyboardButton(text='Humidity', callback_data='humidity')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        max_temp_keyboard = types.KeyboardButton(text='Maximal temperature')
        min_temp_keyboard = types.KeyboardButton(text='Minimal temperature')
        wind_speed_keyboard = types.KeyboardButton(text='Wind speed')
        pressure_keyboard = types.KeyboardButton(text='Pressure')
        humidity_keyboard = types.KeyboardButton(text='Humidity')
        cancel = types.KeyboardButton(text='Cancel')

        keyboard.add(max_temp_keyboard, min_temp_keyboard)
        keyboard.add(wind_speed_keyboard, pressure_keyboard, humidity_keyboard)
        keyboard.add(cancel)

        await message.answer(msg, reply_markup=keyboard)

    else:
        await bot.send_sticker(message.chat.id,
                               sticker='CAACAgIAAxkBAAEIvJRgVNnTXeGXptOG8HGwjQYu3XZLXgACAQADr8ZRGhLj3-N0EyK_HgQ')
        await message.answer("⚠️Something is wrong! Please check your of your city. ⚠")


@dp.message_handler(lambda message: message.text in ['Maximal temperature', 'Minimal temperature', 'Wind speed', 'Pressure', 'Humidity', 'Cancel'])
async def weather(msg: types.Message):
    global m, markup
    text = msg.text
    r = get_response(city)
    if r.status_code == 200:
        res = json.loads(r.content)

        max_temp = str(res['main']['temp_max'])
        min_temp = str(res['main']['temp_min'])
        wind_speed = str(res['wind']['speed'])
        pressure = str(res['main']['pressure'])
        humidity = str(res['main']['humidity'])
        markup = None
        if text == 'Maximal temperature':
            m = "Maximal temperature is " + max_temp + '°C'
        elif text == 'Minimal temperature':
            m = 'Minimal temperature is ' + min_temp + '°C'
        elif text == 'Wind speed':
            m = 'Wind speed is ' + wind_speed + 'm/s'
        elif text == 'Pressure':
            m = 'Pressure is ' + pressure
        elif text == 'Humidity':
            m = 'Humidity is ' + humidity + 'mm'
        else:
            m = 'Cancelled'
            markup = types.ReplyKeyboardRemove()

    if markup is not None:
        await msg.answer(m, reply_markup=markup)
    else:
        await msg.answer(m)

    # @dp.callback_query_handler()
    # async def query_handler(call):
    #     if call.data == 'max':
    #         m = "Maximal temperature is " + str(max_temp) + 'C'
    #     elif call.data == 'min':
    #         m = 'Minimal temperature is ' + str(min_temp) + 'C'
    #     elif call.data == 'wind':
    #         m = 'Wind speed is ' + str(wind_speed) + 'm/s'
    #     elif call.data == 'pressure':
    #         m = 'Pressure is ' + str(pressure)
    #     else:
    #         m = 'Humidity is ' + str(humidity) + 'mm'
    #     await message.answer(m)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
