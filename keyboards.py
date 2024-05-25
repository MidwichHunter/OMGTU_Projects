from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.requests import get_categories, get_category_item

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каталог Марафонов')],
                                     [KeyboardButton(text='Проверить/Отменить запись')],
                                     [KeyboardButton(text='Контакты'),
                                      KeyboardButton(text='О нас')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')


async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


async def Marathone(category_id):
    all_marathones = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()
    for marathone in all_marathones:
        keyboard.add(InlineKeyboardButton(text=marathone.name, callback_data=f"item_{marathone.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()

async def Marathone_confirm(marathone_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='to_category'))
    keyboard.add(InlineKeyboardButton(text='Подтвердить', callback_data='to_confirm'))
    return keyboard.adjust(2).as_markup()

async def Marathone_FIO(message):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='to_confirm'))
    keyboard.add(InlineKeyboardButton(text='Подтвердить', callback_data='to_gone'))
    return keyboard.adjust(2).as_markup()

async def FIO_confirm():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='to_confirm'))
    keyboard.add(InlineKeyboardButton(text='Подтвердить', callback_data='to_gone'))
    return keyboard.adjust(2).as_markup()

async def Check_Inject():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Окей', callback_data='to_nothing'))
    keyboard.add(InlineKeyboardButton(text='Отменить Запись', callback_data='to_lose'))
    return keyboard.adjust(2).as_markup()

async def Inject_confirm():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Я передумал', callback_data='to_nothing'))
    keyboard.add(InlineKeyboardButton(text='Отменить Запись', callback_data='end'))
    return keyboard.adjust(2).as_markup()