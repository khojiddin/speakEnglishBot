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


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm English to English Translator Bot.\nWhat can I do?\n"
                        "I can:"
                        "\n✔ translate words or sentences from any language to English.\n"
                        "✔ English to English definitions with audio.\n"
                        "✔ Uzbek: sentences or words to English")


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
    executor.start_polling(dp, skip_updates=True)