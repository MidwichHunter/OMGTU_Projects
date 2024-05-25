from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from sqlalchemy import select

import keyboards as kb
import database.requests as rq
from database.models import async_session, User, Marathone

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Добро пожаловать на Портал Марафонов Death Runner!', reply_markup= kb.main)

@router.message(F.text == 'Проверить/Отменить запись')
async def checked(message: Message):
    user_data = await rq.get_Data()
    if user_data > 0:
        marathon_info = await rq.get_Marathone(user_data)
        await message.answer(f'Вы записаны на Марафон: { marathon_info.name}\n Описание: { marathon_info.description}\n Дата:{ marathon_info.date}\n',reply_markup= await kb.Check_Inject())
    else:
        await message.answer(f'Вы не записаны на Марафон.',reply_markup= await kb.Check_Inject() )


@router.callback_query(F.data.startswith('to_nothing'))
async def category(callback: CallbackQuery):
    await callback.answer('Вы перешли в главное меню')
    await callback.message.answer('Выберите Марафон по категории',
                                  reply_markup=await kb.categories())

@router.callback_query(F.data.startswith('to_lose'))
async def category(callback: CallbackQuery):
    await callback.message.answer('Вы решили убрать запись с марафона',reply_markup= await kb.Inject_confirm())

@router.callback_query(F.data.startswith('end'))
async def category(callback: CallbackQuery):
    user_data = await rq.get_user()
    await rq.delete_FIO()
    await rq.delete_Maraphone()
    await callback.message.answer('Вы стёрли фио и запись на Марафон')


@router.message(F.text == 'Каталог Марафонов')
async def catalog(message: Message):
    await message.answer('Выберите категорию Марафонов', reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберите Марафон по категории',
                                  reply_markup=await kb.Marathone(callback.data.split('_')[1]))

@router.callback_query(F.data.startswith('to_main'))
async def category(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберите Марафон по категории',
                                  reply_markup= await kb.categories())

@router.callback_query(F.data.startswith('to_category'))
async def category(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберите Марафон по категории',
                                  reply_markup=await kb.categories())

@router.callback_query(F.data.startswith('item_'))
async def maraphone(callback: CallbackQuery):
    global item_data
    item_data = await rq.get_Marathone(callback.data.split('_')[1])
    await callback.answer('Вы выбрали Марафон')
    await callback.message.answer(f'Название: {item_data.name}\n Описание: {item_data.description}\n Дата:  {item_data.date}$',reply_markup=await kb.Marathone_confirm(item_data))

@router.callback_query(F.data.startswith('to_confirm'))
async def Confirm_Maraphone(callback: CallbackQuery):
    await callback.message.answer('Укажите своё фио, пример: фио: Иван Иванович Иванов')

@router.message()
async def Confirm_FIO(message: Message):
    global dataset_text
    dataset_text = message.text
    await message.answer(f'Вы ввели: {message.text}',reply_markup= await kb.FIO_confirm())

@router.callback_query(F.data.startswith('to_gone'))
async def Confirm_Maraphone(callback: CallbackQuery):
    await rq.set_FIO(dataset_text)
    await rq.set_Maraphone(item_data.id)
    await callback.message.answer('Данные введены,увидимся на Марафоне')
    

