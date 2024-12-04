import asyncio
import os
import sqlite3
from datetime import datetime

import pandas as pd

import yaml
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, \
    CallbackQuery, FSInputFile, InputFile

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
    log_action(message.from_user.id, message.from_user.username, message.from_user.full_name, 'start',
               'User started the bot')
    photo_path = "images/INTRO-BOT-PIC.png"
    photo = FSInputFile(photo_path)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📂 Кейсы", callback_data=f"show_cases")],
            [InlineKeyboardButton(text="📝 Отзывы", callback_data=f"reviews")],
            [InlineKeyboardButton(text="📇 Контакты", callback_data=f"contacts")],
            [InlineKeyboardButton(text="💼 О компании", callback_data=f"about")]
        ]
    )
    msg = await message.answer_photo(photo=photo, caption="Добро пожаловать в бот компании Spicy Code!",
                                     parse_mode="HTML",
                                     reply_markup=keyboard)
    # await state.update_data(to_delete=[msg.message_id])
    # await state.set_state(UserState.name)


@dp.callback_query(F.data == "contacts")
async def show_cases(callback_query: CallbackQuery, state: FSMContext):
    log_action(callback_query.message.from_user.id, callback_query.message.from_user.username,
               callback_query.message.from_user.full_name, 'contacts', 'User contacts')
    await callback_query.bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    keyboard = add_back_button()
    cases_text = """
    <b>Номер:</b> +7(987)866-60-44
<b>Телеграмм:</b> @Alexandria_vV 
<b>Наш телеграмм канал:</b> @spicy_code
<b>Наш сайт:</b> https://alexandriabricoz.github.io/vcard-personal-portfolio/
<b>Профи.ру</b>: https://profi.ru/profile/SkvortsovAI11/#reviews-tab
    """
    msg = await callback_query.message.answer(cases_text, parse_mode="HTML", reply_markup=keyboard)
    await state.update_data(to_delete=[msg.message_id])

    await state.set_state(UserState.name)


@dp.message(Command('contacts'))
async def show_cases(message: types.Message, state: FSMContext):
    keyboard = add_back_button()
    log_action(message.from_user.id, message.from_user.username, message.from_user.full_name, 'contacts',
               'User contacts')
    cases_text = """
    <b>Номер:</b> +7(987)866-60-44
<b>Телеграмм:</b> @Alexandria_vV 
<b>Наш телеграмм канал:</b> @spicy_code
<b>Наш сайт:</b> https://alexandriabricoz.github.io/vcard-personal-portfolio/
<b>Профи.ру</b>: https://profi.ru/profile/SkvortsovAI11/#reviews-tab
    """
    msg = await message.answer(cases_text, parse_mode="HTML", reply_markup=keyboard)
    await state.update_data(to_delete=[msg.message_id])

    await state.set_state(UserState.name)


# Обработка выбора "О компании"
@dp.message(Command("about"))
async def about_company(message: types.Message, state: FSMContext):
    log_action(message.from_user.id, message.from_user.username, message.from_user.full_name, 'about', 'User about')
    keyboard = add_back_button()
    about_text = """
    <b>Spicy Code</b>  — это не просто команда разработчиков, а ваш надежный партнер в мире IT. Мы специализируемся на создании и совершенствовании Telegram-ботов, а также на полной автоматизации бизнес-процессов. Наша миссия — не просто предоставлять программные решения, а создавать инструменты, которые трансформируют ваш бизнес, делая его более эффективным и конкурентоспособным.

Мы разрабатываем инновационные решения для самых разнообразных отраслей, от коммерции и торговли до образования и волонтёрства. Каждый наш проект — это тщательно продуманная система, интегрированная в вашу бизнес-модель и оптимизированная под ваши нужды.

<b>Spicy Code</b> — это гарантия качества, инноваций и безупречного исполнения. Мы не просто выполняем задачи, мы создаем будущее для вашего бизнеса.
    """
    msg = await message.answer(about_text, parse_mode="HTML", reply_markup=keyboard)
    await state.update_data(to_delete=[msg.message_id])
    await state.set_state(UserState.name)


