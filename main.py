import asyncio

import yaml
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

API_TOKEN = config['token']

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


class UserState(StatesGroup):
    # Обычный пользователь
    name = State()


# Обработка команды /start
@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📂 Кейсы", callback_data=f"show_cases")],
            [InlineKeyboardButton(text="📝 Отзывы", callback_data=f"reviews")],
            [InlineKeyboardButton(text="📇 Контакты", callback_data=f"contacts")],
            [InlineKeyboardButton(text="💼 О компании", callback_data=f"about")]
        ]
    )
    await message.answer("Добро пожаловать в бот компании Spicy Code!", reply_markup=keyboard)


# @dp.callback_query(F.data == "show_cases")
# async def show_cases(callback_query: CallbackQuery, state: FSMContext):
#     keyboard = add_back_button()
#     cases_text = """
#     **Наши кейсы:**
#
#     1. 📦 **Luba_helper_bot** — Бот для продажи курсов по йоге с интеграцией платёжной системы и контроля подписок.
#     2. ❤️ **Синергия Добра** — Виртуальный помощник для волонтёрства и записи на мастер-классы с экспортом данных.
#     3. 📊 **Bybit Trading Bot** — Скрипт для торговли криптовалютой на Bybit с управлением через Telegram.
#     4. 📸 **Photography Courses Bot** — Виртуальный помощник для знакомства с брендом и покупки курсов по фотографии (неактивен).
#     """
#     msg = await callback_query.message.answer(cases_text, parse_mode='Markdown', reply_markup=keyboard)
#     await state.update_data(to_delete=[msg.message_id])
#     await state.set_state(UserState.name)


# Обработка выбора "Записаться на звонок"

@dp.callback_query(F.data == "contacts")
async def show_cases(callback_query: CallbackQuery, state: FSMContext):
    keyboard = add_back_button()
    cases_text = """
    <b>Номер:</b> +7(987)866-60-44
<b>Телеграмм:</b> @Alexandria_vV 
<b>Наш телеграмм канал:</b> @spicy_code
<b>Наш сайт:</b> https://alexandriabricoz.github.io/vcard-personal-portfolio/
<b>Profi.ru</b>: https://profi.ru/profile/SkvortsovAI11/#reviews-tab
    """
    msg = await callback_query.message.answer(cases_text, parse_mode="HTML", reply_markup=keyboard)
    await state.update_data(to_delete=[msg.message_id])

    await state.set_state(UserState.name)


@dp.message(Command('contacts'))
async def show_cases(message: types.Message, state: FSMContext):
    keyboard = add_back_button()
    cases_text = """
    <b>Номер:</b> +7(987)866-60-44
<b>Телеграмм:</b> @Alexandria_vV 
<b>Наш телеграмм канал:</b> @spicy_code
<b>Наш сайт:</b> https://alexandriabricoz.github.io/vcard-personal-portfolio/
<b>Profi.ru</b>: https://profi.ru/profile/SkvortsovAI11/#reviews-tab
    """
    msg = await message.answer(cases_text, parse_mode="HTML", reply_markup=keyboard)
    await state.update_data(to_delete=[msg.message_id])

    await state.set_state(UserState.name)


# Обработка выбора "О компании"
@dp.message(Command("about"))
async def about_company(message: types.Message, state: FSMContext):
    keyboard = add_back_button()
    about_text = """
    **Spicy Code** — команда разработчиков, специализирующаяся на создании и модернизации Telegram-ботов, а также автоматизации бизнес-процессов.
    Мы предлагаем эффективные решения для различных отраслей и задач.
    """
    msg = await message.answer(about_text, parse_mode="HTML", reply_markup=keyboard)
    await state.update_data(to_delete=[msg.message_id])
    await state.set_state(UserState.name)


# Обработка выбора "О компании"
@dp.callback_query(F.data == "about")
async def about_company(callback_query: CallbackQuery, state: FSMContext):
    keyboard = add_back_button()
    about_text = """
    **Spicy Code** — команда разработчиков, специализирующаяся на создании и модернизации Telegram-ботов, а также автоматизации бизнес-процессов.
    Мы предлагаем эффективные решения для различных отраслей и задач.
    """
    msg = await callback_query.message.answer(about_text, parse_mode="HTML", reply_markup=keyboard)
    await state.update_data(to_delete=[msg.message_id])
    await state.set_state(UserState.name)


class Review:
    def __init__(self, name, answer, date):
        self.name = name
        self.answer = answer
        self.date = date


