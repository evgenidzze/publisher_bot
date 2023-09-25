import json

from aiogram import types

from keyboards.kb_admin import kb_manage_user
from keyboards.kb_client import kb_manage_channel_inline


def get_admins() -> list:
    with open('data.json', 'r', encoding='utf-8') as file:
        file_data = json.load(file)
        return file_data['admins']


async def save_user_id_to_json(user_id: str, message: types.Message):
    with open('data.json', 'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        if user_id in file_data['users']:
            await message.answer(text=f'У користувача з id: {user_id} вже є доступ.', reply_markup=kb_manage_user)
        else:
            file_data['users'][user_id] = message.forward_from.username
            file.seek(0)
            json.dump(file_data, file, indent=4)
            await message.answer(text=f'Ви надали доступ користувачу {message.forward_from.username} з id: {user_id}',
                                 reply_markup=kb_manage_user)


async def remove_user_id_from_json(user_id, message: types.Message):
    with open('data.json', 'r', encoding='utf-8') as file:
        file_data = json.load(file)

    if user_id in file_data['users']:
        del file_data['users'][user_id]

        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(file_data, file, indent=4, ensure_ascii=False)

        await message.answer(text=f'Ви скасували права користувачу з id: {user_id}', reply_markup=kb_manage_user)
    else:
        await message.answer(text=f'Користувача з таким id не існує', reply_markup=kb_manage_user)


async def save_channel_json(channel_id: str, message: types.Message):
    with open('data.json', 'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        user_id = str(message.from_user.id)
        channel_name = message.forward_from_chat.title

        if user_id not in file_data['channels']:  # if user don't have any channels
            file_data['channels'][user_id] = {channel_id: channel_name}
            file.seek(0)
            json.dump(file_data, file, indent=4)
        else:
            if channel_id not in file_data['channels'][user_id]:
                file_data['channels'][user_id][channel_id] = channel_name
                file.seek(0)
                json.dump(file_data, file, indent=4)
                await message.answer(
                    text=f'Канал <a href="{await message.forward_from_chat.get_url()}">{message.forward_from_chat.title}'
                         f'</a> з id: <code>{channel_id}</code> успішно підключений',
                    reply_markup=kb_manage_channel_inline, parse_mode='html')
            else:
                await message.answer(
                    text=f'Канал <a href="{await message.forward_from_chat.get_url()}">{message.forward_from_chat.title}'
                         f'</a> з id: <code>{channel_id}</code> вже підключено.',
                    reply_markup=kb_manage_channel_inline, parse_mode='html')



def get_all_users():
    with open('data.json', 'r', encoding='utf-8') as file:
        file_data = json.load(file)
        users = "\n".join(
            [f"{name} - `{id}`" if name else f"Без імені - `{id}`" for id, name in file_data['users'].items()])
        return users


def get_all_channels(user_id):
    with open('data.json', 'r', encoding='utf-8') as file:
        file_data = json.load(file)
        channels = [f"{name} - <code>{id}</code>" for id, name in file_data['channels'][str(user_id)].items()]
        return channels


async def remove_channel_id_from_json(channel_id, message: types.Message):
    with open('data.json', 'r', encoding='utf-8') as file:
        file_data = json.load(file)
    user_id = str(message.from_user.id)
    if channel_id in file_data['channels'][user_id]:
        channel_name = file_data['channels'][user_id][channel_id]
        del file_data['channels'][user_id][channel_id]

        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(file_data, file, indent=4, ensure_ascii=False)

        await message.answer(text=f'Ви відключили канал: {channel_name}', reply_markup=kb_manage_channel_inline)
    else:
        await message.answer(text=f'Каналу з таким id не існує', reply_markup=kb_manage_channel_inline)


def user_register_status(user_id: str) -> dict:
    with open('data.json', 'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        users = file_data['users']
        register_status = {'is_id': False, 'is_name': False}

        if user_id in users:
            register_status['is_id'] = True
            register_status['is_name'] = bool(users[user_id])
            if register_status['is_name']:
                register_status['name'] = users[user_id]
            return register_status
        return register_status