# Обработка выбора "О компании"
@dp.callback_query(F.data == "about")
async def about_company(callback_query: CallbackQuery, state: FSMContext):
    log_action(callback_query.message.from_user.id, callback_query.message.from_user.username,
               callback_query.message.from_user.full_name, 'about', 'User about')
    await callback_query.bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    keyboard = add_back_button()
    about_text = """
    <b>Spicy Code</b>  — это не просто команда разработчиков, а ваш надежный партнер в мире IT. Мы специализируемся на создании и совершенствовании Telegram-ботов, а также на полной автоматизации бизнес-процессов. Наша миссия — не просто предоставлять программные решения, а создавать инструменты, которые трансформируют ваш бизнес, делая его более эффективным и конкурентоспособным.

Мы разрабатываем инновационные решения для самых разнообразных отраслей, от коммерции и торговли до образования и волонтёрства. Каждый наш проект — это тщательно продуманная система, интегрированная в вашу бизнес-модель и оптимизированная под ваши нужды.

<b>Spicy Code</b> — это гарантия качества, инноваций и безупречного исполнения. Мы не просто выполняем задачи, мы создаем будущее для вашего бизнеса.
    """
    msg = await callback_query.message.answer(about_text, parse_mode="HTML", reply_markup=keyboard)
    await state.update_data(to_delete=[msg.message_id])
    await state.set_state(UserState.name)


class Review:
    def __init__(self, name, answer, date):
        self.name = name
        self.answer = answer
        self.date = date


