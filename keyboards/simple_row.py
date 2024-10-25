from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Keyboard function (create keyboard buttons from list)
def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)
