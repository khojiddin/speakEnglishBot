import logging, os
from aiogram import Bot, Dispatcher, executor, types
from EnglishToEnglish import getWordDefinition
from googletrans import Translator


translator = Translator()

BOT_API_TOKEN = os.getenv('Bot_Api')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_API_TOKEN)
dp = Dispatcher(bot)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{BOT_API_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT', default=8000))


async def on_startup(dp):
    logging.warning(
        'Starting connection. ')
    await bot.set_webhook(WEBHOOK_URL,drop_pending_updates=True)


async def on_shutdown(dp):
    logging.warning('Bye! Shutting down webhook connection')


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm English to English Translator Bot.\nWhat can I do?\n"
                        "I can:"
                        "\nā translate words or sentences from any language to English.\n"
                        "ā English to English definitions with audio.\n"
                        "ā Uzbek: sentences or words to English")


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply('Please contact at:\n https://t.me/MisterMarvel')


@dp.message_handler()
async def translate(message: types.Message):
    try:
        lang = translator.detect(message.text).lang
        if len(message.text.split()) > 2:
            toLang = 'uz' if lang == 'en' else 'en'
            text = translator.translate(message.text, toLang).text
            if text == message.text:
                await message.reply("Please input correct data!")
            else:
                await message.reply(f'From {lang}:\n{text}')
        else:
            word = getWordDefinition(message.text)
            data2 = translator.translate(message.text, dest='en').text

            if word and lang == "en":
                await message.reply(f'Word: {message.text}\n'
                                    f'Definitions:\n {word["definitions"]}')
                if word.get('audio'):
                    await message.reply_voice(word['audio'])

            elif data2 and data2 != message.text:
                await message.reply(f'From {lang}:\n{data2}')

            else:
                await message.reply('No such Word found!')
    except:
        await message.reply("Something went wrong or we cannot translate from this language, please Try again")

if __name__ == '__main__':
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,)
