from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, BotCommand

kb_manage_channel_inline = InlineKeyboardMarkup(row_width=2)

add_channel_inline = InlineKeyboardButton(text='Додати канал', callback_data='Додати канал')
del_channel = InlineKeyboardButton(text='❌ Видалити канал', callback_data='Видалити канал')
channel_list = InlineKeyboardButton(text='Список каналів', callback_data='Список каналів')

kb_manage_channel_inline.add(add_channel_inline, del_channel, channel_list)

main_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
channel_menu = KeyboardButton(text='Канали')
create_post = KeyboardButton(text='Створити пост')
edit_post = KeyboardButton(text='Змінити пост')
media_base = KeyboardButton(text='База медіа')
main_kb.add(create_post, channel_menu, edit_post, media_base)

cancel_kb = InlineKeyboardMarkup()
cancel = InlineKeyboardButton(text='Відміна', callback_data='Відміна')
cancel_kb.add(cancel)

post_formatting_kb = InlineKeyboardMarkup(row_width=2)
post_formating_job_kb = InlineKeyboardMarkup(row_width=2)
make_plan = InlineKeyboardButton(text='🗓 Запланувати', callback_data='Запланувати')
post_loop = InlineKeyboardButton(text='🌀 Зациклити', callback_data='Зациклити')
change_text = InlineKeyboardButton(text='📃 Змінити текст', callback_data='Змінити текст')
post = InlineKeyboardButton(text='Опублікувати зараз 🚀', callback_data='post_now_menu')
del_post = InlineKeyboardButton(text='❌ Видалити пост', callback_data='delete_post')
media_settings = InlineKeyboardButton(text='🎞 Налаштувати медіа', callback_data='Налаштувати медіа')

post_formatting_kb.add(make_plan, post_loop, change_text, post)
post_formating_job_kb.add(make_plan, post_loop, change_text, del_post, media_settings, post)

create_post_inline_kb = InlineKeyboardMarkup()
create_post_inline = InlineKeyboardButton(text='Створити пост', callback_data='Створити пост')
create_post_inline_kb.add(create_post_inline)

media_choice_kb = InlineKeyboardMarkup(row_width=2)
take_from_db = InlineKeyboardButton(text='Обрати з бази', callback_data='take_from_db')
send_by_self = InlineKeyboardButton(text='Додати самостійно', callback_data='send_by_self')
remove_media = InlineKeyboardButton(text='❌ Видалити медіа', callback_data='remove_media')
back = InlineKeyboardButton(text='« Назад', callback_data='back')
media_choice_kb.add(take_from_db, send_by_self, remove_media)

back_kb = InlineKeyboardMarkup()
back_kb.add(back)

base_manage_panel_kb = InlineKeyboardMarkup(row_width=2)
create_catalog = InlineKeyboardButton(text='Створити каталог', callback_data='Створити каталог')
edit_catalog = InlineKeyboardButton(text='Редагувати каталог', callback_data='edit_cat')
catalog_list_inline = InlineKeyboardButton(text='Оглянути каталоги', callback_data='cat_list')
delete_catalog_inline = InlineKeyboardButton(text='❌ Видалити каталог', callback_data='delete_cat')
base_manage_panel_kb.add(create_catalog, edit_catalog, catalog_list_inline, delete_catalog_inline)

add_to_cat_kb = InlineKeyboardMarkup(row_width=3)
add_video_img = InlineKeyboardButton(text='Відео/Фото/GIF', callback_data='Відео/Фото/GIF')
add_audio_voice = InlineKeyboardButton(text='Аудіо/Голосове', callback_data='Аудіо/Голосове')
add_file = InlineKeyboardButton(text='Файл', callback_data='Файл')
add_to_cat_kb.add(add_video_img, add_audio_voice, add_file)

no_text_kb = InlineKeyboardMarkup()
no_text_kb.add(InlineKeyboardButton(text='Без тексту', callback_data='no_text'))

del_voice_kb = InlineKeyboardMarkup()
del_voice_kb.add(InlineKeyboardButton(text='Так', callback_data='yes'))
del_voice_kb.add(InlineKeyboardButton(text='Ні', callback_data='no'))

