from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, InlineQuery, ReplyKeyboardRemove

from keyboards.simple_row import create_inline_kb


router = Router()

# Start action
@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    available_actions = [
        ["Управление событиями ⏰", "manage_tasks"],
        ["Другие действия ⭐", "other"],
        ["Отмена ❌", "cancel"]
    ]
    await message.answer(
        text="Выберите, что хотите сделать: ",
        reply_markup=create_inline_kb(2, available_actions)
    )

# Cancel actions
@router.callback_query(StateFilter(None), F.data == "cancel")
async def cmd_cancel_no_state(callback: CallbackQuery, state: FSMContext):
    await state.set_data({})
    await callback.message.edit_text(
        text='Работа с ботом завершена,\r\nдля возврата к боту нажмите /start',
        reply_markup=None
    )
    await callback.answer()

@router.callback_query(F.data == "cancel")
async def cmd_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        text='Работа с ботом завершена,\r\nдля возврата к боту нажмите /start',
        reply_markup=None
    )
    await callback.answer()
