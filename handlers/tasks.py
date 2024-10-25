from aiogram import Router, F, html
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.enums import ParseMode

from keyboards.simple_row import make_row_keyboard
from db import DB_Connect

import prettytable as pt


# Create router object
router = Router()

# Actions text
available_actions = ["Посмотреть события 📅", "Добавить событие 📝", "Удалить событие ⛔", "Отмена ❌"]
back_actions = ["Управление событиями ⏰", "Отмена ❌"]
add_actions = ["Добавить событие 📝", "Отмена ❌"]
new_task_actions = ["Подтвердить добавление ✅", "Изменить данные 📝", "Отмена ❌"]
cancel_action = ["Отмена ❌"]
del_actions = ["Посмотреть события 📅", "Отмена ❌"]

# Create states class
class TasksEdit(StatesGroup):
    choosing_tasks_options = State()
    view_tasks_options = State()
    add_task_option = State()
    new_task_option = State()
    del_tasks_options = State()

# Tasks control
@router.message(F.text.lower() == "управление событиями ⏰")
async def cmd_tasks(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите что хотите сделать:",
        reply_markup=make_row_keyboard(available_actions)
    )

# View tasks
@router.message(F.text.lower() == "посмотреть события 📅")
async def cmd_tasks(message: Message, state: FSMContext):
    db = DB_Connect()
    tasks_list = db.view_tasks()
    table = pt.PrettyTable(['ID', 'Событие', 'Имя', 'Дата'])
    table.align['ID'] = 'l'
    table.align['Событие'] = 'r'
    table.align['Имя'] = 'r'
    table.align['Дата'] = 'r'
    for task in tasks_list:
        table.add_row([task[0], task[1], task[2], task[3]])
    await message.answer(
        f"Список событий:\r\n<pre>{table}</pre>",
        parse_mode=ParseMode.HTML,
        reply_markup=make_row_keyboard(back_actions)
    )
    await state.set_state(TasksEdit.view_tasks_options)

# Add task - start
@router.message(F.text.lower() == "добавить событие 📝")
@router.message(F.text.lower() == "изменить данные 📝")
async def add_task(message: Message, state: FSMContext):
    await message.answer(
        text="Введите данные нового события, дата в формате (число.номер месяца), пример:\r\n Название события:Имя:31.03",
        reply_markup=make_row_keyboard(add_actions)
    )
    await state.set_state(TasksEdit.add_task_option)

# Add task - check input
@router.message(TasksEdit.add_task_option, F.text.regexp(r'^.*:.*:.*\..*$'))
async def new_task(message: Message, state: FSMContext):
    await state.update_data(new_task_data=message.text)
    table_data = message.text.split(":")
    table = pt.PrettyTable(['Событие', 'Имя', 'Дата'])
    table.align['Событие'] = 'r'
    table.align['Имя'] = 'r'
    table.align['Дата'] = 'r'
    table.add_row([table_data[0], table_data[1], table_data[2]])
    await message.answer(
        f"Проверьте введенные данные, или измените их если они неправильные:\r\n<pre>{table}</pre>",
        parse_mode=ParseMode.HTML,
        reply_markup=make_row_keyboard(new_task_actions)
    )
    await state.set_state(TasksEdit.new_task_option)

# Add task - bad input
@router.message(TasksEdit.add_task_option)
async def task_format_incorrectly(message: Message):
    await message.answer(
        text="Невозможно распознать данные, попробуйте ещё раз:",
        reply_markup=make_row_keyboard(cancel_action)
    )
# Add task - confirm input
@router.message(TasksEdit.new_task_option, F.text.lower() == "подтвердить добавление ✅")
async def new_task_confirm(message: Message, state: FSMContext):
    task_data = await state.get_data()
    new_task_data = task_data['new_task_data'].split(":")
    db = DB_Connect()
    db.add_new_task(new_task_data[0], new_task_data[1], new_task_data[2])
    await message.answer(
        text=f"Данные успено добавлены, если хотите вернутся в главное меню, то нажмите /start",
        reply_markup=ReplyKeyboardRemove()
    )
    # Reset state
    await state.clear()

# Delete tasks - start
@router.message(F.text.lower() == "удалить событие ⛔")
async def del_tasks_input(message: Message, state: FSMContext):
    db = DB_Connect()
    tasks_list = db.view_tasks()
    table = pt.PrettyTable(['ID', 'Событие', 'Имя', 'Дата'])
    table.align['ID'] = 'l'
    table.align['Событие'] = 'r'
    table.align['Имя'] = 'r'
    table.align['Дата'] = 'r'
    for task in tasks_list:
        table.add_row([task[0], task[1], task[2], task[3]])
    await message.answer(
        f"Для удаления введите ID одного из событий:\r\n<pre>{table}</pre>",
        parse_mode=ParseMode.HTML,
        reply_markup=make_row_keyboard(cancel_action)
    )
    await state.set_state(TasksEdit.del_tasks_options)

# Delete tasks - check input and delete
@router.message(TasksEdit.del_tasks_options, F.text.regexp(r'^\d{1,}$'))
async def del_task(message: Message, state: FSMContext):
    await state.update_data(del_task_data=message.text)
    del_id = message.text
    db = DB_Connect()
    db.del_task(del_id)
    await message.answer(
        text="Данные удалены!",
        reply_markup=make_row_keyboard(del_actions)
    )
    # Reset state
    await state.clear()

# Delete tasks - bad input
@router.message(TasksEdit.del_tasks_options)
async def del_task_format_incorrectly(message: Message):
    await message.answer(
        text="Неправильный формат ID, попробуйте ещё раз:",
        reply_markup=make_row_keyboard(cancel_action)
    )
