#!/usr/bin/env python
# pylint: disable=C0116,W0613


import logging
import requests
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

URL = "https://api.openweathermap.org/data/2.5/weather/"
APPID = "f0073aec073f44b014cd174b032cfcda"


def get_weather_url(params):
    """
    Get weather data from OpenWeather
    """
    params["appid"] = APPID
    return requests.get(URL, params=params).json()
# Define a few command handlers. These usually take the two arguments update and
# context.


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        f'URL tashla'
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')
    update


def today_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""

    city = "tashkent"
    if update.message.text != "/today":
        message_splited = update.message.text.split(' ')
        city = " ".join(message_splited[1::])

    response = get_weather_url({'q': city})
    if response.get('weather', None) != None:
        update.message.reply_text(
            f'Today weather in {response["name"]}:\n\n{response["weather"][0]["main"].capitalize()}\n{response["weather"][0]["description"].capitalize()}')
    else:
        update.message.reply_text(
            'City not found.')


def url(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    import requests
    from bs4 import BeautifulSoup
    URL = "https://kun.uz/news/2022/07/12/tolibon-delegatsiyasi-toshkentdagi-xalqaro-konferensiyada-ishtirok-etadi"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    # print(soup)
    # print(dir(soup))
    title = str(soup.find_all("div", class_="single-header__title")[0].text)
    # print(title.text)
    content = str(soup.find_all("div", class_="single-content")[0].text)
    # print(content.text)
    image = soup.find_all("div", class_="main-img")[0].find_all("img")[0]
    print(image)
    update.message.reply_photo(image['src'],f"{title}\n\n{content[:200]}")


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5406902621:AAHypEBrTHm5Ufj8pNGiNWxRFi1LS28pBFQ")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, url))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
