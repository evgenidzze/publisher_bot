from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


#
kb_manage_user = InlineKeyboardMarkup(row_width=2)
add_user = InlineKeyboardButton(text='Додати користувача', callback_data='Додати користувача')
del_user = InlineKeyboardButton(text='Видалити користувача', callback_data='Видалити користувача')
user_list = InlineKeyboardButton(text='Список користувачів', callback_data='Список користувачів')
cancel = InlineKeyboardButton(text='Відміна', callback_data='Відміна')
kb_manage_user.add(add_user, del_user, user_list, cancel)


