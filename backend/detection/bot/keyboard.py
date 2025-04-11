from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_inline_keyboard(pk):
    keyboard_inline = InlineKeyboardMarkup()
    btn_link = InlineKeyboardButton(
        "🌐Детальніше", 
        url=f"http://127.0.0.1:8000/statistics/detection/{pk}/"
    )
    keyboard_inline.add(btn_link)
    return keyboard_inline