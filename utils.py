import asyncio
import json
import random
import aiogram_timepicker
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from create_bot import bot
from json_functionality import get_all_channels, get_users_dict, get_media_from_base
from aiogram.dispatcher.middlewares import BaseMiddleware

aiogram_timepicker.panel.full._default['select'] = 'Обрати'
aiogram_timepicker.panel.full._default['cancel'] = 'Скасувати'


class AuthMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):

        if update.callback_query:
            if str(update.callback_query.from_user.id) not in get_users_dict():
                await update.callback_query.message.answer(
                    text='У вас немає доступу до бота. Після отримання доступу від адміністратора, натисніть на команду /start',
                    reply_markup=ReplyKeyboardRemove())
                raise CancelHandler()
        else:
            if str(update.message.from_user.id) not in get_users_dict():
                await update.message.answer(
                    text='У вас немає доступу до бота. Після отримання доступу від адміністратора, натисніть на команду /start',
                    reply_markup=ReplyKeyboardRemove())
                raise CancelHandler()


def pressed_back_button(message):
    if isinstance(message, types.CallbackQuery):
        call: types.CallbackQuery = message
        if call.data == 'back':
            return True
        else:
            return False


def add_random_media(media_files, data, cat_name):
    random_photos_number = data.get('random_photos_number')
    random_videos_number = data.get('random_videos_number')

    if random_photos_number:
        r_photos = get_random_photos(count=int(random_photos_number), cat_name=cat_name)
        for rand_photo in r_photos:
            media_files.attach_photo(rand_photo)

    if random_videos_number:
        r_videos = get_random_videos(count=int(random_videos_number), cat_name=cat_name)
        for rand_video in r_videos:
            media_files.attach_video(rand_video)


async def send_message_time(callback_query: CallbackQuery, data):
    channel_id = data.get('channel_id')
    post_text = data.get('post_text')
    media_files = data.get('loaded_post_files')
    voice = data.get('voice')
    video_note = data.get('video_note')
    cat_name = data.get('choose_catalog')
    if not media_files and (data.get('random_photos_number') or data.get('random_videos_number')):
        media_files = types.MediaGroup()
        add_random_media(media_files=media_files, data=data, cat_name=cat_name)

    if media_files:
        await bot.send_media_group(chat_id=channel_id, media=media_files)
    elif voice:
        await bot.send_voice(chat_id=channel_id, voice=voice)
    elif video_note:
        await bot.send_video_note(chat_id=channel_id, voice=video_note)
    else:
        await bot.send_message(chat_id=channel_id, text=post_text)


async def send_message_cron(callback_query: CallbackQuery, data):
    channel_id = data.get('channel_id')
    post_text = data.get('post_text')
    media_files: types.MediaGroup = data.get('loaded_post_files')
    voice = data.get('voice')
    video_note = data.get('video_note')
    cat_name = data.get('choose_catalog')

    if not media_files and (data.get('random_photos_number') or data.get('random_videos_number')):
        media_files = types.MediaGroup()
        add_random_media(media_files=media_files, data=data, cat_name=cat_name)

    random_number = random.randint(0, 4)
    print(f"post in {random_number} minutes")
    if media_files:
        await asyncio.sleep(random_number * 60)
        await callback_query.bot.send_media_group(chat_id=channel_id, media=media_files)
    elif voice:
        await asyncio.sleep(random_number * 60)
        await callback_query.bot.send_voice(chat_id=channel_id, voice=voice)
    elif video_note:
        await asyncio.sleep(random_number * 60)
        await callback_query.bot.send_video_note(chat_id=channel_id, video_note=video_note)
    else:
        await asyncio.sleep(random_number * 60)
        await callback_query.bot.send_message(chat_id=channel_id, text=post_text)


async def kb_channels(message, bot):
    kb_all_channels = InlineKeyboardMarkup(row_width=1)
    all_channels_list = get_all_channels(message.from_user.id)
    kb_channels_list = []

    for channel_id in all_channels_list:
        channel = await bot.get_chat(channel_id)
        channel_name = channel.title
        kb_channels_list.append(InlineKeyboardButton(text=channel_name, callback_data=channel_id))
    kb_all_channels.add(*kb_channels_list)
    return kb_all_channels


def del_list_duplicates(l: list) -> list:
    seen_ids = set()
    result = []
    for item in l:
        unique_id = item["photo"][0]["file_unique_id"]
        if unique_id not in seen_ids:
            seen_ids.add(unique_id)
            result.append(item)
    return result


