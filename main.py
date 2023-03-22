from flask import Flask, request, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import pytz
from datetime import datetime, date

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
# to train your own txt file
#{with open('dialogs.txt', 'r') as k:
#    conv = k.read().splitlines()
    
#trainer = ListTrainer(bot)
#trainer.train(conv)}
trainer = ChatterBotCorpusTrainer(bot)
trainer.train('chatterbot.corpus.english')

responses = {
    'who created you?': 'chatterbot',
    'who designed you': 'chatterbot',
    'who made you': 'chatterbot',
    'exit': 'bye have a nice day',
    'bye': 'bye have a nice day',
    'quite': 'bye have a nice day',
    'Thanks for help': 'Thanks it is my pleasure to help you!',
    'Thank you': 'Thanks it is my pleasure to help you!',
    'Thank for your help': 'Thanks it is my pleasure to help you!',
    'you are great': 'Thanks it is my pleasure to help you!',
    'you are awsome': 'Thanks it is my pleasure to help you!',
    'time': datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%H:%M:%S'),
    'time now': datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%H:%M:%S'),
    'what is time now': datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%H:%M:%S'),
    'time?': datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%H:%M:%S'),
    'time now?': datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%H:%M:%S'),
    'date': str(date.today()),
    'today date': str(date.today()),
    'date?': str(date.today()),
    'todaydate': str(date.today())
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def response():
    string = request.args.get('msg')
    return responses.get(string, str(bot.get_response(string)))

if __name__ == '__main__':
    app.run(debug=True)
