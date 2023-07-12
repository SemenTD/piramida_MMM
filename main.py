import asyncio  # Работа с асинхронностью

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter  # Фильтр для /start, /...
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message  # Тип сообщения

from config import config  # Config
from states.form import FormStatesGroup

API_TOKEN = config.token

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())  # Менеджер бота


@dp.message(Command('start'))
async def process_start_command(message: Message):
    await message.answer(text='Этот бот демонстрирует работу FSM\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /fillform')


@dp.message(Command('fillform'))
async def handle_fillform(message: Message, state: FSMContext):
    await message.answer('Вы начали заполнение анкеты. Для начала введите имя')
    await state.set_state(FormStatesGroup.fill_name)


@dp.message(StateFilter(FormStatesGroup.fill_name))
async def handle_get_name(message: Message, state: FSMContext):
    name_from_message = message.text
    await state.update_data(name=name_from_message)  # {'name': name_from_message}
    await message.answer('Хорошо. А теперь напишите ваш возраст')
    await state.set_state(FormStatesGroup.fill_age)


@dp.message(StateFilter(FormStatesGroup.fill_age))
async def handle_get_age(message: Message, state: FSMContext):
    age_from_message = message.text
    if age_from_message.isdigit() and 1 <= int(age_from_message) <= 120:
        await state.update_data(age=age_from_message)
        await message.answer('А теперь загрузите фото')
        await state.set_state(FormStatesGroup.upload_photo)


@dp.message(StateFilter(FormStatesGroup.upload_photo), F.photo)
async def handle_photo_upload(message: Message, state: FSMContext):
    photo_id = message.photo[0].file_id
    state_data = await state.get_data()
    name = state_data['name']
    age = int(state_data['age'])

    await message.answer_photo(photo_id, caption=f'{name}, {age}')
    await state.clear()


async def main():
    try:
        print('Bot Started')
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':  # Если мы запускаем конкретно этот файл.
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')