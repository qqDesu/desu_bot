import requests
import telebot
from telebot import types
import json
from configparser import ConfigParser

parser = ConfigParser()
parser.read("config.txt")
token = parser.get("auth", "token")

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'],content_types='text')
def start_message(message):
    bot.send_message(message.chat.id, "Watashi wa Waifu boto, desu! Nice to meet you! Type /waifu to your waifu. FuFuFu... (￣▽￣)ノ")
    
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "Type '/waifu', baka! (・`ω´・)")
    
@bot.message_handler(commands=['waifu'])
def main_category_select(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    categories = ['sfw', 'nsfw']
    keyboard.add(*categories)
    bot.send_message(message.chat.id, "Category?", reply_markup=keyboard) 
    bot.register_next_step_handler(message, subcategory_select)

def subcategory_select(message):    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    if message.text == 'sfw':
        global category
        category = message.text
        
        sfw_categories = ['waifu','neko','shinobu','megumin','bully','cuddle','cry','hug','awoo','kiss','lick','pat','smug','bonk','yeet','blush','smile','wave','highfive','handhold','nom','bite','glomp','slap','kill','kick','happy','wink','poke','dance','cringe', 'Back to main menu']
        keyboard.add(*sfw_categories)
        
        bot.send_message(message.chat.id, "Choose your waifu (￣ω￣)", reply_markup=keyboard)
        bot.register_next_step_handler(message, waifu_url)


    elif message.text == 'nsfw':
        category = message.text
        
        nsfw_categories = ['waifu','neko','trap','blowjob', 'Back to main menu']
        keyboard.add(*nsfw_categories)
        
        bot.send_message(message.chat.id, "Choose your waifu (￣ω￣)", reply_markup=keyboard)
        bot.register_next_step_handler(message, waifu_url)

def waifu_url(message):
    subcategory = message.text
    if subcategory == 'Back to main menu':
        bot.send_message(message.chat.id, "Make up your mind already! BAKAYARO ヽ( `д´*)ノ")
        main_category_select(message)
        
        
    else:
        response = requests.get(('https://api.waifu.pics/{}/{}').format(category, subcategory))
        json_url = response.json()
        waifu = json_url['url']
        bot.send_photo(message.chat.id, photo=waifu)
        main_category_select(message)

bot.polling(non_stop=True, interval=0)