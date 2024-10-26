from aiogram import Router, F, html
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineQuery, ReplyKeyboardRemove
from aiogram.enums import ParseMode

from keyboards.simple_row import create_inline_kb
from db import DB_Connect

import prettytable as pt


# Create router object
router = Router()

# Create states class
class TasksEdit(StatesGroup):
    view_tasks_options = State()
    add_task_option = State()
    new_task_option = State()
    del_tasks_options = State()

# Manage tasks
@router.callback_query(F.data == "manage_tasks")
async def manage_tasks(callback: CallbackQuery, state: FSMContext):
    available_actions = [
        ["Посмотреть события 📅", "view_tasks"],
        ["Добавить событие 📝", "add_task"],
        ["Удалить событие ⛔", "del_task"],
        ["Отмена ❌", "cancel"]
    ]
    await callback.message.edit_text(
        text='Выберите что хотите сделать:',
        reply_markup=create_inline_kb(2, available_actions)
    )
    await callback.answer()

# View tasks
@router.callback_query(F.data == "view_tasks")
async def view_tasks(callback: CallbackQuery, state: FSMContext):
    available_actions = [
        ["Управление событиями ⏰", "manage_tasks"],
        ["Отмена ❌", "cancel"]
    ]
    await state.set_state(TasksEdit.view_tasks_options)
    db = DB_Connect()
    tasks_list = db.view_tasks()
    table = pt.PrettyTable(['ID', 'Событие', 'Имя', 'Дата'])
    table.align['ID'] = 'l'
    table.align['Событие'] = 'r'
    table.align['Имя'] = 'r'
    table.align['Дата'] = 'r'
    for task in tasks_list:
        table.add_row([task[0], task[1], task[2], task[3]])
    await callback.message.edit_text(
        f"Список событий:\r\n<pre>{table}</pre>",
        parse_mode=ParseMode.HTML,
        reply_markup=create_inline_kb(2, available_actions)
    )
    await callback.answer()

# Add task - start
@router.callback_query(F.data == "add_task")
async def add_task(callback: CallbackQuery, state: FSMContext):
    available_actions = [
        ["Отмена ❌","cancel"]
    ]
    await callback.message.edit_text(
        f"Введите данные нового события,\r\nдата должна быть в формате (число.номер месяца),\r\nпример:\r\n<pre>Название события:Имя:31.03</pre>",
        parse_mode=ParseMode.HTML,
        reply_markup=create_inline_kb(1, available_actions)
    )
    await state.set_state(TasksEdit.add_task_option)
    await callback.answer()

# Add task - check input
@router.message(TasksEdit.add_task_option, F.text.regexp(r'^.*:.*:.*\..*$'))
async def new_task(message: Message, state: FSMContext):
    await state.update_data(new_task_data=message.text)
    available_actions = [
        ["Подтвердить добавление ✅", "confirm_add_task"],
        ["Изменить данные 📝", "add_task"],
        ["Отмена ❌","cancel"]
    ]
    table_data = message.text.split(":")
    table = pt.PrettyTable(['Событие', 'Имя', 'Дата'])
    table.align['Событие'] = 'r'
    table.align['Имя'] = 'r'
    table.align['Дата'] = 'r'
    table.add_row([table_data[0], table_data[1], table_data[2]])
    await message.answer(
        f"Проверьте введенные данные, или измените их если они неправильные:\r\n<pre>{table}</pre>",
        parse_mode=ParseMode.HTML,
        reply_markup=create_inline_kb(2, available_actions)
    )
    await state.set_state(TasksEdit.new_task_option)

# Add task - bad input
@router.message(TasksEdit.add_task_option)
async def task_format_incorrectly(message: Message):
    available_actions = [
        ["Отмена ❌","cancel"]
    ]
    await message.answer(
        text="Невозможно распознать данные, попробуйте ещё раз:",
        reply_markup=create_inline_kb(1, available_actions)
    )

# Add task - confirm input
@router.callback_query(F.data == "confirm_add_task")
async def new_task_confirm(callback: CallbackQuery, state: FSMContext):
    task_data = await state.get_data()
    new_task_data = task_data['new_task_data'].split(":")
    db = DB_Connect()
    db.add_new_task(new_task_data[0], new_task_data[1], new_task_data[2])
    await callback.message.edit_text(
        text=f"Данные успено добавлены!\r\nЕсли хотите вернутся в главное меню, то нажмите /start",
        reply_markup=None
    )
    # Reset state
    await state.clear()
    await callback.answer()

# Delete tasks - start
@router.callback_query(F.data == "del_task")
async def del_tasks_input(callback: CallbackQuery, state: FSMContext):
    available_actions = [
        ["Отмена ❌","cancel"]
    ]
    db = DB_Connect()
    tasks_list = db.view_tasks()
    table = pt.PrettyTable(['ID', 'Событие', 'Имя', 'Дата'])
    table.align['ID'] = 'l'
    table.align['Событие'] = 'r'
    table.align['Имя'] = 'r'
    table.align['Дата'] = 'r'
    for task in tasks_list:
        table.add_row([task[0], task[1], task[2], task[3]])
    await callback.message.edit_text(
        f"Для удаления введите ID одного из событий:\r\n<pre>{table}</pre>",
        parse_mode=ParseMode.HTML,
        reply_markup=create_inline_kb(2, available_actions)
    )
    await state.set_state(TasksEdit.del_tasks_options)
    await callback.answer()

# Delete tasks - check input and delete
@router.message(TasksEdit.del_tasks_options, F.text.regexp(r'^\d{1,}$'))
async def del_task(message: Message, state: FSMContext):
    await state.update_data(del_task_data=message.text)
    available_actions = [
        ["Посмотреть события 📅","view_tasks"],
        ["Отмена ❌","cancel"]
    ]
    del_id = message.text
    db = DB_Connect()
    db.del_task(del_id)
    await message.answer(
        text="Данные удалены!",
        reply_markup=create_inline_kb(2, available_actions)
    )
    # Reset state
    await state.clear()

# Delete tasks - bad input
@router.message(TasksEdit.del_tasks_options)
async def del_task_format_incorrectly(message: Message):
    available_actions = [
        ["Отмена ❌","cancel"]
    ]
    await message.answer(
        text="Неправильный формат ID, попробуйте ещё раз:",
        reply_markup=create_inline_kb(1, available_actions)
    )
