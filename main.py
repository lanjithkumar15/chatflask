from flask import Flask, request, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import pytz
from datetime import datetime, date
from fp.fp import FreeProxy
import nltk

proxy = FreeProxy().get()
nltk.set_proxy(proxy)
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')


app = Flask(__name__)
bot = ChatBot(
    'chatbot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand. I am still learning.',
            'maximum_similarity_threshold': 0.90
        }
    ],
    database_uri='sqlite:///database.sqlite3'
)

data = "save.txt"
file = open(data, "r")
training = file.readlines()
trainer = ListTrainer(bot)
trainer.train(training)
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english")

def generate_response(user_input):
    greeting_keywords = ['hello', 'hi', 'hey', 'greetings', 'howdy']
    gratitude_keywords = ['thanks', 'thank you', 'appreciate it', 'thankful']
    exit_keywords = ['exit', 'bye', 'quit', 'goodbye']
    creator_keywords = ['who created you', 'who made you', 'who designed you']
    time_keywords = ['time', 'what time is it', 'what is the time', 'current time']
    date_keywords = ['date', 'what is the date', 'today date']
    if any(keyword in user_input.lower() for keyword in greeting_keywords):
        return 'Hello!'
    elif any(keyword in user_input.lower() for keyword in gratitude_keywords):
        return 'You\'re welcome!'
    elif any(keyword in user_input.lower() for keyword in exit_keywords):
        return 'Goodbye!'
    elif any(keyword in user_input.lower() for keyword in creator_keywords):
        return 'I was created by the ChatterBot team.'
    elif any(keyword in user_input.lower() for keyword in time_keywords):
        IST = pytz.timezone('Asia/Kolkata')
        ist = datetime.now(IST)
        return 'The current time is ' + ist.strftime('%H:%M:%S') + ' in India.'
    elif any(keyword in user_input.lower() for keyword in date_keywords):
        return 'Today\'s date is ' + str(date.today()) + '.'
    else:
        return str(bot.get_response(user_input))

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/get")
def response():
    user_input = request.args.get('msg')
    return generate_response(user_input)

if __name__ == '__main__':
    app.run()
