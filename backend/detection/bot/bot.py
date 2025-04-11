from celery import shared_task
import telebot

import os
import time
from backend.settings import BOT_TOKEN, ADMINS_ID
from detection.bot.keyboard import get_inline_keyboard

bot = telebot.TeleBot(BOT_TOKEN)


@shared_task
def send_msg(photo_path, pk):

    keyboard_inline = get_inline_keyboard(pk) 
    
    for admin_id in ADMINS_ID:
        with open(f"{photo_path}", 'rb') as photo:
            caption = "Виявлено об'єкт"
            bot.send_photo(admin_id, photo, caption=caption,reply_markup=keyboard_inline)
            
        
