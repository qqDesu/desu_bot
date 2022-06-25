from urllib import response
import requests
import telebot
from telebot import types
import json
from configparser import ConfigParser
import redis

parser = ConfigParser()
parser.read("config.txt")
token = parser.get("auth", "token")

bot = telebot.TeleBot(token)

statsDB = redis.Redis(host='redis', port=6379, db=0)
usersDB = redis.Redis(host='redis', port=6379, db=1)

@bot.message_handler(commands=['start'],content_types='text')
def start_message(message):
    bot.send_message(message.chat.id, "Watashi wa Waifu boto, desu! Nice to meet you! Type /waifu to your waifu. FuFuFu... (￣▽￣)ノ")
    
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "Type '/waifu', baka! (・`ω´・)")
    
@bot.message_handler(commands=['waifu'])
def main_menu(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    categories = ['sfw', 'nsfw', 'gif']
    keyboard.add(*categories)
    bot.send_message(message.chat.id, "Category?", reply_markup=keyboard) 
    bot.register_next_step_handler(message, subcategory_select)

def subcategory_select(message):    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if message.text == 'sfw':
        global category
        category = message.text
        
        sfw_tags = ['waifu','neko','shinobu','megumin','bully','cuddle','cry','hug','awoo','kiss','lick','pat','smug','bonk','yeet','blush','smile','wave','highfive','handhold','nom','bite','glomp','slap','kill','kick','happy','wink','poke','dance','cringe', 'Back to main menu']
        keyboard.add(*sfw_tags)
        
        bot.send_message(message.chat.id, "Choose your waifu (￣ω￣)", reply_markup=keyboard)
        bot.register_next_step_handler(message, img_url)

    elif message.text == 'nsfw':
        category = message.text
        
        nsfw_tags = ['waifu','neko','trap','blowjob', 'Back to main menu']
        keyboard.add(*nsfw_tags)
        
        bot.send_message(message.chat.id, "Choose your waifu (￣ω￣)", reply_markup=keyboard)
        bot.register_next_step_handler(message, img_url)

    elif message.text == 'gif':
        
        gif_category = ['sfw', 'nsfw', 'Back to main menu']
        keyboard.add(*gif_category)
        
        bot.send_message(message.chat.id, "Choose your waifu (￣ω￣)", reply_markup=keyboard)
        bot.register_next_step_handler(message, gif_tags_menu)

def back_to_main_menu(message):
    tag = message.text
    if tag == 'Back to main menu':
        bot.send_message(message.chat.id, "Make up your mind already! BAKAYARO ヽ( `д´*)ノ")
        main_menu(message)

def img_url(message):
    back_to_main_menu(message)
    tag = message.text
    response = requests.get(('https://api.waifu.pics/{}/{}').format(category, tag))
    json_url = response.json()
    waifu = json_url['url']
    bot.send_photo(message.chat.id, photo=waifu)
    main_menu(message)

def gif_tags_menu(message):
    back_to_main_menu(message)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    if message.text == 'sfw':
        global category
        category = 'false'
        gif_sfw_tags = ['waifu', 'baka', 'Back to main menu']
        keyboard.add(*gif_sfw_tags)

        bot.send_message(message.chat.id, "Seiso tag? (・о・)", reply_markup=keyboard)
        bot.register_next_step_handler(message, gif_send)
    
    elif message.text == 'nsfw':
        category = 'true'
        gif_nsfw_tags = ['ass', 'hentai', 'milf', 'oral', 'paizuri', 'ecchi', 'ero', 'Back to main menu']
        keyboard.add(*gif_nsfw_tags)

        bot.send_message(message.chat.id, "You perv...heeheehee... ԅ(≖‿≖ԅ)", reply_markup=keyboard)
        bot.register_next_step_handler(message, gif_send)

def gif_send(message):
    back_to_main_menu(message)

    tag = message.text

    if tag == 'baka':
        response = requests.get('https://api.catboys.com/baka')
        json_url = response.json()
        waifu = json_url['url']
        bot.send_animation(message.chat.id, animation=waifu)

    else:    
        response = requests.get(('https://api.waifu.im/random/?is_nsfw={}&selected_tags={}&gif=true').format(category, tag))
        json_url = response.json()
        waifu_url = json_url['images'][0]
        waifu = waifu_url['url']
        bot.send_animation(message.chat.id, animation=waifu)

    main_menu(message)

bot.polling(non_stop=True, interval=0)
