from aiogram import Router, F, html
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.enums import ParseMode

from keyboards.simple_row import make_row_keyboard
from db import add_new_task, view_tasks

import prettytable as pt
import re


router = Router()

# Actions text
available_actions = ["Посмотреть задания", "Добавить задание", "Удалить задание", "Отмена"]
back_actions = ["Управление заданиями", "Отмена"]
add_actions = ["Добавить задание", "Отмена"]
new_task_actions = ["Подтвердить добавление", "Изменить данные", "Отмена"]
cancel_action = ["Отмена"]


class TasksEdit(StatesGroup):
    choosing_tasks_options = State()
    view_tasks_options = State()
    add_task_option = State()
    new_task_option = State()

# Tasks control
@router.message(F.text.lower() == "управление заданиями")
async def cmd_tasks(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите что хотите сделать:",
        reply_markup=make_row_keyboard(available_actions)
    )

# View tasks
@router.message(F.text.lower() == "посмотреть задания")
async def cmd_tasks(message: Message, state: FSMContext):
    tasks_list = view_tasks()
    table = pt.PrettyTable(['ID', 'Task', 'Name', 'Date'])
    table.align['ID'] = 'l'
    table.align['Task'] = 'r'
    table.align['Name'] = 'r'
    table.align['Date'] = 'r'
    for task in tasks_list:
        table.add_row([task[0], task[1], task[2], task[3]])
    await message.answer(
        f"Список заданий:\r\n<pre>{table}</pre>",
        parse_mode=ParseMode.HTML,
        reply_markup=make_row_keyboard(back_actions)
    )
    await state.set_state(TasksEdit.view_tasks_options)

# Add task
@router.message(F.text.lower() == "добавить задание")
@router.message(F.text.lower() == "изменить данные")
async def add_task(message: Message, state: FSMContext):
    await message.answer(
        text="Введите данные нового задания, дата в формате (число.номер месяца), пример:\r\n Название события:Имя:31.03",
        reply_markup=make_row_keyboard(add_actions)
    )
    await state.set_state(TasksEdit.add_task_option)

@router.message(TasksEdit.add_task_option, F.text.regexp(r'^.*:.*:.*\..*$'))
async def new_task(message: Message, state: FSMContext):
    await state.update_data(new_task_data=message.text)
    table_data = message.text.split(":")
    table = pt.PrettyTable(['Task', 'Name', 'Date'])
    table.align['Task'] = 'r'
    table.align['Name'] = 'r'
    table.align['Date'] = 'r'
    table.add_row([table_data[0], table_data[1], table_data[2]])
    await message.answer(
        f"Проверьте введенные данные, подтвердите или измените их если они неправильные:\r\n<pre>{table}</pre>",
        parse_mode=ParseMode.HTML,
        reply_markup=make_row_keyboard(new_task_actions)
    )
    await state.set_state(TasksEdit.new_task_option)

@router.message(TasksEdit.add_task_option)
async def task_format_incorrectly(message: Message):
    await message.answer(
        text="Невозможно распознать данные, попробуйте ещё раз:",
        reply_markup=make_row_keyboard(cancel_action)
    )

@router.message(TasksEdit.new_task_option, F.text.lower() == "подтвердить добавление")
async def new_task_confirm(message: Message, state: FSMContext):
    task_data = await state.get_data()
    new_task_data = task_data['new_task_data'].split(":")
    print(new_task_data)
    add_new_task(new_task_data[0], new_task_data[1], new_task_data[2])
    await message.answer(
        text=f"Данные успено добавлены, если хотите вернутся в главное меню, то нажмите /start",
        reply_markup=ReplyKeyboardRemove()
    )
    # Reset state
    await state.clear()
