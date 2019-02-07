from flask import Flask, render_template, request ,flash
from pymongo import MongoClient
import re
from mongo_schema import TextDocument
from settings import *
from text_extractor import *

app = Flask(__name__)

client = MongoClient('mongodb://{}:{}'.format(MONGO_HOST_NAME, MONGO_HOST_PORT))
db = client.lootnotes


def regex_mongo(text):
    return re.compile('.*' + text + '.*', re.IGNORECASE)


@app.route('/')
def home():
    return render_template('search.html')


@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'Save' in request.form:
        TextDocument(link=request.form['link'],
                     tag=request.form['tag'],
                     message=request.form['message'],
                     title=request.form['title']).save()

    if 'Extract' in request.form:
        lang = language_controller(request.form['link'])
        text = TextParser(request.form['link'], lang=lang).parse_text()
        title = TextParser(request.form['link'], lang=lang).parse_title()
        url = TextParser(request.form['link'], lang=lang).parse_url()
        return render_template("add_new_note.html", text=text, title=title, url=url)

    return render_template('add_new_note.html', text="", title="", url="")


@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    user_information = db.text_document.find({"tag": regex_mongo(search_term)})

    return render_template('results.html', user_information=user_information)


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0', port=5000)
    app.debug = True