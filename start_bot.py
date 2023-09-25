from aiogram.utils import executor

from create_bot import dp
from admin import admin
from client import handlers

handlers.register_handlers_client(dp)
admin.register_handlers_admin(dp)

executor.start_polling(dp, skip_updates=True)
