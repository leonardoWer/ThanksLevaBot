import telebot
from telebot import types
import requests
import json

bot = telebot.TeleBot("")
API = ""

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.username}!")
    bot.send_message(message.chat.id, "Я твой личный бот <b>Спасибо Лёва!</b>", parse_mode="html")
    bot.send_message(message.chat.id, "Я буду помогать тебе <em>в чём захочешь</em>", parse_mode="html")

    markup = types.InlineKeyboardMarkup()
    btn_weather_spb = types.InlineKeyboardButton("Погода в Санкт-Петербурге", callback_data="weather_spb")
    btn_weather_sites = types.InlineKeyboardButton("Прогноз погоды на несколько дней", callback_data="weather_sites")
    btn_weather_city = types.InlineKeyboardButton("Прогноз погоды в другом городе", callback_data="weather_city")
    markup.add(btn_weather_spb)
    markup.add(btn_weather_sites)
    markup.add(btn_weather_city)
    
    bot.send_message(message.chat.id, "Вот чему Лёва меня уже научил: ", reply_markup=markup)

    
@bot.callback_query_handler(func = lambda callback: True)
def callback_message(callback):
    message = callback.message
    if callback.data == "weather_spb":
        weather_spb(message)
    elif callback.data == "weather_sites":
        weather_sites(message)
    elif callback.data == "weather_city":
        weather_city(message)


@bot.message_handler(commands=["hello"])
def main(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.username}!")
    
    markup = types.ReplyKeyboardMarkup()
    btn_weather_spb = types.KeyboardButton("Погода в Санкт-Петербурге")
    btn_weather_sites = types.KeyboardButton("Сайты с погодой")
    btn_weather_city = types.InlineKeyboardButton("Прогноз погоды в другом городе")
    markup.add(btn_weather_spb)
    markup.add(btn_weather_sites)
    markup.add(btn_weather_city)

    bot.send_message(message.chat.id, "Чем могу помочь?", reply_markup=markup)

    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == "Погода в Санкт-Петербурге":
        weather_spb(message)
    elif message.text == "Сайты с погодой":
        weather_sites(message)
    elif message.text == "Прогноз погоды в другом городе":
        weather_city(message)
    else:
        bot.reply_to(message, "Нет такой команды")



@bot.message_handler(commands=["weather_spb"])
def weather_spb(message):
    city = "Санкт-Петербург"
    weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric")
    if weather.status_code == 200:
        data = json.loads(weather.text)
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"]

        image = take_image(description)
        file = open(r"C:\Python\ITMO\Proga\lab0\Thanks Leva Bot\weatherphoto\\"+image,"rb")
        bot.send_photo(message.chat.id, file)

        bot.reply_to(message, f"Погода в Санкт-Петербурге сейчас:\n {temp} градусов\n Ощущается как: {feels_like} градусов\n Состояние: {description}")
    else:
        bot.reply_to(message, "Сервер с погодой не отвечает")



@bot.message_handler(commands=["weather_sites"])
def weather_sites(message):
    
    markup = types.InlineKeyboardMarkup()
    buttonyand = types.InlineKeyboardButton("Яндекс", url = "https://yandex.ru/pogoda/saint-petersburg")
    buttongis = types.InlineKeyboardButton("Gismeteo", url = "https://www.gismeteo.ru/weather-sankt-peterburg-4079/")
    buttonworldweather = types.InlineKeyboardButton("WorldWeather", url = "https://world-weather.ru/pogoda/russia/saint_petersburg/24hours/")
    markup.add(buttonyand)
    markup.add(buttongis)
    markup.add(buttonworldweather)
    bot.send_message(message.chat.id, "Сайты с погодой:", reply_markup=markup)


@bot.message_handler(commands=["weather_city"])
def weather_city(message):
    bot.send_message(message.chat.id, "Напиши название города")
    bot.register_next_step_handler(message, get_city)

def get_city(message):
    city = message.text.strip().lower()
    weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric")
    if weather.status_code == 200:
        data = json.loads(weather.text)
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"]

        image = take_image(description)
        file = open(r"C:\Python\ITMO\Proga\lab0\Thanks Leva Bot\weatherphoto\\"+image,"rb")
        bot.send_photo(message.chat.id, file)
        
        bot.reply_to(message, f"Погода в {city} сейчас:\n {temp} градусов\n Ощущается как: {feels_like} градусов\n Состояние: {description}")
    else:
        bot.reply_to(message, "Такого города нет, попробуйте указать название ещё раз")

def take_image(description):
    if description == "clear sky":
        return "sun_weather_icon.png"
    elif description == "few clouds":
        return "sunny_weather_icon.png"
    elif description == "scattered clouds":
        return "cloud_weather_icon.png"
    elif description == "broken clouds":
        return "cloudy_weather_icon.png"
    elif description == "shower rain":
        return "rain_weather_icon.png"
    elif description == "rain":
        return "rain_weather_icon.png"
    elif description == "thunderstorm":
        return "lightning_weather_icon.png"
    elif description == "snow":
        return "snow_weather_icon.png"
    elif description == "mist":
        return "cloudy_weather_icon.png"
    else:
        return "non_image.png"
    

@bot.message_handler(content_types=["text"])
def reaction(message):
    if message.text.lower() == "спасибо":
        bot.reply_to(message, "Спасибо Лёва!")
    elif message.text == "Погода в Санкт-Петербурге" or message.text == "Сайты с погодой" or message.text == "Прогноз погоды в другом городе":
        on_click(message)


bot.polling(none_stop=True)
