import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from tweets_classifier import predict_tweets
from retrieve_tweets import get_tweets_trend, get_tweets_user


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Base functions for the bot
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Write "@username" or "#trend" to analize the tweets of a user or a trend. Write "/help" to see the commands.')

def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('This is a bot that will analizy the tweets of a user or a trend and will tell you if the tweets is happy or sad.')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


# Function to analize the tweets of a user or a trend
def trend(update,context):
    trend_name = update.message.text
    try:
        y = predict_tweets(get_tweets_trend(trend_name))
        print(y)
        average = sum(y) / len(y)
        if average > 0.5:
            update.message.reply_text("The tweets of this trend are happy for " + str(round(average*100,2)) + "%")
        else:
            if average == 0.5:
                update.message.reply_text("The tweets of this trend are neutral")
            else:
                update.message.reply_text("The tweets of this trend are sad for " + str(round(100-average*100,2)) + "%")
    except:
        update.message.reply_text("Trend not found")

def user(update,context):
    user_name = update.message.text[1:]
    try:
        y = predict_tweets(get_tweets_user(user_name))
        average = sum(y) / len(y)
        if average > 0.5:
            update.message.reply_text("The tweets of user are happy for " + str(round(average*100,2)) + "%")
        else:
            if average == 0.5:
                update.message.reply_text("The tweets of user are neutral")
            else:
                update.message.reply_text("The tweets of user are sad for " + str(round(100-average*100,2)) + "%")
    except:
        update.message.reply_text("User not found")

def incorrect_message(update, context):
    update.message.reply_text(
        "The message you typed is incorrect "
        + 'To try again, send "@" followed by a twitter username'
        + 'or "#" followed by a topic!'
    )

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    token = "5938896126:AAG8aKWFvZiLyS11QavUBZ6f2MlvDOiPwqY"
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # If the message is a trend or a user, analize the tweets
    # Else, send a error message to user
    dp.add_handler(MessageHandler(Filters.regex(r"^[@][\w]+"), user))
    dp.add_handler(MessageHandler(Filters.regex(r"^[#][\w]+"), trend))
    dp.add_handler(MessageHandler(Filters.text, incorrect_message))

    # Log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
    

