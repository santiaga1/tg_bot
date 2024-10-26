from aiogram import Router, F, html, Bot, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineQuery, ReplyKeyboardRemove
from aiogram.enums import ParseMode
from aiogram.enums.dice_emoji import DiceEmoji

from keyboards.simple_row import create_inline_kb

# Get config from .env
from config_reader import config


# Create router object
router = Router()

# Other control
@router.callback_query(F.data == "other")
async def manage_other(callback: CallbackQuery, state: FSMContext):
    available_actions = [
        ["Test 🎲", "test_act"],
        ["Отмена ❌", "cancel"]
    ]
    await callback.message.edit_text(
        text='Выберите действие:',
        reply_markup=create_inline_kb(2, available_actions)
    )
    await callback.answer()

# Test action
@router.callback_query(F.data == "test_act")
async def cmd_dice(callback: CallbackQuery, bot: Bot):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await bot.send_dice(config.group_id.get_secret_value(), emoji=DiceEmoji.DICE)