async def send_voice_from_audio(message: types.Message, bot):
    file_info = await bot.get_file(message.audio.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    return await message.answer_voice(downloaded_file)


async def restrict_media(messages, state, data, post_formatting_kb):
    # якщо надсилаємо (відео фото документ) при цьому войс у даних - заборонити
    if messages[0].content_type in ('video', 'photo', 'document') and 'voice' in data:
        await messages[0].answer(text='❌ Голосове повідомлення не можна публікувати у групі з іншими медіа',
                                 reply_markup=post_formatting_kb)
        await state.reset_state(with_data=False)
        return True
    if messages[0].content_type in ('audio', 'voice'):
        if 'loaded_post_files' in data:
            await messages[0].answer(text='❌ Голосове повідомлення не можна публікувати у групі з іншими медіа',
                                     reply_markup=post_formatting_kb)
            await state.reset_state(with_data=False)
            return True

        if len(messages) > 1:
            await messages[0].answer(text='❌ У пості може бути тільки 1 голосове.',
                                     reply_markup=post_formatting_kb)
            await state.reset_state(with_data=False)
            return True
    if data.get('voice'):
        await messages[0].answer(text='❌ У пості може бути тільки 1 голосове.',
                                 reply_markup=post_formatting_kb)
        await state.reset_state(with_data=False)
        return True


def set_caption(media, text):
    for m in range(len(media.media)):
        if m > 0:
            if 'caption' in media.media[m]:
                media.media[m].caption = None
        else:
            media.media[m].caption = text


async def send_post(post_media_files, post_text, bot, channel_id, post_voice, post_video_note):
    if post_media_files:
        set_caption(text=post_text, media=post_media_files),
        await bot.send_media_group(chat_id=channel_id, media=post_media_files)
    elif post_voice:
        await bot.send_voice(chat_id=channel_id, voice=post_voice, caption=post_text)
    elif post_video_note:
        await bot.send_video_note(chat_id=channel_id, video_note=post_video_note)
    else:
        await bot.send_message(chat_id=channel_id, text=post_text)


async def cat_content(call: types.CallbackQuery, catalog_data: dict, media_type: str = None):
    for media in catalog_data:
        if media == 'videos':
            if media == media_type:
                for video_num in range(len(catalog_data[media])):
                    await call.message.answer_video(video=catalog_data[media][video_num], caption=str(video_num + 1))
                return
            elif not media_type:
                for video in catalog_data[media]:
                    await call.message.answer_video(video=video)
        elif media == 'photos':
            if media == media_type:
                for photo_num in range(len(catalog_data[media])):
                    await call.message.answer_photo(photo=catalog_data[media][photo_num], caption=str(photo_num + 1))
                return
            elif not media_type:
                for photo in catalog_data[media]:
                    await call.message.answer_photo(photo=photo)
        elif media == 'voices':
            if media == media_type:
                for voice_num in range(len(catalog_data[media])):
                    await call.message.answer_voice(voice=catalog_data[media][voice_num], caption=str(voice_num + 1))
                return
            elif not media_type:
                for voice in catalog_data[media]:
                    await call.message.answer_voice(voice=voice)
        elif media == 'documents':
            if media == media_type:
                for document_num in range(len(catalog_data[media])):
                    await call.message.answer_document(document=catalog_data[media][document_num],
                                                       caption=str(document_num + 1))
                return
            elif not media_type:
                for document in catalog_data[media]:
                    await call.message.answer_document(document=document)
        elif media == 'gifs':
            if media == media_type:
                for gif_num in range(len(catalog_data[media])):
                    await call.message.answer_animation(animation=catalog_data[media][gif_num],
                                                        caption=str(gif_num + 1))
                return
            elif not media_type:
                for gif in catalog_data[media]:
                    await call.message.answer_animation(animation=gif)

        elif media == 'video_notes':
            if media == media_type:
                for video_note_num in range(len(catalog_data[media])):
                    await call.message.answer_video_note(video_note=catalog_data[media][video_note_num])
                    await call.message.answer(text=str(video_note_num + 1))
                return
            elif not media_type:
                for video_note in catalog_data[media]:
                    await call.message.answer_video_note(video_note=video_note)


def get_random_photos(count, cat_name) -> list:
    with open('data.json', 'r', encoding='utf-8') as file:
        file_data = json.load(file)
        res = []
        photos_id = file_data['catalogs'][cat_name]['photos']
        print(count)
        print(photos_id)
        random.shuffle(photos_id)
        for i in range(count):
            res.append(photos_id[i])
        return res


def get_random_videos(count, cat_name) -> list:
    with open('data.json', 'r', encoding='utf-8') as file:
        file_data = json.load(file)
        res = []
        videos_id = file_data['catalogs'][cat_name]['videos']
        print(count)
        print(videos_id)
        random.shuffle(videos_id)
        for i in range(count):
            res.append(videos_id[i])
        return res
