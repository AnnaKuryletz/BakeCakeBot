from aiogram import types, Router, F
from aiogram.types import FSInputFile
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from backend.bake_cake.bot.models import DeliveryState, CustomCakeState
from aiogram import Bot, types
from config import ADMIN_GROUP_ID
from .keyboards import (
    get_consent_keyboard,
    get_main_menu,
    get_order_menu,
    get_ready_cakes_menu,
    get_custom_cakes_menu,
)
from .notifications import send_order_notification

router = Router()


@router.message(Command("get_group_id"))
async def get_group_id(message: types.Message):
    """Отправляет ID группы"""
    if message.chat.type in ["group", "supergroup"]:
        await message.answer(
            f"ID этой группы: `{message.chat.id}`", parse_mode="Markdown"
        )
    else:
        await message.answer("Эта команда работает только в группах!")


async def send_admin_notification(bot: Bot, text: str):
    """Отправляет уведомление в группу администраторов"""
    await bot.send_message(ADMIN_GROUP_ID, text)


@router.message(Command("start"))
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение с кнопками согласия."""
    user_name = (
        message.from_user.username
        if message.from_user.username
        else message.from_user.first_name
    )
    text = f"Привет, {user_name} 🙋‍♀️! BakeCake приветствует тебя. Для продолжения работы, пожалуйста, подтвердите согласие с обработкой персональных данных."
    consent_file = FSInputFile("files/soglasie.pdf")
    await message.answer(text, reply_markup=get_consent_keyboard())
    await message.answer_document(consent_file)


@router.message(
    lambda message: message.text == "✅Согласен с обработкой персональных данных"
)
async def agree_handler(message: types.Message):
    await message.answer(
        "Вы дали согласие на обработку персональных данных. Можете продолжить работу",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    """Обрабатывает согласие и показывает главное меню."""
    await message.answer(
        "Пожалуйста, выберите, что Вас интересует", reply_markup=get_main_menu()
    )


@router.message(
    lambda message: message.text == "❌Не согласен с обработкой персональных данных"
)
async def disagree_handler(message: types.Message):
    """Обрабатывает отказ и завершает диалог."""
    await message.answer(
        "Вы не согласились с обработкой персональных данных. К сожалению, мы не можем продолжить работу😔.",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.callback_query(F.data == "order_cake")
async def order_cake_callback(callback: CallbackQuery):
    """Обрабатывает нажатие на кнопку 'Хочу заказать торт' и предлагает выбрать тип заказа."""
    await callback.message.answer(
        "Какой торт хотите заказать?", reply_markup=get_order_menu()
    )


@router.callback_query(F.data == "view_prices")
async def view_prices_callback(callback: CallbackQuery):
    """Обрабатывает нажатие на кнопку 'Просмотреть цены'."""
    await callback.message.answer(
        """Вот наш прайс-лист :\n1. Торт "Шоколадное наслаждение"\nОписание: Богатый шоколадный торт с насыщенным вкусом какао, нежным кремом из бельгийского шоколада и легким ароматом ванили. Идеально подойдет для любителей шоколада.\n
Цена: 1500 руб. (1,5 кг)\n
Состав: шоколадный бисквит, ганаш из темного шоколада, сливочное масло, сахар, яйца, ваниль, какао, сливки.\n
2. Торт "Клубничная мечта"\nОписание: Легкий и воздушный торт с нежным бисквитом, пропитанным клубничным сиропом, и слоем сливочного крема с натуральной клубникой.\n
Цена: 1700 руб. (1,8 кг)\n
Состав: ванильный бисквит, клубничное пюре, сливочный крем, сахар, яйца, сливки, желатин, ваниль.\n
3. Торт "Медовик по-домашнему"\n Описание: Классический медовый торт с мягкими медовыми коржами и нежным сметанным кремом. Прекрасное сочетание вкусов для любителей традиционной выпечки.\n
Цена: 1400 руб. (1,5 кг)\n
Состав: мука, мед, сахар, яйца, сливочное масло, сметана, сода, ваниль, грецкие орехи (по желанию).\n
4. Торт "Тропический рай"\n Описание: Экзотический торт с ананасом, кокосом и манго, пропитанный легким цитрусовым сиропом. Освежающий и нежный десерт для жарких дней.\n
Цена: 1800 руб. (1,7 кг)\n
Состав: кокосовый бисквит, ананасовое пюре, манговый мусс, сливки, сахар, яйца, желатин, лаймовый сироп\n
5. Торт "Ореховый шедевр"\nОписание: Насыщенный ореховый торт с карамельно-шоколадным кремом и хрустящими слоями из фундука и миндаля.\n
Цена: 1900 руб. (2 кг)\n
Состав: ореховый бисквит, карамель, шоколадный крем, фундук, миндаль, сливки, сахар, яйца, ваниль.
6. Кастомный торт - +300руб. к стоимости оригинального торта"""
    )


@router.callback_query(F.data == "delivery_time")
async def delivery_time_callback(callback: CallbackQuery):
    """Выдает пользователю дату доставки (текущая + 2 дня)."""
    delivery_date = (datetime.now() + timedelta(days=2)).strftime("%d.%m.%Y")
    await callback.message.answer(f"📦 Ориентировочная дата доставки: {delivery_date}")


@router.callback_query(F.data == "order_ready_cake")
async def order_ready_cake_callback(callback: CallbackQuery):
    """Обрабатывает нажатие на кнопку 'Заказать готовый торт' и показывает список тортов."""
    await callback.message.answer(
        "Выберите один из наших готовых тортов:", reply_markup=get_ready_cakes_menu()
    )


@router.callback_query(F.data.startswith("cake_"))
async def ready_cake_selected(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор готового торта и запрашивает адрес доставки."""
    cakes = {
        "cake_nut_masterpiece": "Торт 'Ореховый шедевр'",
        "cake_tropical_paradise": "Торт 'Тропический рай'",
        "cake_honey_homemade": "Торт 'Медовик по-домашнему'",
        "cake_strawberry_dream": "Торт 'Клубничная мечта'",
        "cake_choco_delight": "Торт 'Шоколадное наслаждение'",
    }

    selected_cake = cakes.get(callback.data, "Неизвестный торт")
    await state.update_data(selected_cake=selected_cake)

    await callback.message.answer(
        f"✅ Вы выбрали торт *{selected_cake}*.\n\n" "📍 Теперь введите адрес доставки:",
        parse_mode="Markdown",
    )

    await state.set_state(DeliveryState.waiting_for_address)
    await callback.answer()


