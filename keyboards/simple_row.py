from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Keyboard function (create inline keyboard buttons from list)
def create_inline_kb(width, args) -> InlineKeyboardMarkup:
    # Init builder
    kb_builder = InlineKeyboardBuilder()
    # Init button list
    buttons = []
    # Create buttons from args list
    for text, button in args:
        buttons.append(
            InlineKeyboardButton(
                text=text,
                callback_data=button
            )
        )
    # Unpack buttons to builder with width parameter
    kb_builder.row(*buttons, width=width)
    # Return inline keyboard object
    return kb_builder.as_markup()
