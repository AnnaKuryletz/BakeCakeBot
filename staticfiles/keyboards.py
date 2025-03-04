from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from django.db.models import QuerySet
from bot.models import StandardCake
from asgiref.sync import sync_to_async


def get_consent_keyboard():
    """Создает клавиатуру с кнопками согласия и отказа."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅Согласен с обработкой персональных данных")],
            [KeyboardButton(text="❌Не согласен с обработкой персональных данных")],
        ],
        resize_keyboard=True,
    )
    return keyboard


def get_main_menu():
    """Главное меню с кнопками (InlineKeyboard)."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎂Хочу заказать торт", callback_data="order_cake"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💰Просмотреть цены и описание тортов",
                    callback_data="view_prices",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📬Узнать сроки доставки", callback_data="delivery_time"
                )
            ],
        ]
    )


def get_order_menu():
    """Меню выбора типа заказа торта."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎂Заказать готовый торт", callback_data="order_ready_cake"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎨Заказать кастомный торт", callback_data="order_custom_cake"
                )
            ],
        ]
    )


@sync_to_async
def get_cakes_from_db():
    try:
        return list(
            StandardCake.objects.all())
    except Exception as e:
        print(f"Error: {e}")
        return []


async def get_ready_cakes_menu():
    """Меню с выбором готовых тортов."""
    cakes = await get_cakes_from_db()

    # Создаем клавиатуру
    inline_buttons = []

    for cake in cakes:
        button_text = f"🍰 {cake.name} - {cake.price} руб."
        callback_data = f"cake_{cake.id}"  # Используем ID торта в качестве callback_data
        inline_buttons.append(InlineKeyboardButton(text=button_text, callback_data=callback_data))

    # Разбиваем кнопки на строки (например, по 2 кнопки в строке)
    row_width = 2
    rows = [inline_buttons[i:i + row_width] for i in range(0, len(inline_buttons), row_width)]

    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_level_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1 уровень", callback_data="level_1"),
                InlineKeyboardButton(text="2 уровня", callback_data="level_2"),
            ],
            [
                InlineKeyboardButton(text="3 уровня", callback_data="level_3")
            ]
        ]
    )
    return keyboard


def get_shape_keyboard():
    """Создаем клавиатуру для выбора формы торта"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Круглый", callback_data="shape_circle"),
            InlineKeyboardButton(text="Квадратный", callback_data="shape_square"),
        ],
        [
            InlineKeyboardButton(text="Прямоугольный", callback_data="shape_rectangle")
        ]
    ])
    return keyboard


def get_topping_keyboard():
    """Создаем клавиатуру для выбора топпинга торта"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Без топпинга", callback_data="topping_none"),
            InlineKeyboardButton(text="Белый соус", callback_data="topping_white_sauce"),
        ],
        [
            InlineKeyboardButton(text="Карамельный сироп", callback_data="topping_caramel_syrup"),
            InlineKeyboardButton(text="Кленовый сироп", callback_data="topping_maple_syrup"),
        ],
        [
            InlineKeyboardButton(text="Клубничный сироп", callback_data="topping_strawberry_syrup"),
            InlineKeyboardButton(text="Черничный сироп", callback_data="topping_blueberry_syrup"),
        ],
        [
            InlineKeyboardButton(text="Молочный шоколад", callback_data="topping_milk_chocolate"),
        ]
    ])
    return keyboard


def get_berries_keyboard():
    """Создаем клавиатуру для выбора ягод"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Малина", callback_data="berry_raspberry"),
            InlineKeyboardButton(text="Голубика", callback_data="berry_blueberry"),
        ],
        [
            InlineKeyboardButton(text="Клубника", callback_data="berry_strawberry"),
            InlineKeyboardButton(text="Ежевика", callback_data="berry_blackberry"),
        ]
    ])
    return keyboard

def get_decor_keyboard():
    """Создаем клавиатуру для выбора декора"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Фисташки", callback_data="decor_pistachios"),
            InlineKeyboardButton(text="Безе", callback_data="decor_meringue"),
        ],
        [
            InlineKeyboardButton(text="Фундук", callback_data="decor_hazelnut"),
            InlineKeyboardButton(text="Пекан", callback_data="decor_pecan"),
        ],
        [
            InlineKeyboardButton(text="Маршмеллоу", callback_data="decor_marshmallow"),
            InlineKeyboardButton(text="Марципан", callback_data="decor_marzipan"),
        ]
    ])
    return keyboard






