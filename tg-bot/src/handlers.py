from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

main_router = Router()

# ID администратора для отправки заявок
ADMIN_ID = 8233542198
SUPPORT_USERNAME = "@signum_dev"


class RequestStates(StatesGroup):
    waiting_for_request = State()
    waiting_for_budget = State()


def get_main_keyboard():
    """Клавиатура для главного меню"""
    builder = ReplyKeyboardBuilder()
    builder.add(
        types.KeyboardButton(text="🚀 Make Request"),
        types.KeyboardButton(text="🏢 About Company"),
        types.KeyboardButton(text="📞 Contact Support")
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def get_request_type_keyboard():
    """Клавиатура для выбора типа запроса"""
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(text="🤖 Telegram Bot", callback_data="make_tg_bot_request"),
        types.InlineKeyboardButton(text="🌐 Website", callback_data="make_web_request"),
        types.InlineKeyboardButton(text="⚙️ Backend Service", callback_data="make_backend_request"),
        types.InlineKeyboardButton(text="🔧 Technical Help", callback_data="make_help_request"),
        types.InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_request")
    )
    builder.adjust(2)
    return builder.as_markup()


def get_budget_keyboard():
    """Клавиатура для выбора бюджета"""
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(text="💵 $10-50", callback_data="budget_10_50"),
        types.InlineKeyboardButton(text="💰 $50-100", callback_data="budget_50_100"),
        types.InlineKeyboardButton(text="🏦 $100-1000", callback_data="budget_100_1000"),
        types.InlineKeyboardButton(text="🚀 $1000+", callback_data="budget_1000_plus"),
        types.InlineKeyboardButton(text="💬 Custom Budget", callback_data="budget_custom"),
        types.InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_request")
    )
    builder.adjust(2)
    return builder.as_markup()


@main_router.message(Command("start"))
async def start(message: types.Message):
    welcome_text = (
        "👋 **Welcome to Signum!**\n\n"
        "🏢 **About Us:**\n"
        "• 3+ years of commercial development experience\n"
        "• Professional team of developers\n"
        "• Quality assurance & timely delivery\n"
        "• Client-oriented approach\n\n"
        "💼 **Our Services:**\n"
        "• 🤖 Telegram bots & integration\n"
        "• 🌐 Web development & design\n"
        "• ⚙️ Backend services & APIs\n"
        "• 🔧 Technical consulting\n\n"
        "💰 **Pricing Information:**\n"
        "• **Rate:** $10/hour per developer\n"
        "• **All project types** have the same rate\n"
        "• Final cost depends on project complexity\n\n"
        "📞 **For questions contact:** {support}\n\n"
        "Choose an option below: 👇"
    ).format(support=SUPPORT_USERNAME)

    await message.answer(
        text=welcome_text,
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )


@main_router.message(F.text == "🚀 Make Request")
async def make_request(message: types.Message):
    text = (
        "🚀 **Choose Project Type**\n\n"
        "Select the type of development you need:\n\n"
        "• 🤖 **Telegram Bot** - Bots, automation, integration\n"
        "• 🌐 **Website** - Web applications, landing pages\n"
        "• ⚙️ **Backend Service** - APIs, databases, servers\n"
        "• 🔧 **Technical Help** - Consultation, code review\n\n"
        "💰 **Standard Rate:** $10/hour per developer\n"
        "*(same for all project types)*\n\n"
        "Click on the desired option:"
    )
    await message.answer(text, reply_markup=get_request_type_keyboard(), parse_mode="Markdown")


@main_router.message(F.text == "🏢 About Company")
async def about_company(message: types.Message):
    about_text = (
        "🏢 **About Signum**\n\n"
        "✅ **3+ years** of commercial development experience\n"
        "✅ **Professional team** of skilled developers\n"
        "✅ **Quality assurance** and timely delivery\n"
        "✅ **Client-oriented** approach\n\n"
        "🛠 **Our Expertise:**\n"
        "• 🤖 Telegram bots & automation\n"
        "• 🌐 Modern web development\n"
        "• ⚙️ Backend & API development\n"
        "• 📱 Mobile applications\n"
        "• 🗄 Database design & optimization\n\n"
        "💰 **Pricing:**\n"
        "• **$10/hour** per developer\n"
        "• **Same rate** for all project types\n"
        "• **Transparent** pricing\n"
        "• **No hidden** costs\n\n"
        "💡 **We bring your ideas to life!**\n\n"
        "📞 Contact us: {support}"
    ).format(support=SUPPORT_USERNAME)

    await message.answer(about_text, parse_mode="Markdown")


