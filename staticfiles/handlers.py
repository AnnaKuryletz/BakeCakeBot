from aiogram import types, Router, F
from aiogram.types import FSInputFile
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from .keyboards import get_consent_keyboard, get_main_menu, get_order_menu, get_ready_cakes_menu

router = Router()

@router.message(Command("start"))
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение с кнопками согласия."""
    user_name = message.from_user.username if message.from_user.username else message.from_user.first_name
    text = f"Привет, {user_name} 🙋‍♀️! Для продолжения работы, пожалуйста, подтвердите согласие с обработкой персональных данных."
    consent_file = FSInputFile("files/soglasie.pdf")
    await message.answer(text, reply_markup=get_consent_keyboard())
    await message.answer_document(consent_file)

@router.message(lambda message: message.text == "Согласен с обработкой персональных данных")
async def agree_handler(message: types.Message):
    await message.answer(
        "Вы дали согласие на обработку персональных данных. Можете продолжить работу.", 
        reply_markup=types.ReplyKeyboardRemove()
    )
    """Обрабатывает согласие и показывает главное меню."""
    await message.answer("Пожалуйста, выберите, что Вас интересует", reply_markup=get_main_menu())

@router.message(lambda message: message.text == "Не согласен с обработкой персональных данных")
async def disagree_handler(message: types.Message):
    """Обрабатывает отказ и завершает диалог."""
    await message.answer(
        "Вы не согласились с обработкой персональных данных. К сожалению, мы не можем продолжить работу.", 
        reply_markup=types.ReplyKeyboardRemove()
    )

@router.callback_query(F.data == "order_cake")
async def order_cake_callback(callback: CallbackQuery):
    """Обрабатывает нажатие на кнопку 'Хочу заказать торт' и предлагает выбрать тип заказа."""
    await callback.message.answer("Какой торт хотите заказать?", reply_markup=get_order_menu())

@router.callback_query(F.data == "view_prices")
async def view_prices_callback(callback: CallbackQuery):
    """Обрабатывает нажатие на кнопку 'Просмотреть цены'."""
    await callback.message.answer('''Вот наш прайс-лист :\n1. Торт "Шоколадное наслаждение"\nОписание: Богатый шоколадный торт с насыщенным вкусом какао, нежным кремом из бельгийского шоколада и легким ароматом ванили. Идеально подойдет для любителей шоколада.\n
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
Состав: ореховый бисквит, карамель, шоколадный крем, фундук, миндаль, сливки, сахар, яйца, ваниль.''')

@router.callback_query(F.data == "order_ready_cake")
async def order_ready_cake_callback(callback: CallbackQuery):
    """Обрабатывает нажатие на кнопку 'Заказать готовый торт' и показывает список тортов."""
    await callback.message.answer("Выберите один из наших готовых тортов:", reply_markup=get_ready_cakes_menu())

@router.callback_query(F.data.startswith("cake_"))
async def ready_cake_selected(callback: CallbackQuery):
    """Обрабатывает выбор конкретного торта."""
    cakes = {
        "cake_nut_masterpiece": "Торт 'Ореховый шедевр'",
        "cake_tropical_paradise": "Торт 'Тропический рай'",
        "cake_honey_homemade": "Торт 'Медовик по-домашнему'",
        "cake_strawberry_dream": "Торт 'Клубничная мечта'",
        "cake_choco_delight": "Торт 'Шоколадное наслаждение'"
    }
    
    selected_cake = cakes.get(callback.data, "Неизвестный торт")
    await callback.message.answer(f"Вы выбрали: {selected_cake}\nСкоро добавим возможность оформить заказ!")

@router.callback_query(F.data == "order_custom_cake")
async def order_custom_cake_callback(callback: CallbackQuery):
    """Обрабатывает нажатие на кнопку 'Заказать кастомный торт'."""
    await callback.message.answer("Вы выбрали кастомный торт! Оформление заказа скоро будет доступно.")