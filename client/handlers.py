import locale
import re

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from create_bot import bot
from .utils import nav_cal_handler, kb_channels, process_simple_calendar
from json_functionality import user_register_status, get_all_channels, save_channel_json, remove_channel_id_from_json
from keyboards.kb_client import kb_manage_channel, kb_manage_channel_inline, cancel_kb, cancel, post_formatting_kb

locale.setlocale(locale.LC_ALL, 'uk_UA.utf8')


class FSMClient(StatesGroup):
    user_name = State()
    post_text = State()
    remove_channel_id = State()
    channel_id = State()
    create_post_in_channel = State()
    formatting = State()


async def start_command(message: Message):
    if message.chat.type != types.ChatType.GROUP:
        user_id = str(message.from_user.id)
        user_status = user_register_status(user_id)
        if user_status['is_id'] and user_status['is_name']:
            await message.answer(text=f'Вітаю, {user_status["name"]}\n'
                                      f'Це бот для відкладеного постингу. Для початку роботи '
                                      f'скористайтеся командами або головним меню.\n'
                                      f'/addchannel – підключення нового каналу',
                                 reply_markup=kb_manage_channel)
        else:
            await message.answer(
                text='У вас немає доступу до бота. Після отримання доступу від адміністратора, натисніть на команду /start',
                reply_markup=ReplyKeyboardRemove())


async def manage_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(chat_id=message.from_user.id, text="Панель управління каналами",
                           reply_markup=kb_manage_channel_inline)


async def deny_channel(message: types.Message):
    await FSMClient.remove_channel_id.set()
    all_channels = '\n'.join([i for i in get_all_channels(message.from_user.id)])

    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Надішліть id каналу, який хочете відключити.\n\n'
                                f'{all_channels}', reply_markup=cancel_kb, parse_mode="html")


async def remove_channel_id(message: types.Message, state: FSMContext):
    channel_id = str(message.text)
    if channel_id[1:].isdigit():
        await remove_channel_id_from_json(channel_id, message)
        await state.finish()
    else:
        await message.answer('id має складатись тільки з цифр, надішліть ще раз.')


async def add_channel(message: types.Message, state: FSMContext):
    await state.finish()
    await FSMClient.channel_id.set()
    me = await bot.me
    bot_name = me.username
    await bot.send_message(chat_id=message.from_user.id,
                           text="Щоб підключити канал, призначте бота його адміністратором. Для цього:\n1. Перейдіть в канал.\n2. "
                                "Натисніть на назву каналу, щоб відкрити його налаштування.\n3. Перейдіть в «Адміністратори» → «Додати "
                                f"адміністратора».\n4. Введіть в пошуку <code>@{bot_name}</code>. У результатах пошуку побачите вашого бота. "
                                "Клікніть по ньому, потім натисніть «Готово». Після цього перешліть сюди будь-яке повідомлення з каналу.",
                           parse_mode='html', reply_markup=cancel_kb)


async def load_channel_id(message: types.Message, state: FSMContext):
    if 'forward_from_chat' in message:
        channel_chat_id = str(message.forward_from_chat.id)
        me = await bot.get_me()
        bot_id = me.id
        bot_name = me.username
        chat_member = await bot.get_chat_member(chat_id=channel_chat_id, user_id=bot_id)
        bot_status = chat_member.status
        if bot_status == 'administrator':
            await save_channel_json(channel_id=channel_chat_id, message=message)
            await state.finish()
        else:
            await state.finish()
            await message.answer(
                text=f'⛔️ Немає доступу. Переконайтеся, що бот <code>@{bot_name}</code> доданий до адміністраторів каналу '
                     f'<a href="{await message.forward_from_chat.get_url()}">{message.forward_from_chat.title}</a>.',
                parse_mode='html')
    else:
        await message.answer(text='Потрібно переслати повідовлення саме з каналу.\n'
                                  'Спробуйте ще раз.')


async def channel_list(call: types.CallbackQuery):
    all_channels = '\n'.join([i for i in get_all_channels(call.message.chat.id)])

    try:
        await call.message.edit_text(text=all_channels, parse_mode='html',
                                     reply_markup=kb_manage_channel_inline)
    except:
        pass


async def create_post(message: types.Message, state: FSMContext):
    await state.finish()

    if get_all_channels(message.from_user.id):
        await FSMClient.create_post_in_channel.set()
        await message.answer(text='Оберіть канал:', reply_markup=kb_channels(message), parse_mode='html')
    else:
        await add_channel(message, state)


async def choose_channel(message: types.CallbackQuery, state: FSMContext):
    await FSMClient.post_text.set()
    choosen_channel = message.data
    pattern = r'<code>(.*?)</code>'
    channel_id = re.findall(pattern, choosen_channel)[0]
    channel_name = choosen_channel.split(' - <code>')[0]

    await state.update_data(channel_id=channel_id)

    await message.message.answer(
        text=f'Надішліть боту те, що хочете опублікувати в каналі\n«{channel_name}».')


async def load_post_data(message: types.Message, state: FSMContext):
    await state.update_data(post_text=message.text)

    data = await state.get_data()
    print(data)

    await bot.send_message(chat_id=message.from_user.id,
                           text='Налаштуйте оформлення посту. Якщо все буде готово, натисніть на кнопку «Продовжити».',
                           reply_markup=post_formatting_kb)
    await FSMClient.formatting.set()


async def load_post_formatting(message: types.CallbackQuery, state: FSMContext):
    if message.data == 'Запланувати':
        await nav_cal_handler(message)


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('OK')
        return
    await state.finish()
    await message.answer('OK')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'], state=None)
    dp.register_message_handler(cancel_handler, Text(equals='Відміна', ignore_case=True), state="*")
    dp.register_message_handler(create_post, Text(equals='Створити пост'), state="*")

    dp.register_message_handler(add_channel, commands=['addchannel'], state='*')
    dp.register_message_handler(manage_menu, Text(equals='Канали'), state='*')

    dp.register_callback_query_handler(deny_channel, Text(equals='Видалити канал'))
    dp.register_message_handler(remove_channel_id, state=FSMClient.remove_channel_id)
    dp.register_callback_query_handler(channel_list, Text(equals='Список каналів'))

    dp.register_callback_query_handler(add_channel, Text(equals='Додати канал'), state=None)
    dp.register_message_handler(load_channel_id, state=FSMClient.channel_id)

    dp.register_callback_query_handler(choose_channel, state=FSMClient.create_post_in_channel)
    dp.register_message_handler(load_post_data, state=FSMClient.post_text)

    dp.register_callback_query_handler(nav_cal_handler, Text(equals='Запланувати'))
    dp.register_callback_query_handler(load_post_formatting, state=FSMClient.formatting)

    # dp.register_callback_query_handler(process_simple_calendar, state=FSMClient.planned_date)