edit_catalog_kb = InlineKeyboardMarkup()
edit_catalog_kb.add(InlineKeyboardButton(text='Додати медіа', callback_data='add_cat_media'),
                    InlineKeyboardButton(text='Видалити медіа', callback_data='del_cat_media'))

# remove_media_cat_type = InlineKeyboardMarkup()
video_type = InlineKeyboardButton(text='Відео', callback_data='videos')
photo_type = InlineKeyboardButton(text='Фото', callback_data='photos')
animation_type = InlineKeyboardButton(text='GIF', callback_data='gifs')
voice_type = InlineKeyboardButton(text='Голосове', callback_data='voices')
document_type = InlineKeyboardButton(text='Файл', callback_data='documents')
v_note_type = InlineKeyboardButton(text='Відеоповідомлення', callback_data='video_notes')

planning_kb = InlineKeyboardMarkup(row_width=2)
date_choose = InlineKeyboardButton(text='Обрати дату/час', callback_data='choose_date')
planning_kb.add(date_choose, media_settings, back)

loop_kb = InlineKeyboardMarkup(row_width=2)
date_choose = InlineKeyboardButton(text='Обрати час', callback_data='choose_loop_time')
loop_kb.add(date_choose, media_settings, back)

post_now_kb = InlineKeyboardMarkup(row_width=2)
post_now = InlineKeyboardButton(text='Опублікувати зараз 🚀', callback_data='Опублікувати')
post_now_kb.add(post_now, media_settings, back)

change_post_kb = InlineKeyboardMarkup()
change_post = InlineKeyboardButton(text='Змінити пост', callback_data='Змінити пост')
change_post_kb.add(change_post)

change_create_post_kb = InlineKeyboardMarkup()
change_create_post_kb.add(create_post_inline, change_post)

self_or_random_kb = InlineKeyboardMarkup(row_width=2)
random_inline = InlineKeyboardButton(text='Рандом медіа', callback_data='random_media')
self_media_inline = InlineKeyboardButton(text='Обрати самому', callback_data='self_media')
self_or_random_kb.add(random_inline, self_media_inline)

loop_media_kb = InlineKeyboardMarkup(row_width=2)
back_loop = InlineKeyboardButton(text='« Назад', callback_data='Зациклити')
loop_media_kb.insert(take_from_db)
loop_media_kb.add(back_loop, remove_media)

planned_media_kb = InlineKeyboardMarkup(row_width=2)
back_planned = InlineKeyboardButton(text='« Назад', callback_data='Запланувати')
planned_media_kb.add(take_from_db, send_by_self, back_planned, remove_media)

now_media_kb = InlineKeyboardMarkup(row_width=2)
back_now = InlineKeyboardButton(text='« Назад', callback_data='post_now_menu')
now_media_kb.add(take_from_db, send_by_self, back_now, remove_media)




def add_posts_to_kb(jobs, edit_kb):
    for j in jobs:
        date_p: datetime = j.next_run_time
        job_data = j.kwargs['data']

        if not job_data.get('post_text'):
            job_post_text = ''
        else:
            job_post_text = f'- "{job_data.get("post_text")}"'
        trigger_name = str(j.trigger).split('[')[0]
        if trigger_name == 'date':
            text = f"Пост {date_p.date()} о {date_p.strftime('%H:%M')} {job_post_text}"
        elif trigger_name == 'cron':
            text = f"Кожного дня о {date_p.strftime('%H:%M')} {job_post_text}"
        else:
            text = 'Без імені'

        edit_kb.add(InlineKeyboardButton(text=text,
                                         callback_data=j.id))


media_types = {"videos": video_type, "photos": photo_type, "gifs": animation_type, "voices": voice_type,
               "documents": document_type, 'video_notes': v_note_type}


def cat_types_kb(cat_data_types):
    kb = InlineKeyboardMarkup()
    for data_type in cat_data_types:
        kb.add(media_types[data_type])
    return kb
