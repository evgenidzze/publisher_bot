from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


kb_manage_channel_inline = InlineKeyboardMarkup(row_width=2)

add_channel_inline = InlineKeyboardButton(text='Додати канал', callback_data='Додати канал')
del_channel = InlineKeyboardButton(text='Видалити канал', callback_data='Видалити канал')
channel_list = InlineKeyboardButton(text='Список каналів', callback_data='Список каналів')
cancel = InlineKeyboardButton(text='Відміна', callback_data='Відміна')

kb_manage_channel_inline.add(add_channel_inline, del_channel, channel_list, cancel)

kb_manage_channel = ReplyKeyboardMarkup(resize_keyboard=True)
channel_menu = KeyboardButton(text='Канали')
create_post = KeyboardButton(text='Створити пост')
kb_manage_channel.add(channel_menu, create_post)

cancel_kb = InlineKeyboardMarkup()
cancel_kb.add(cancel)

post_formatting_kb = InlineKeyboardMarkup()
date_choose = InlineKeyboardButton(text='Запланувати', callback_data='Запланувати')
add_media = InlineKeyboardButton(text='Додати медіа', callback_data='Додати медіа')
continue_button = InlineKeyboardButton(text='Продовжити »', callback_data='Продовжити')
post_formatting_kb.add(date_choose, add_media, continue_button)

