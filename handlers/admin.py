from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import ADMINS
from json_functionality import save_user_id_to_json, remove_user_id_from_json, get_all_users
from keyboards.kb_admin import kb_admin


class FSMAdmin(StatesGroup):
    user_id = State()
    remove_user_id = State()
    channel_id = State()


async def make_changes_command(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer(text='Вітаю, адміністратор!', reply_markup=kb_admin)
    else:
        await message.answer(text='У вас немає прав модератора.')


# @dp.message_handler(Text(equals='Додати нового працівника'), state=None)
async def add_user(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await FSMAdmin.user_id.set()
        await message.answer('Напишіть id користувача, якого хочете додати.\n'
                             '(Щоб дізнатись id, перешліть будь яке його повідомлення боту @getmyid_bot)')


async def user_list(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer(get_all_users(), parse_mode="Markdown")


# Скасувати працівнику права
async def deny_user_access(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await FSMAdmin.remove_user_id.set()

        await message.answer('Надішліть id користувача, якому хочете скасувати права.')
        all_users = get_all_users()
        await message.answer(all_users, parse_mode="Markdown")


# @dp.message_handler(state=FSMAdmin.user_id)
async def load_id(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        user_id = message.text
        if user_id.isdigit():
            await save_user_id_to_json(user_id, message)
            await state.finish()
        else:
            await message.answer('id має складатись тільки з цифр, надішліть ще раз.')


async def remove_id(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        user_id = message.text
        if user_id.isdigit():
            await remove_user_id_from_json(user_id, message)
            await state.finish()
        else:
            await message.answer('id має складатись тільки з цифр, надішліть ще раз.')


# @dp.message_handler(Text(equals='відміна', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        current_state = await state.get_state()
        if current_state is None:
            await message.answer('OK')
            return
        await state.finish()
        await message.answer('OK')
    else:
        await message.answer('У вас немає прав адміністратора')


async def add_channel(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await FSMAdmin.channel_id.set()
        await message.answer('Напишіть id каналу, якого хочете додати.\n'
                             '(Щоб дізнатись id, перешліть будь яке його повідомлення боту @getmyid_bot)')

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(add_user, Text(equals='Додати працівника'), state=None)
    dp.register_message_handler(deny_user_access, Text(equals='Видалити працівника'), state=None)
    dp.register_message_handler(cancel_handler, Text(equals='Відміна', ignore_case=True), state="*")
    dp.register_message_handler(user_list, Text(equals='Список користувачів', ignore_case=True))
    dp.register_message_handler(add_channel, Text(equals='Додати канал'), state=None)
    dp.register_message_handler(load_id, state=FSMAdmin.user_id)
    dp.register_message_handler(remove_id, state=FSMAdmin.remove_user_id)
    dp.register_message_handler(make_changes_command, commands=['moderator'])
