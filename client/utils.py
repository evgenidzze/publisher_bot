from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_calendar import SimpleCalendar, simple_cal_callback
from aiogram_timepicker import carousel, clock

from create_bot import dp, bot
from aiogram_timepicker.panel import FullTimePicker, full_timep_callback

from json_functionality import get_all_channels
from keyboards.kb_client import cancel


async def nav_cal_handler(message: Message):
    print(message)
    await bot.send_message(chat_id=message.from_user.id, text="Оберіть дату: ",
                           reply_markup=await SimpleCalendar().start_calendar())


@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    print('asdasd')
    print('asdasd')
    print('asdasd')
    print('asdasd')
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}'
        )


@dp.message_handler(Text(equals=['Full TimePicker'], ignore_case=True))
async def full_picker_handler(message: Message):
    await message.answer(
        "Please select a time: ",
        reply_markup=await FullTimePicker().start_picker()
    )


@dp.callback_query_handler(full_timep_callback.filter())
async def process_full_timepicker(callback_query: CallbackQuery, callback_data: dict):
    r = await FullTimePicker().process_selection(callback_query, callback_data)
    if r.selected:
        await callback_query.message.answer(
            f'You selected {r.time.strftime("%H:%M:%S")}'
        )
        await callback_query.message.delete_reply_markup()


def kb_channels(message):
    kb_all_channels = InlineKeyboardMarkup()
    kb_all_channels.add(
        *[InlineKeyboardButton(text=i.split(' - <code>')[0], callback_data=i) for i in
          get_all_channels(message.from_user.id)])
    kb_all_channels.add(cancel)
    return kb_all_channels