@main_router.message(F.text == "📞 Contact Support")
async def contact_support(message: types.Message):
    contact_text = (
        "📞 **Contact Signum**\n\n"
        "For technical questions and support:\n"
        "👨‍💻 {support}\n\n"
        "💰 **Pricing:** $10/hour per developer\n"
        "📋 **All project types** - same rate\n\n"
        "For new project requests:\n"
        "🚀 Click 'Make Request' button\n\n"
        "We'll be happy to help you! 💼"
    ).format(support=SUPPORT_USERNAME)

    await message.answer(contact_text, parse_mode="Markdown")


@main_router.callback_query(F.data.startswith("make_") and F.data.endswith("_request"))
async def handle_request_type(callback: types.CallbackQuery, state: FSMContext):
    request_type = callback.data

    # Сохраняем тип запроса в состоянии
    await state.update_data(request_type=request_type)

    # Переходим к описанию задачи
    await state.set_state(RequestStates.waiting_for_request)

    type_display_map = {
        "make_tg_bot_request": "Telegram Bot",
        "make_web_request": "Website",
        "make_backend_request": "Backend Service",
        "make_help_request": "Technical Help"
    }

    type_display = type_display_map.get(request_type, "Project")

    text = (
        f"📝 **{type_display} Development**\n\n"
        "💰 **Rate:** $10/hour per developer\n"
        "*(same for all project types)*\n\n"
        "Please describe in detail what you want to develop:\n\n"
        "• **Features and functionality**\n"
        "• **Technical requirements**\n"
        "• **Design preferences**\n"
        "• **Any specific technologies**\n\n"
        "✍️ Write everything that comes to mind:"
    )

    await callback.message.edit_text(text, parse_mode="Markdown")
    await callback.answer()


@main_router.message(RequestStates.waiting_for_request)
async def process_request_description(message: types.Message, state: FSMContext):
    request_description = message.text
    user = message.from_user

    # Сохраняем описание и информацию о пользователе
    await state.update_data(
        request_description=request_description,
        user_id=user.id,
        username=user.username,
        full_name=user.full_name
    )

    # Запрашиваем бюджет
    await state.set_state(RequestStates.waiting_for_budget)

    text = (
        "💰 **Budget Selection**\n\n"
        "💵 **Standard Rate:** $10/hour per developer\n\n"
        "Please choose your budget range:\n\n"
        "• **💵 $10-50** - Small tasks, quick fixes\n"
        "• **💰 $50-100** - Medium tasks, consultations\n"
        "• **🏦 $100-1000** - Full projects, development\n"
        "• **🚀 $1000+** - Complex solutions, teams\n"
        "• **💬 Custom** - Specify your exact budget\n\n"
        "Select an option:"
    )

    await message.answer(text, reply_markup=get_budget_keyboard(), parse_mode="Markdown")


@main_router.callback_query(F.data.startswith("budget_"))
async def process_budget_callback(callback: types.CallbackQuery, state: FSMContext):
    budget_data = callback.data

    budget_map = {
        "budget_10_50": "$10-50",
        "budget_50_100": "$50-100",
        "budget_100_1000": "$100-1000",
        "budget_1000_plus": "$1000+",
        "budget_custom": "custom"
    }

    budget = budget_map.get(budget_data)

    if budget_data == "budget_custom":
        await callback.message.edit_text(
            "💬 **Custom Budget**\n\n"
            "💰 **Standard Rate:** $10/hour per developer\n\n"
            "Please specify your budget:\n"
            "• Fixed amount (e.g., $75)\n"
            "• Hourly rate preference\n"
            "• Project-based pricing\n\n"
            "✍️ Write your budget:"
        )
        await callback.answer()
        return

    # Завершаем обработку с выбранным бюджетом
    await finish_request_processing(callback.message, state, budget)
    await callback.answer()


@main_router.message(RequestStates.waiting_for_budget)
async def process_custom_budget(message: types.Message, state: FSMContext):
    budget = message.text
    await finish_request_processing(message, state, f"Custom: {budget}")


