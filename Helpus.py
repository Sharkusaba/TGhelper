import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Чтение токена из .env файла
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN_HELPUS')

if not TOKEN:
    raise ValueError("❌ Токен бота не найден! Добавьте TELEGRAM_BOT_TOKEN_HELPUS в файл .env")

ABOUT_TEXT = """🎌 Анимешники России — общественно-политическое движение, собравшее вокруг себя всех поклонников японской культуры. С 1905 года мы защищаем гордость и честь отечественных отаку.

📜 Нашу программу можно увидеть на нашем сайте."""

CONTACTS_TEXT = """📬 Вы можете написать нам на почту anime.rossii@yandex.ru либо написать в личные сообщения телеграмм группы"""

REGIONS = {
    "🏛️ Москва": {
        "telegram": "t.me/animepartiyaMSK",
        "vk": "vk.ru/animepartiyamsk"
    },
    "🏰 Санкт-Петербург": {
        "telegram": "t.me/animepartiyaSPB",
        "vk": "vk.ru/animepartiyaspb"
    },
    "❄️ Вологда": {
        "telegram": "t.me/animepartiyaVLG",
        "vk": "vk.com/animepartiyaVLG"
    },
    "🌳 Воронеж": {
        "telegram": "t.me/animepartiyaVRN",
        "vk": "vk.ru/animepartiyaVRN"
    },
    "🌲 Томск": {
        "telegram": "t.me/animepartiyaTOM",
        "vk": "vk.ru/animepartiyaTOM"
    }
}

MAIN_PHOTO_URL = "https://i.ibb.co/67Cx6LfZ/2026-02-02-000614281.png"

JOIN_LINK = "https://forms.yandex.ru/cloud/697f18c84936394858d64f57"


def create_button(text, callback_data=None, url=None):
    if url:
        return InlineKeyboardButton(text, url=url)
    else:
        return InlineKeyboardButton(text, callback_data=callback_data, switch_inline_query_current_chat=None)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [create_button("📖 О нас", callback_data="about")],
        [create_button("🏛️ Партийные отделения", callback_data="regions")],
        [create_button("📞 Наши контакты", callback_data="contacts")],
        [create_button("🤝 Вступить к нам", callback_data="join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo=MAIN_PHOTO_URL,
        caption="🎌 Добро пожаловать в Анимешники России! Выберите опцию:",
        reply_markup=reply_markup
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "main_menu":
        keyboard = [
            [create_button("📖 О нас", callback_data="about")],
            [create_button("🏛️ Партийные отделения", callback_data="regions")],
            [create_button("📞 Наши контакты", callback_data="contacts")],
            [create_button("🤝 Вступить к нам", callback_data="join")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_media(
            InputMediaPhoto(media=MAIN_PHOTO_URL, caption="🎌 Добро пожаловать в Анимешники России! Выберите опцию:"),
            reply_markup=reply_markup
        )

    elif data == "about":
        keyboard = [
            [create_button("🌐 Наш сайт", url="https://анимепартия.рф")],
            [create_button("📢 Наш телеграм", url="https://t.me/animepartiya")],
            [create_button("↩️ Назад", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_caption(
            caption=ABOUT_TEXT,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )

    elif data == "regions":
        keyboard = []
        for region in REGIONS.keys():
            keyboard.append([create_button(region, callback_data=f"region_{region}")])
        keyboard.append([create_button("↩️ Назад", callback_data="main_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_caption(
            caption="📍 Выберите город:",
            reply_markup=reply_markup
        )

    elif data.startswith("region_"):
        region_name = data.replace("region_", "")
        region_data = REGIONS.get(region_name)

        if not region_data:
            # Если не нашли с эмодзи, ищем без эмодзи в ключах
            for key in REGIONS.keys():
                if region_name in key:
                    region_data = REGIONS[key]
                    break

        keyboard = [
            [create_button("📱 Telegram", url=region_data["telegram"])],
            [create_button("🔵 VK", url=region_data["vk"])],
            [create_button("↩️ Назад", callback_data="regions")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        display_name = region_name
        # Восстанавливаем эмодзи в названии для отображения
        for key in REGIONS.keys():
            if region_name in key:
                display_name = key
                break
        
        await query.edit_message_caption(
            caption=f"📍 <b>{display_name}</b>\n\n🔗 Ссылки на наши соцсети:",
            parse_mode='HTML',
            reply_markup=reply_markup
        )

    elif data == "contacts":
        keyboard = [
            [create_button("📱 Telegram группа", url="https://t.me/animepartiya")],
            [create_button("↩️ Назад", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_caption(
            caption=CONTACTS_TEXT,
            reply_markup=reply_markup
        )

    elif data == "join":
        keyboard = [
            [create_button("📝 Заполнить анкету", url=JOIN_LINK)],
            [create_button("↩️ Назад", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_caption(
            caption="📋 Для вступления в наши ряды заполните анкету по ссылке ниже:",
            reply_markup=reply_markup
        )


def main() -> None:
    # Проверка токена
    if not TOKEN:
        logger.error("Токен бота не найден! Проверьте файл .env")
        return
    
    logger.info(f"Бот запускается с токеном: {TOKEN[:10]}...")

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    logger.info("Бот запущен в режиме polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
