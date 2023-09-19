import json


def get_admins() -> list:
    with open('data.json', 'r', encoding='utf-8') as file:
        file_data = json.load(file)
        return file_data['admins']


async def save_user_id_to_json(user_id, message):
    with open('users.json', 'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        if user_id in file_data['users']:
            await message.answer(text=f'У користувача з id: {user_id} вже є доступ.')
        else:
            file_data['users'][user_id] = ""
            file.seek(0)
            json.dump(file_data, file, indent=4)
            await message.answer(text=f'Ви надали доступ користувачу з id: {user_id}')


async def remove_user_id_from_json(user_id, message):
    with open('users.json', 'r', encoding='utf-8') as file:
        file_data = json.load(file)

    if user_id in file_data['users']:
        print(file_data)
        del file_data['users'][user_id]

        with open('users.json', 'w', encoding='utf-8') as file:
            json.dump(file_data, file, indent=4, ensure_ascii=False)

        await message.answer(text=f'Ви скасували права користувачу з id: {user_id}')
    else:
        await message.answer(text=f'Користувача з таким id не існує')


def get_all_users():
    with open('data.json', 'r', encoding='utf-8') as file:
        file_data = json.load(file)
        users = "\n".join(
            [f"{name} - `{id}`" if name else f"Без імені - `{id}`" for id, name in file_data['users'].items()])
        return users
