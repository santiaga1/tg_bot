from aiogram import Router, F, html, Bot, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.enums import ParseMode
from aiogram.enums.dice_emoji import DiceEmoji

from keyboards.simple_row import make_row_keyboard

# Get config from .env
from config_reader import config


# Create router object
router = Router()

# Actions text
available_actions = ["Test 🎲", "Отмена ❌"]

# Other control
@router.message(F.text.lower() == "другие действия ⭐")
async def cmd_other(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите действие:",
        reply_markup=make_row_keyboard(available_actions)
    )

@router.message(F.text.lower() == "test 🎲")
async def cmd_dice(message: types.Message, bot: Bot):
    await bot.send_dice(config.group_id.get_secret_value(), emoji=DiceEmoji.DICE)
