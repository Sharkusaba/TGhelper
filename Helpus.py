import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# Определяем путь к .env файлу
ENV_PATH = os.getenv('DOTENV_PATH', '.env_helpus')  # По умолчанию ищем .env_helpus в текущей папке

# Загружаем переменные окружения из указанного .env файла
if os.path.exists(ENV_PATH):
    load_dotenv(dotenv_path=ENV_PATH)
    logging.info(f"Загружен .env файл: {ENV_PATH}")
else:
    # Пробуем загрузить из текущей директории
    load_dotenv()
    logging.info("Загружен .env файл из текущей директории")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Чтение токена из .env файла
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN_HELPUS')

if not TOKEN:
    logger.error(f"❌ Токен бота не найден! Проверьте файл: {ENV_PATH}")
    logger.error(f"Текущая директория: {os.getcwd()}")
    logger.error(f"Содержимое директории: {os.listdir('.')}")
    raise ValueError(f"❌ Токен бота не найден! Проверьте TELEGRAM_BOT_TOKEN_HELPUS в файле: {ENV_PATH}")

ABOUT_TEXT = """Анимешники России — общественно-политическое движение, собравшее вокруг себя всех поклонников японской культуры. С 1905 года мы защищаем гордость и честь отечественных отаку."""

PROGRAM_TEXT = """*Наша программа*

*Мир, Труд, Кавай!*
Создание комфортной среды для каждого отаку.

*Свобода самовыражения*
Защита права на ношение косплея.

*Традиции и Будущее*
Поддержка молодых художников.

*Импортозамещение вайфу*
Гранты на отечественные новеллы.

*Цифровой суверенитет*
Платформа для тайтлов без цензуры.

*Доступная атрибутика*
Снижение налогов на фигурки.

*2D-инфраструктура*
Курсы японского в каждом городе.

*Вечный онгоинг*
Пропаганда дружбы через аниме.

*Первая аниме-империя*
Россия восстанавливает монархию.

*Месть за Цусиму*
Установление русско-японской унии.

*Новое образование*
Роспуск Минпросвещения.

*Переход в 2D*
Интернет — новый субъект Федерации.

*Новые лица в политике*
Активисты возглавят Правительство.

*Манга в библиотеках*
Классика в школьных библиотеках.

*Ня-документы*
Полный электронный документооборот.

*Манга-терапия*
Включение манги в ОМС.

*День Хокаге*
Выплата 10.000р всем Хокаге.

*Лудомания во благо*
Казино национализируются.

*Отмена униформы*
Служащие в аниме-атрибутике.

*Аниме-юстиция*
Опричнина 21-го века."""

FULL_PROGRAM_TEXT = """*Наша программа*

*Мир, Труд, Кавай!*
Создание комфортной среды для каждого отаку и развитие сообществ.

*Свобода самовыражения*
Защита права на ношение косплея в общественных местах.

*Традиции и Будущее*
Поддержка молодых художников и аниматоров.

*Импортозамещение вайфу*
Гранты на отечественные визуальные новеллы.

*Цифровой суверенитет*
Платформа для просмотра тайтлов без цензуры.

*Доступная атрибутика*
Снижение налогов на импорт мерча и фигурок.

*Защита тайтлов*
Отмена интеллектуальной собственности.

*2D-инфраструктура*
Курсы японского и манги в каждом городе.

*Вечный онгоинг*
Пропаганда дружбы и саморазвития через аниме.

*Первая аниме-империя*
Россия восстанавливает монархию.

*Свадьба на Ходынском поле*
Русский царевич женится на японской принцессе.

*Месть за Цусиму*
Установление русско-японской унии.

*Новое русское образование*
Роспуск Минпросвещения. Бюджет на образование будет перераспределён.

*Национальное нейробудущее*
ИИ-корпорации должны стать государствообразующими. Россия принимает курс на покупку OpenAI.

*Переход в 2D*
Всемирная паутина возвращается в родную гавань. Сеть Интернет — новый субъект Федерации.

*Новые лица в политике*
Анкорд, Хацунэ Мику и другие активисты Анимешников России возглавят Правительство.

*Манга в библиотеках*
Обязательное наличие классики (Берсерк, Евангелион) в школьных библиотеках.

*Ня-документы*
Полный переход на электронный документооборот.

*Манга-терапия*
Включение чтения расслабляющей манги в программу ОМС.

*Архив шедевров*
Оцифровка и вечное хранение редких кассетных записей аниме 80-х годов.

*День Хокаге*
Выплата 10.000р всем Хокаге. Подтвердить статус можно через ня-услуги.

*Введение NAP*
Агрессия физическая заменяется на культурную, социальную и экономическую.

*Лудомания во благо*
Казино и букмекерские контуры национализируются.

*Традиционные семейные ценности*
Полигиничный брак становится нормой. Происходит институционализация гейш.

*Школьники тоже люди*
12 лет — возраст приобретения полной гражданской дееспособности.

*Отмена униформы*
В МВД вас будут встречать в аниме-парике, в суде — в розковой юбке, а в МФЦ — в налобной повязке Наруто.

*Аниме-юстиция*
Опричнина 21-го века. Действует до полного перехода России в 2D."""

