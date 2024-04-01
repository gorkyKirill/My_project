from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aiohttp
import uuid
import asyncio
import logging
from datetime import datetime

# Инициализация бота и диспетчера
bot = Bot(token="6701021643:AAFvrs2tbdQLqpk3IDiBk6JdQM6KKmWJAHw")
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

dom = "моте.рф"
# Конфигурация
SERVER_URL = 'http://91.222.236.174:8080'

# # Словарь для хранения состояния кнопок
# button_states = {
#     'sms': False,
#     'push': False,
#     'error_card': False,
#     'error_sms': False,
#     'complete': False
# }

# Класс состояний FSM
class Path(StatesGroup):
    time = State()
    currency = State()
    price_car1 = State()
    price_car2 = State()
    price_car3 = State()
    price_car4 = State()
    price_car5 = State()
    price_car6 = State()
    price_car7 = State()
    time_trip = State()
    map_screen = State()

# Функция для создания клавиатуры с кнопками
# def create_keyboard():
#     keyboard_id = str(uuid.uuid4())  # Генерируем уникальный идентификатор для клавиатуры
#     keyboard = InlineKeyboardMarkup(row_width=2)
#     sms_button = InlineKeyboardButton(
#         text=("✅ SMS" if button_states['sms'] else "❌ SMS"),
#         callback_data=f"toggle:|:sms:|:{keyboard_id}"
#     )
#     push_button = InlineKeyboardButton(
#         text=("✅ PUSH" if button_states['push'] else "❌ PUSH"),
#         callback_data=f"toggle:|:push:|:{keyboard_id}"
#     )
#     error_card_button = InlineKeyboardButton(
#         text=("✅ ERROR_CARD" if button_states['error_card'] else "❌ ERROR_CARD"),
#         callback_data=f"toggle:|:error_card:|:{keyboard_id}"
#     )
#     error_sms_button = InlineKeyboardButton(
#         text=("✅ ERROR_SMS" if button_states['error_sms'] else "❌ ERROR_SMS"),
#         callback_data=f"toggle:|:error_sms:|:{keyboard_id}"
#     )
#     complete_button = InlineKeyboardButton(
#         text=("✅ COMPLETE" if button_states['complete'] else "❌ COMPLETE"),
#         callback_data=f"toggle:|:complete:|:{keyboard_id}"
#     )
#     keyboard.add(sms_button, push_button, error_card_button, error_sms_button, complete_button)
#     return keyboard

# Обработчик команды /start
@dp.message_handler(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Создать поездку", callback_data="new_path"))
    await message.answer("В режиме доработок. Используйте команду /keyboard, чтобы отправить клавиатуру в чат.", reply_markup=kb)

# # Обработчик команды /keyboard
# @dp.message_handler(Command("keyboard"))
# async def send_keyboard(message: types.Message):
#     chat_id = message.chat.id  # Получаем ID текущего чата
#     await bot.send_message(chat_id, "Выберите опции:", reply_markup=create_keyboard())

# Обработчик нажатия на кнопки
# @dp.callback_query_handler(lambda c: c.data.startswith('toggle:|:'))
# async def process_callback(callback_query: types.CallbackQuery):
#     _, action, _ = callback_query.data.split(':|:')
#     if action in button_states:
#         button_states[action] = not button_states[action]
#         await bot.answer_callback_query(callback_query.id)
#         await update_keyboard(callback_query)

# async def update_keyboard(callback_query):
#     await asyncio.sleep(0.1)  # Добавляем задержку перед редактированием сообщения
#     await bot.edit_message_reply_markup(
#         chat_id=callback_query.message.chat.id,
#         message_id=callback_query.message.message_id,
#         reply_markup=create_keyboard()
#     )

# Обработчик callback-кнопки "Создать поездку"
@dp.callback_query_handler(text="new_path")
async def path(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Path.time.state)
    #await Path.currency.set()
    await bot.send_message(call.from_user.id, "Введи время прибытия")

@dp.message_handler(state=Path.time.state)
async def curq(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)
    await state.set_state(Path.currency.state)
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(InlineKeyboardButton(text="USD", callback_data="USD"),
           InlineKeyboardButton(text="EUR", callback_data="EUR"),
           InlineKeyboardButton(text="AED", callback_data="AED"))
    await bot.send_message(message.from_user.id, "Выберите валюту:", reply_markup=kb)


# Обработчик выбора валюты
@dp.callback_query_handler(text=["USD", "EUR", "AED"], state=Path.currency)
async def handle_currency(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(currency=call.data)
    await Path.price_car1.set()
    await call.message.answer(f"Введите цену для Comfort тарифа в {call.data}:")

# Обработчики ввода цены для каждого тарифа
@dp.message_handler(lambda message: message.text.isdigit(), state=[Path.price_car1, Path.price_car2, Path.price_car3, Path.price_car4, Path.price_car5, Path.price_car6, Path.price_car7])
async def handle_price_car(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    state_number = int(current_state.split(".")[-1][-1])
    tariff_names = {
        1: "Comfort",
        2: "UberX",
        3: "UberXL",
        4: "VanXL",
        5: "Black",
        6: "Green",
        7: "Family"
    }
    price = int(message.text)
    await state.update_data({f"price_car{state_number}": price})

    if state_number < 7:
        next_state_number = state_number + 1
        await getattr(Path, f"price_car{next_state_number}").set()
        currency = await state.get_data()
        await message.answer(f"Введите цену для {tariff_names[next_state_number]} в {currency['currency']}:")
    else:
        await Path.time_trip.set()
        await message.answer("Введите время поездки в минутах:")

# Обработчик ввода времени поездки
@dp.message_handler(lambda message: message.text.isdigit(), state=Path.time_trip)
async def time_trip(message: types.Message, state: FSMContext):
    time_minutes = int(message.text)
    await state.update_data(time_trip=time_minutes)
    await Path.map_screen.set()
    await message.answer("Отправьте скриншот карты:")

# Обработчик приема фото и отправки его на сервер Flask
@dp.message_handler(content_types=types.ContentType.PHOTO, state=Path.map_screen)
async def handle_photo(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    ser_url = (SERVER_URL + "/save_trip")
    new_filename = str(uuid.uuid4()) + '.png'
    photo = await message.photo[-1].download(new_filename)
    async with aiohttp.ClientSession() as session:
        async with session.post(ser_url, data={"photo": open(new_filename, 'rb')}) as response:
            try:
                server_response = await response.text()
                await message.answer(f'Server response: {server_response}')
                await message.answer(f'http://моте.рф/?{new_filename[:-4]}')
            except aiohttp.ClientError as e:
                logging.error(f'Error sending photo to server: {str(e)}')
                await message.answer('Error sending photo to server')
        await session.get(f"{SERVER_URL}/tg/?guid={new_filename[:len(new_filename) - 4]}&price1={user_data['price_car1']}&price2={user_data['price_car2']}&price3={user_data['price_car3']}&price4={user_data['price_car4']}&price5={user_data['price_car5']}&price6={user_data['price_car6']}&price7={user_data['price_car7']}&time={user_data['time']}&current={user_data['currency']}")
    await state.finish()

    kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Создать поездку", callback_data="new_path"))
    await message.answer("Поездка успешно создана.", reply_markup=kb)

def parse_button_states(keyboard: InlineKeyboardMarkup) -> dict:
    button_states = {}
    if keyboard:
        for row in keyboard.inline_keyboard:
            for button in row:
                callback_data = button.callback_data
                if callback_data.startswith("toggle:|:"):
                    _, action, _ = callback_data.split(':|:')
                    button_states[action] = True if button.text.startswith("✅") else False
    return button_states

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)