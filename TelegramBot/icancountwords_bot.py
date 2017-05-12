import flask
import telebot
import conf
# import string
import re

# regex = re.compile('[%s][^\-]' % re.escape(string.punctuation))
# # regex = re.compile(r"(\b[-']\b)|[\W_]\-")
# regex = re.compile(r"[^a-zA-Z0-9-]+")

WEBHOOK_URL_BASE = "https://{}".format(conf.WEBHOOK_HOST)
WEBHOOK_URL_PATH = "/{}".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=(WEBHOOK_URL_BASE+WEBHOOK_URL_PATH))

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Здравствуйте! Этот бот считает количество слов в вашем сообщении.')

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, 'Просто отправьте боту сообщение, длину которого вы хотите посчитать.')

@bot.message_handler(func=lambda m: True)
def send_len(message):
    allwords = message.text.replace(' - ', ' ').replace(' \u2013 ', ' ').replace(' \u2014 ', ' ')
    cl_words = re.sub(r'[.,!?;:–«»"@#&$]+\ *', ' ', allwords)
    words = cl_words.split()
    wordCount = len(words)

    mod10 = wordCount % 10
    mod100 = wordCount % 100

    form = 'слов'

    if 10 < mod100 < 20:
        pass
    elif mod10 == 1:
        form = 'слово'
    elif 1 < mod10 < 5:
        form = 'слова'

    bot.send_message(message.chat.id, 'В вашем сообщении {} {}.'.format(wordCount, form))