@router.callback_query(F.data == "start_delivery")
async def start_delivery(callback: CallbackQuery, state: FSMContext):
    """Начинаем процесс оформления доставки."""
    await callback.message.answer("📍Пожалуйста, введите адрес доставки:")
    await state.set_state(DeliveryState.waiting_for_address)


@router.message(DeliveryState.waiting_for_address)
async def process_address(message: types.Message, state: FSMContext):
    """Сохраняем адрес и запрашиваем комментарий."""
    await state.update_data(address=message.text)
    await message.answer(
        "Спасибо! Теперь введите ваши пожелания (если есть). Если пожеланий нет, просто напишите 'нет'."
    )
    await state.set_state(DeliveryState.waiting_for_comment)


@router.message(DeliveryState.waiting_for_comment)
async def process_comment(message: types.Message, state: FSMContext, bot: Bot):
    """Сохраняем комментарий, завершаем процесс заказа и уведомляет администраторов."""
    user_data = await state.get_data()
    address = user_data.get("address")
    comment = message.text
    selected_cake = user_data.get("selected_cake", "Кастомный торт")
    cake_text = user_data.get("cake_text", None)  

    base_cake = user_data.get("base_cake")
    if selected_cake and "Кастомный торт" in selected_cake and base_cake:
        selected_cake = f"Заказ: {base_cake} (кастомный)"

    await message.answer(
        f"✅ Ваш заказ оформлен!\n\n📍 Адрес доставки: {address}\n💬 Пожелания: {comment}\n\nСпасибо, что выбрали нас! 🎂"
    )

    await send_order_notification(
        bot, message.from_user, selected_cake, address, comment, cake_text
    )

    await state.clear()


@router.callback_query(F.data == "order_custom_cake")
async def order_custom_cake_callback(callback: CallbackQuery):
    """Выбор торта для кастомизации."""
    await callback.message.answer(
        "Вы выбрали кастомный торт! Пожалуйста, выберите, какой торт хотите кастомизировать:",
        reply_markup=get_custom_cakes_menu(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("custom_cake_"))
async def custom_cake_selected(callback: CallbackQuery, state: FSMContext):
    """Обрабатываем выбор торта для кастомизации и запрашиваем надпись."""
    cakes = {
        "custom_cake_nut_masterpiece": "Торт 'Ореховый шедевр'",
        "custom_cake_tropical_paradise": "Торт 'Тропический рай'",
        "custom_cake_honey_homemade": "Торт 'Медовик по-домашнему'",
        "custom_cake_strawberry_dream": "Торт 'Клубничная мечта'",
        "custom_cake_choco_delight": "Торт 'Шоколадное наслаждение'",
    }

    base_cake = cakes.get(callback.data, "Неизвестный торт")
    await state.update_data(selected_cake="Кастомный торт", base_cake=base_cake)

    await callback.message.answer(
        f"Вы выбрали: {base_cake} 🎂\n\nВведите надпись, которую хотели бы добавить на торт:"
    )

    await state.set_state(CustomCakeState.waiting_for_text)


@router.message(CustomCakeState.waiting_for_text)
async def receive_cake_text(message: types.Message, state: FSMContext, bot: Bot):
    """Сохраняем надпись, подтверждаем заказ и запрашиваем адрес доставки."""
    user_data = await state.get_data()
    selected_cake = user_data.get("selected_cake")
    cake_text = message.text

    await state.update_data(cake_text=cake_text)

    await message.answer(
        f'✅ Вы заказали кастомный {selected_cake}!\n🖋 Надпись: "{cake_text}".\n\n'
        "📍Теперь укажите адрес доставки:",
        reply_markup=types.ReplyKeyboardRemove(),
    )

    await state.set_state(DeliveryState.waiting_for_address)


@router.message(DeliveryState.waiting_for_address)
async def receive_address(message: types.Message, state: FSMContext):
    """Сохраняем адрес и запрашиваем комментарий."""
    address = message.text
    await state.update_data(address=address)

    await message.answer(
        "Спасибо! Теперь введите ваши пожелания (если есть). Если пожеланий нет, просто напишите 'нет'."
    )

    await state.set_state(DeliveryState.waiting_for_comment)