CONTACTS_TEXT = """Вы можете написать нам на почту anime.rossii@yandex.ru либо написать в личные сообщения телеграмм группы"""

REGIONS = {
    "Москва": {
        "telegram": "t.me/animepartiyaMSK",
        "vk": "vk.ru/animepartiyamsk"
    },
    "Санкт-Петербург": {
        "telegram": "t.me/animepartiyaSPB",
        "vk": "vk.ru/animepartiyaspb"
    },
    "Вологда": {
        "telegram": "t.me/animepartiyaVLG",
        "vk": "vk.com/animepartiyaVLG"
    },
    "Воронеж": {
        "telegram": "t.me/animepartiyaVRN",
        "vk": "vk.ru/animepartiyaVRN"
    },
    "Томск": {
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
        [create_button("О нас", callback_data="about")],
        [create_button("Партийные отделения", callback_data="regions")],
        [create_button("Наши контакты", callback_data="contacts")],
        [create_button("Вступить к нам", callback_data="join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo=MAIN_PHOTO_URL,
        caption="Добро пожаловать в Анимешники России! Выберите опцию:",
        reply_markup=reply_markup
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "main_menu":
        keyboard = [
            [create_button("О нас", callback_data="about")],
            [create_button("Партийные отделения", callback_data="regions")],
            [create_button("Наши контакты", callback_data="contacts")],
            [create_button("Вступить к нам", callback_data="join")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_media(
            InputMediaPhoto(media=MAIN_PHOTO_URL, caption="Добро пожаловать в Анимешники России! Выберите опцию:"),
            reply_markup=reply_markup
        )

    elif data == "about":
        keyboard = [
            [create_button("Наш сайт", url="https://анимепартия.рф")],
            [create_button("Наш телеграм", url="https://t.me/animepartiya")],
            [create_button("Наша программа", callback_data="program")],
            [create_button("Назад", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_caption(
            caption=ABOUT_TEXT,
            reply_markup=reply_markup
        )

    elif data == "program":
        keyboard = [
            [create_button("Полная программа", callback_data="full_program")],
            [create_button("Назад", callback_data="about")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if query.message.photo:
            await query.edit_message_caption(
                caption=PROGRAM_TEXT,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
        else:
            await query.message.delete()
            await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=MAIN_PHOTO_URL,
                caption=PROGRAM_TEXT,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )

    elif data == "full_program":
        keyboard = [
            [create_button("Назад к программе", callback_data="program")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=FULL_PROGRAM_TEXT,
            parse_mode='Markdown',
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

    elif data == "regions":
        keyboard = []
        for region in REGIONS.keys():
            keyboard.append([create_button(region, callback_data=f"region_{region}")])
        keyboard.append([create_button("Назад", callback_data="main_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_caption(
            caption="Выберите город:",
            reply_markup=reply_markup
        )

    elif data.startswith("region_"):
        region_name = data.replace("region_", "")
        region_data = REGIONS.get(region_name)

        keyboard = [
            [create_button("Telegram", url=region_data["telegram"])],
            [create_button("VK", url=region_data["vk"])],
            [create_button("Назад", callback_data="regions")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_caption(
            caption=f"*{region_name}*\n\nСсылки на наши соцсети:",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

    elif data == "contacts":
        keyboard = [
            [create_button("Telegram группа", url="https://t.me/animepartiya")],
            [create_button("Назад", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_caption(
            caption=CONTACTS_TEXT,
            reply_markup=reply_markup
        )

    elif data == "join":
        keyboard = [
            [create_button("Заполнить анкету", url=JOIN_LINK)],
            [create_button("Назад", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_caption(
            caption="Для вступления в наши ряды заполните анкету по ссылке ниже:",
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