reviews = [Review('Кирилл',
                  'Александр — отличный специалист. Старается вникнуть в суть задачи, предлагает лучшие решения, стремится сделать задачу наилучшим образом.',
                  '12 августа 2024'),
           Review('Александр',
                  'Александр, хоть и молодой специалист, но опытный. Задание сделал быстро и качественно. Мне все понравилось, включая стоимость. Буду к нему обращаться в дальнейшем.',
                  '7 июля 2024'),
           Review('Резеда',
                  'Благодаря специалисту удалось разработать телеграмм бота быстро и эффективно! Его консультация помогла мне реализовать нужный функционал без лишних сложностей. Работа была сделана в срок. Без воды и лишних проблем. Рекомендую данного специалиста! Буду Рада сотрудничать в дальнейшем!',
                  '9 апреля 2024')
           ]


@dp.callback_query(F.data == "reviews")
async def show_cases(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message_ids = data.get("message_ids", [])
    msg_ids = []
    for i in reviews:
        cases_text = f"""<b>{i.name}</b>:\n{i.answer}\n\n{i.date}"""
        if i == reviews[-1]:
            keyboard = add_back_button()
            message_id = await callback_query.message.answer(cases_text, parse_mode="HTML", reply_markup=keyboard)
        else:
            message_id = await callback_query.message.answer(cases_text, parse_mode="HTML")
        msg_ids.append(message_id.message_id)
    await state.update_data(to_delete=msg_ids)


class Case:
    def __init__(self, name, answer, link = None):
        self.name = name
        self.answer = answer
        self.link = link


cases = [Case('Кейс компании Spicy Code: Модернизация Telegram-бота "Локал Маркет" для управления коммерцией',
              """ЗАДАЧА: Улучшение функционала Telegram-бота, используемого для управления коммерческой информацией, оптимизация взаимодействия администратора, партнеров и пользователей.

ОСНОВНЫЕ ИЗМЕНЕНИЯ:

Интерфейс администратора:

Добавлены функции удаления, редактирования и управления коммерческой информацией.

Настройка позиций коммерции и изменение ее статуса.
Разделение коммерции по категориям и улучшение навигации в меню.

Возможность просмотра пользовательского интерфейса и управления статистикой бота.

Введение системы уведомлений для администратора.

Контроль за действиями пользователей:

Внедрение расширенной системы оценок коммерции.

Создание механизмов для резервного копирования данных.

Улучшение контроля за публикацией информации и манипуляциями с оценками.

Интерфейс партнера:

Настройка таймингов сообщений и ограничений на бронирование услуг.

Добавление кнопки для отправки жалоб администратору.

Интерфейс пользователя:

Уведомления о подтверждении бронирования и улучшенное отображение информации.

Введение ежедневных опросов и функционала для обратной связи с администратором.

РЕЗУЛЬТАТ: Бот стал более функциональным и удобным для администрирования и использования, что улучшило качество взаимодействия всех участников процесса.""", 'https://t.me/LocalShopsBot'),
         Case(
             'Кейс компании Spicy Code: Создание Telegram-бота "Синергия Добра 🫶🏻🇷🇺" для волонтёрства и мастер-классов',
             """ЗАДАЧА: Разработка виртуального помощника в виде Telegram-бота для связи с администратором и подачи заявок на волонтёрство и участие в мастер-классах.

ОСНОВНЫЕ ИЗМЕНЕНИЯ:

Интерфейс администратора:

Создание функций для получения и управления заявками на волонтёрство и мастер-классы.

Разработка инструмента для экспорта данных о записях на мероприятия в формате Excel.

Интерфейс пользователя:

Удобный интерфейс для связи с администратором и подачи заявок на волонтёрство и мастер-классы.

РЕЗУЛЬТАТ: Бот упрощает процесс взаимодействия пользователей с администрацией, автоматизирует подачу заявок и предоставляет удобный способ для мониторинга и анализа данных по мероприятиям.""", 'https://t.me/Synergidobra_bot'),
         Case('Кейс компании Spicy Code: Создание Telegram-бота "Luba_helper_bot" для продажи курсов по йоге',
              """ЗАДАЧА: Разработка Telegram-бота для продажи курсов по йоге с интеграцией платёжной системы и системы контроля подписок на занятия, которые также оплачиваются.

ОСНОВНЫЕ ИЗМЕНЕНИЯ:

Интерфейс администратора:

Интеграция платёжной системы для автоматизированной оплаты курсов и подписок.

Создание системы контроля подписок, позволяющей управлять доступом к занятиям в зависимости от статуса оплаты.

Разработка функции для экспорта данных о пользователях, подписках и платежах в формате Excel.

Интерфейс пользователя:

Удобный интерфейс для покупки курсов и оформления подписок.

Автоматические уведомления о статусе подписки и предстоящих платежах.

РЕЗУЛЬТАТ: Бот обеспечивает автоматизацию продажи курсов и управления подписками, упрощая процесс для администраторов и пользователей, а также предоставляет удобный инструмент для мониторинга и анализа данных.""", 'https://t.me/Luba_helper_bot'),
         Case(
             'Кейс компании Spicy Code: Создание скрипта для торговли криптовалютой на Bybit с управлением через Telegram-бот',
             """ЗАДАЧА: Разработка скрипта для автоматизированной торговли криптовалютой на платформе Bybit по заданному алгоритму, с управлением и мониторингом через Telegram-бот.

ОСНОВНЫЕ ИЗМЕНЕНИЯ:

Скрипт для торговли:

Разработка алгоритма для автоматической торговли криптовалютой на платформе Bybit.

Интеграция с Bybit API для выполнения торговых операций в соответствии с алгоритмом.

Интерфейс Telegram-бота:

Управление скриптом через Telegram-бот, включая запуск, остановку и настройку параметров алгоритма.

Мониторинг торговых операций и отправка уведомлений о статусе сделок в реальном времени.

РЕЗУЛЬТАТ: Бот автоматизирует процесс торговли криптовалютой, обеспечивает гибкое управление и мониторинг операций через Telegram, что делает процесс торговли более эффективным и удобным.""", ),
         Case(
             'Кейс компании Spicy Code: Создание Telegram-бота для знакомства с брендом и покупки курсов по фотографии',
             """‼️На данный момент бот не активен и не функционирует.‼️

ЗАДАЧА: Разработка виртуального помощника в виде Telegram-бота для знакомства с брендом и продажи курсов по фотографии, с возможностью отслеживания и экспорта информации о платежах.

ОСНОВНЫЕ ИЗМЕНЕНИЯ:

Интерфейс администратора:

Интеграция функции экспорта данных о платежах за курсы в формате Excel для удобного анализа и учета.

Интерфейс пользователя:

Удобный интерфейс для знакомства с брендом и покупки курсов по фотографии.

Автоматизированная система оплаты и уведомления о статусе покупки.

РЕЗУЛЬТАТ: Бот обеспечивал автоматизацию процесса продажи курсов и знакомил пользователей с брендом.""")
         ]


# Функция для добавления кнопок "Назад" и "Далее"
def add_navigation_buttons(index, total_cases):
    buttons = []
    if index > 0:
        buttons.append(InlineKeyboardButton(text="🔙 Назад", callback_data=f"previous_case_{index - 1}"))
    if index < total_cases - 1:
        buttons.append(InlineKeyboardButton(text="➡️ Далее", callback_data=f"next_case_{index + 1}"))
    return InlineKeyboardMarkup(inline_keyboard=[buttons,[InlineKeyboardButton(text="📂 Вернуться в главное меню", callback_data="back")]])


# Обработка показа кейсов по одному
@dp.callback_query(F.data.startswith("show_cases"))
async def show_cases(callback_query: CallbackQuery, state: FSMContext):
    # Начинаем с первого кейса
    await state.update_data(current_case=0)
    await show_case(callback_query, state, 0)


async def show_case(callback_query: CallbackQuery, state: FSMContext, index: int):
    case = cases[index]
    if case.link:
        cases_text = f"<b>{case.name}</b>:\n\n{case.answer}\n\n<b>Ссылка на проект</b>:{case.link}"
    else:
        cases_text = f"<b>{case.name}</b>:\n\n{case.answer}"
    total_cases = len(cases)

    # Отправляем сообщение с текущим кейсом и навигацией
    keyboard = add_navigation_buttons(index, total_cases)
    message = await callback_query.message.answer(cases_text, parse_mode="HTML", reply_markup=keyboard)

    # Сохраняем ID сообщения для удаления
    data = await state.get_data()
    msg_ids = data.get("to_delete", [])
    msg_ids.append(message.message_id)
    await state.update_data(to_delete=msg_ids, current_case=index)


# Обработка кнопки "Далее"
@dp.callback_query(F.data.startswith("next_case"))
async def next_case(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = int(callback_query.data.split('_')[-1])
    await delete_previous_messages(callback_query, state)
    await show_case(callback_query, state, index)


# Обработка кнопки "Назад"
@dp.callback_query(F.data.startswith("previous_case"))
async def previous_case(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = int(callback_query.data.split('_')[-1])
    await delete_previous_messages(callback_query, state)
    await show_case(callback_query, state, index)


# Удаление предыдущих сообщений
async def delete_previous_messages(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message_ids = data.get("to_delete", [])
    for message_id in message_ids:
        try:
            await callback_query.bot.delete_message(callback_query.message.chat.id, message_id)
        except Exception as e:
            print(f"Error deleting message {message_id}: {e}")
    await state.update_data(to_delete=[])


# Функция для добавления кнопки "Назад"
def add_back_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
        ]
    )


@dp.callback_query(F.data == "back")
async def back_to_commerce(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message_ids = data.get("to_delete", [])
    for message_id in message_ids:
        try:
            await callback_query.bot.delete_message(callback_query.message.chat.id, message_id)
        except Exception as e:
            print(f"Error deleting message {message_id}: {e}")
    await state.update_data(to_delete=[])  # Очищаем список идентификаторов сообщений


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