reviews = [Review('Ярослав',
                  'С заданием справился на 1000%. Вопросов о компетенциях не было, потому что он очень сильно помог и сделал круто. Обязательно сохраню контакт.',
                  '11 октября 2024'),
           Review('Никита',
                  'Быстро решили проблему специалист отличный, я как чайник ничего не понимал все объяснили хорошо и понятно,советую брать только у него!!',
                  '31 октября 2024'),
           Review('Кирилл',
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
    await callback_query.bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
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


def init_db():
    conn = sqlite3.connect('cases.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            answer TEXT NOT NULL,
            link TEXT,
            photo TEXT
        )
    ''')
    conn.commit()
    conn.close()


class Case:
    def __init__(self, name, answer, link=None, photo=None):
        self.name = name
        self.answer = answer
        self.link = link
        self.photo = photo


cases = [Case('Кейс компании Spicy Code: Модернизация Telegram-бота "Локал Маркет" для управления коммерцией',
              """<b>ЗАДАЧА:</b> Улучшение функционала Telegram-бота, используемого для управления коммерческой информацией, оптимизация взаимодействия администратора, партнеров и пользователей.

<b>ОСНОВНЫЕ ИЗМЕНЕНИЯ:</b>

<b>Интерфейс администратора:</b>

Добавлены функции удаления, редактирования и управления коммерческой информацией.

Настройка позиций коммерции и изменение ее статуса.
Разделение коммерции по категориям и улучшение навигации в меню.

Возможность просмотра пользовательского интерфейса и управления статистикой бота.

Введение системы уведомлений для администратора.

Контроль за действиями пользователей:

Внедрение расширенной системы оценок коммерции.

Создание механизмов для резервного копирования данных.

Улучшение контроля за публикацией информации и манипуляциями с оценками.

<b>Интерфейс партнера:</b>

Настройка таймингов сообщений и ограничений на бронирование услуг.

Добавление кнопки для отправки жалоб администратору.

<b>Интерфейс пользователя:</b>

Уведомления о подтверждении бронирования и улучшенное отображение информации.

Введение ежедневных опросов и функционала для обратной связи с администратором.

<b>РЕЗУЛЬТАТ:</b> Бот стал более функциональным и удобным для администрирования и использования, что улучшило качество взаимодействия всех участников процесса.""",
              'https://t.me/LocalShopsBot', 'images/1.png'),
         Case(
             'Кейс компании Spicy Code: Разработка Telegram-бота для парсинга аптеки и управления базой данных PostgreSQL',
             """
<b>ЗАДАЧА:</b> Создание Telegram-бота, который будет парсить информацию с сайта аптеки, сохранять данные в базу данных PostgreSQL.

<b>ОСНОВНЫЕ ИЗМЕНЕНИЯ:</b>

<b>Интерфейс администратора:</b>

<b>Парсинг данных:</b> Бот автоматически парсит информацию о лекарствах, ценах, наличии и других параметрах с сайта аптеки.
<b>Управление базой данных:</b> Администратор может просматривать, редактировать и удалять данные в базе данных через удобный интерфейс бота.

<b>РЕЗУЛЬТАТ:</b> Бот значительно упростил процесс управления информацией об ассортименте аптеки, сделав его более удобным и эффективным как для администраторов, так и для пользователей. Автоматизация парсинга и хранения данных в базе PostgreSQL обеспечивает быстрый доступ к актуальной информации и улучшает качество обслуживания клиентов.
""",
         )
    ,
         Case(
             'Кейс компании Spicy Code: Создание Telegram-бота "Синергия Добра 🫶🏻🇷🇺" для волонтёрства и мастер-классов',
             """<b>ЗАДАЧА:</b> Разработка виртуального помощника в виде Telegram-бота для связи с администратором и подачи заявок на волонтёрство и участие в мастер-классах.

<b>ОСНОВНЫЕ ИЗМЕНЕНИЯ:</b>

<b>Интерфейс администратора:</b>

Создание функций для получения и управления заявками на волонтёрство и мастер-классы.

Разработка инструмента для экспорта данных о записях на мероприятия в формате Excel.

<b>Интерфейс пользователя:</b>

Удобный интерфейс для связи с администратором и подачи заявок на волонтёрство и мастер-классы.

<b>РЕЗУЛЬТАТ:</b> Бот упрощает процесс взаимодействия пользователей с администрацией, автоматизирует подачу заявок и предоставляет удобный способ для мониторинга и анализа данных по мероприятиям.""",
             'https://t.me/Synergidobra_bot', 'images/2.png'),
         Case(
             'Кейс компании Spicy Code: Разработка Telegram-бота для отслеживания изменений стоимости лота на аукционе',
             """<b>ЗАДАЧА:</b> Создание Telegram-бота, который будет отслеживать изменения в последней цене лота на сайте аукциона каждые 5 секунд, отправлять уведомления в Telegram и звонить на телефон при изменении цены. Когда лот становится не актуальным, отслеживание прекращается.
         
<b>ОСНОВНЫЕ ИЗМЕНЕНИЯ:</b>
         
<b>Скрипт для отслеживания:</b>

Разработка алгоритма для автоматического отслеживания изменений цены лота на сайте аукциона.

Интеграция с API сайта аукциона для получения актуальной информации о цене лота.

<b>Интерфейс Telegram-бота:</b>

Управление скриптом через Telegram-бот, включая запуск, остановку и настройку параметров отслеживания.

Мониторинг изменений цены и отправка уведомлений о статусе лота в реальном времени.

<b>Уведомления и звонки:</b>

Отправка уведомлений в Telegram при изменении цены лота.

Звонок на телефон при изменении цены лота.

<b>РЕЗУЛЬТАТ:</b> Бот значительно упрощает процесс отслеживания изменений стоимости интересующего лота, обеспечивая своевременные уведомления и звонки, что помогает пользователям быть в курсе всех изменений и принимать оперативные решения."""
         ),
         Case('Кейс компании Spicy Code: Создание Telegram-бота "Luba_helper_bot" для продажи курсов по йоге',
              """<b>ЗАДАЧА:</b> Разработка Telegram-бота для продажи курсов по йоге с интеграцией платёжной системы и системы контроля подписок на занятия, которые также оплачиваются.

<b>ОСНОВНЫЕ ИЗМЕНЕНИЯ:</b>

<b>Интерфейс администратора:</b>

Интеграция платёжной системы для автоматизированной оплаты курсов и подписок.

Создание системы контроля подписок, позволяющей управлять доступом к занятиям в зависимости от статуса оплаты.

Разработка функции для экспорта данных о пользователях, подписках и платежах в формате Excel.

<b>Интерфейс пользователя:</b>

Удобный интерфейс для покупки курсов и оформления подписок.

Автоматические уведомления о статусе подписки и предстоящих платежах.

<b>РЕЗУЛЬТАТ:</b> Бот обеспечивает автоматизацию продажи курсов и управления подписками, упрощая процесс для администраторов и пользователей, а также предоставляет удобный инструмент для мониторинга и анализа данных.""",
              'https://t.me/Luba_helper_bot', 'images/3.png'),
         Case(
             'Кейс компании Spicy Code: Создание скрипта для торговли криптовалютой на Bybit с управлением через Telegram-бот',
             """<b>ЗАДАЧА:</b> Разработка скрипта для автоматизированной торговли криптовалютой на платформе Bybit по заданному алгоритму, с управлением и мониторингом через Telegram-бот.

<b>ОСНОВНЫЕ ИЗМЕНЕНИЯ:</b>

Скрипт для торговли:

Разработка алгоритма для автоматической торговли криптовалютой на платформе Bybit.

Интеграция с Bybit API для выполнения торговых операций в соответствии с алгоритмом.

<b>Интерфейс Telegram-бота:</b>

Управление скриптом через Telegram-бот, включая запуск, остановку и настройку параметров алгоритма.

Мониторинг торговых операций и отправка уведомлений о статусе сделок в реальном времени.

<b>РЕЗУЛЬТАТ:</b> Бот автоматизирует процесс торговли криптовалютой, обеспечивает гибкое управление и мониторинг операций через Telegram, что делает процесс торговли более эффективным и удобным.""", ),
         Case(
             'Кейс компании Spicy Code: Создание Telegram-бота для знакомства с брендом и покупки курсов по фотографии',
             """‼️На данный момент бот не активен и не функционирует.‼️

<b>ЗАДАЧА:</b> Разработка виртуального помощника в виде Telegram-бота для знакомства с брендом и продажи курсов по фотографии, с возможностью отслеживания и экспорта информации о платежах.

<b>ОСНОВНЫЕ ИЗМЕНЕНИЯ:</b>

<b>Интерфейс администратора:</b>

Интеграция функции экспорта данных о платежах за курсы в формате Excel для удобного анализа и учета.

<b>Интерфейс пользователя:</b>

Удобный интерфейс для знакомства с брендом и покупки курсов по фотографии.

Автоматизированная система оплаты и уведомления о статусе покупки.

<b>РЕЗУЛЬТАТ:</b> Бот обеспечивал автоматизацию процесса продажи курсов и знакомил пользователей с брендом.""")
         ]


# Функция для добавления кнопок "Назад" и "Далее"
def add_navigation_buttons(index, total_cases):
    buttons = []
    if index > 0:
        buttons.append(InlineKeyboardButton(text="🔙 Назад", callback_data=f"previous_case_{index - 1}"))
    if index < total_cases - 1:
        buttons.append(InlineKeyboardButton(text="➡️ Далее", callback_data=f"next_case_{index + 1}"))
    return InlineKeyboardMarkup(
        inline_keyboard=[buttons, [InlineKeyboardButton(text="📂 Вернуться в главное меню", callback_data="back")]])


# Обработка показа кейсов по одному
@dp.callback_query(F.data.startswith("show_cases"))
async def show_cases(callback_query: CallbackQuery, state: FSMContext):
    log_action(callback_query.message.from_user.id, callback_query.message.from_user.username,
               callback_query.message.from_user.full_name, 'show_cases', 'show_cases')
    await callback_query.bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    # Начинаем с первого кейса
    await state.update_data(current_case=0)
    await show_case(callback_query, state, 0)

def get_cases():
    conn = sqlite3.connect('cases.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, answer, link, photo FROM cases')
    rows = cursor.fetchall()
    conn.close()

    cases = []
    for row in rows:
        name, answer, link, photo = row
        case = Case(name, answer, link, photo)
        cases.append(case)

    return cases

async def show_case(callback_query: CallbackQuery, state: FSMContext, index: int):
    cases = get_cases()
    case = cases[index]
    if case.link:
        cases_text = f"<b>{case.name}</b>:\n\n{case.answer}\n\n<b>Ссылка на проект</b>:{case.link}"
    else:
        cases_text = f"<b>{case.name}</b>:\n\n{case.answer}"
    total_cases = len(cases)

    # Отправляем сообщение с текущим кейсом и навигацией
    keyboard = add_navigation_buttons(index, total_cases)

    if case.photo:
        photo_path = case.photo
        photo = FSInputFile(f'case_images/{photo_path}')
        try:
            msg = await callback_query.message.answer_photo(photo=photo,
                                                            parse_mode="HTML")
        except Exception as e:
            print(e)
        message = await callback_query.message.answer(cases_text, parse_mode="HTML", reply_markup=keyboard)
    else:
        message = await callback_query.message.answer(cases_text, parse_mode="HTML", reply_markup=keyboard)

    # Сохраняем ID сообщения для удаления
    data = await state.get_data()
    msg_ids = data.get("to_delete", [])
    msg_ids.append(message.message_id)
    if case.photo:
        msg_ids.append(msg.message_id)
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
    await send_welcome(callback_query.message)


def log_action(user_id, username, user_name, action, details):
    log_data = {
        'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        'user_id': [user_id],
        'username': [username],
        'user_name': [user_name],
        'action': [action],
        'details': [details]
    }
    df = pd.DataFrame(log_data)

    # Проверяем, существует ли уже файл логов
    try:
        existing_df = pd.read_excel('logs.xlsx')
        df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        pass

    df.to_excel('logs.xlsx', index=False)


# Обработка команды /moderate
@dp.message(Command('moderate'))
async def moderate(message: types.Message):
    try:
        if message.from_user.id == 1324829412:
            # Отправка файла logs.xlsx
            file = FSInputFile('logs.xlsx')
            await message.answer_document(file, caption="Логи действий пользователей")
        else:
            await message.answer("В доступе отказано.")
    except FileNotFoundError:
        await message.answer("Лог-файл не найден.")


class AddingCase(StatesGroup):
    name = State()
    answer = State()
    link = State()
    photo = State()


@dp.message(Command('addcase'))
async def add_case(message: types.Message, state: FSMContext):
    await message.answer("Please send the name of the case.")
    await state.set_state(AddingCase.name)


@dp.message(AddingCase.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Please send the answer/text for the case.")
    await state.set_state(AddingCase.answer)


# Another handler with multiple filters
@dp.message(AddingCase.answer)
async def process_answer(message: types.Message, state: FSMContext):
    await state.set_state(AddingCase.link)
    await state.update_data(answer=message.text)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Skip", callback_data="skip_link")]
    ])
    await message.answer("Please send the link for the case.", reply_markup=keyboard)


@dp.callback_query(F.data == "skip_link")
async def skip_photo(callback_query: types.CallbackQuery, state: FSMContext):
    await process_link(callback_query.message, state, skip=True)
    await callback_query.answer()


@dp.message(AddingCase.link)
async def process_link(message: types.Message, state: FSMContext, skip=False):

    await state.set_state(AddingCase.photo)
    if not skip:
        await state.update_data(link=message.text)
    else:
        await state.update_data(link=None)
    # Create an inline keyboard with a "Skip" button
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Skip", callback_data="skip_photo")]
    ])

    await message.answer("Please send the photo for the case or press 'Skip'.", reply_markup=keyboard)


# Callback handler for the "Skip" button
@dp.callback_query(F.data == "skip_photo")
async def skip_photo(callback_query: types.CallbackQuery, state: FSMContext):
    await process_photo(callback_query.message, state, skip=True)
    await callback_query.answer()


# Message handler for the photo state
@dp.message(AddingCase.photo)
async def process_photo(message: types.Message, state: FSMContext, skip=False):
    data = await state.get_data()
    name = data.get('name')
    answer = data.get('answer')
    link = data.get('link')
    photo = None

    if not skip:
        if message.photo:
            photo = message.photo[-1].file_id
            file_info = await message.bot.get_file(photo)
            file_path = file_info.file_path
            file_name = f"{name.replace(' ', '_')}.jpg"
            file_path_local = os.path.join('case_images', file_name)
            await message.bot.download_file(file_path, file_path_local)
            photo = file_name
    print(name, answer, link, photo)

    conn = sqlite3.connect('cases.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cases (name, answer, link, photo)
        VALUES (?, ?, ?, ?)
    ''', (name, answer, link, photo))
    conn.commit()
    conn.close()

    await message.answer("Case added successfully.")
    await state.clear()


@dp.message(Command('deletecase'))
async def delete_case(message: types.Message):
    conn = sqlite3.connect('cases.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM cases')
    cases = cursor.fetchall()
    conn.close()

    if not cases:
        await message.answer("No cases to delete.")
        return
    buttons = [
        [InlineKeyboardButton(text=case[1], callback_data=f"delete_{case[0]}")]
        for case in cases
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Select a case to delete:", reply_markup=keyboard)


@dp.callback_query(F.data.startswith("delete_"))
async def delete_case_callback(callback_query: types.CallbackQuery):
    case_id = callback_query.data.split("_")[1]

    conn = sqlite3.connect('cases.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cases WHERE id = ?', (case_id,))
    conn.commit()
    conn.close()

    await callback_query.message.answer("Case deleted successfully.")
    await callback_query.message.delete()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    init_db()
    asyncio.run(main())