async def finish_request_processing(message: types.Message, state: FSMContext, budget: str):
    data = await state.get_data()
    request_type = data.get('request_type')
    request_description = data.get('request_description')
    user_id = data.get('user_id')
    username = data.get('username')
    full_name = data.get('full_name')

    type_display_map = {
        "make_tg_bot_request": "Telegram Bot",
        "make_web_request": "Website",
        "make_backend_request": "Backend Service",
        "make_help_request": "Technical Help"
    }

    request_type_display = type_display_map.get(request_type, "Project")

    # Текст для пользователя
    user_response = (
        "✅ **Thank you for your request!**\n\n"
        f"**Project Type:** {request_type_display}\n"
        f"**Your Budget:** {budget}\n\n"
        "💰 **Our Rate:** $10/hour per developer\n"
        "*(same for all project types)*\n\n"
        "🚀 **Signum Team** will contact you within 24 hours!\n\n"
        "We have **3+ years of commercial development experience** "
        "and are ready to help bring your project to life!\n\n"
        f"📞 For questions: {SUPPORT_USERNAME}"
    )

    # Формируем заявку для администратора
    admin_notification = (
        "🆕 **NEW PROJECT REQUEST**\n\n"
        f"👤 **Client:** {full_name}\n"
        f"🆔 **User ID:** {user_id}\n"
        f"📧 **Username:** @{username if username else 'No username'}\n\n"
        f"📋 **Project Type:** {request_type_display}\n"
        f"💰 **Budget:** {budget}\n\n"
        f"📝 **Project Description:**\n{request_description}\n\n"
        f"🏢 **Signum** - 3+ years of commercial development experience\n"
        f"💵 **Rate:** $10/hour per developer\n"
        f"📞 **Support:** {SUPPORT_USERNAME}"
    )

    try:
        # Отправляем заявку администратору
        await message.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_notification,
            parse_mode="Markdown"
        )

        # Уведомляем пользователя
        await message.answer(user_response, parse_mode="Markdown", reply_markup=get_main_keyboard())

    except Exception as e:
        # В случае ошибки отправки администратору
        error_response = (
            "✅ **Thank you for your request!**\n\n"
            "We have received your information and will contact you soon.\n\n"
            "⚠️ *There was a temporary issue, but your request is saved.*\n\n"
            f"📞 Contact us directly: {SUPPORT_USERNAME}"
        )
        await message.answer(error_response, reply_markup=get_main_keyboard())

        print(f"Error sending notification to admin: {e}")

    # Очищаем состояние
    await state.clear()


@main_router.callback_query(F.data == "cancel_request")
async def cancel_request(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "❌ **Request cancelled**\n\n"
        "💰 **Remember our rate:** $10/hour per developer\n\n"
        "If you change your mind, feel free to create a new request!\n\n"
        f"📞 Questions? Contact: {SUPPORT_USERNAME}",
        parse_mode="Markdown"
    )
    await callback.answer()


@main_router.message(Command("help"))
async def help_command(message: types.Message):
    help_text = (
        "🆘 **Help**\n\n"
        "**Available Commands:**\n"
        "/start - Main menu\n"
        "/help - This help message\n"
        "/price - Pricing information\n\n"
        "💰 **Pricing Information:**\n"
        "• $10/hour per developer\n"
        "• Same rate for all project types\n"
        "• Transparent pricing\n\n"
        "**How to make a request:**\n"
        "1. Click '🚀 Make Request'\n"
        "2. Choose project type\n"
        "3. Describe your project\n"
        "4. Select budget\n\n"
        f"**Support:** {SUPPORT_USERNAME}\n\n"
        "We're here to help! 💪"
    )
    await message.answer(help_text, parse_mode="Markdown", reply_markup=get_main_keyboard())


@main_router.message(Command("price"))
async def price_command(message: types.Message):
    price_text = (
        "💰 **Pricing Information**\n\n"
        "**Standard Rate:** $10/hour per developer\n\n"
        "**This rate applies to:**\n"
        "• 🤖 Telegram Bot development\n"
        "• 🌐 Website development\n"
        "• ⚙️ Backend services\n"
        "• 🔧 Technical consulting\n"
        "• All other project types\n\n"
        "**Budget Ranges:**\n"
        "• 💵 $10-50 - Small tasks, quick fixes\n"
        "• 💰 $50-100 - Medium tasks, consultations\n"
        "• 🏦 $100-1000 - Full projects, development\n"
        "• 🚀 $1000+ - Complex solutions, teams\n\n"
        "Final cost depends on project complexity and time required.\n\n"
        f"📞 Questions? Contact: {SUPPORT_USERNAME}"
    )
    await message.answer(price_text, parse_mode="Markdown", reply_markup=get_main_keyboard())