from flask import Flask, render_template, request ,redirect ,url_for
from pymongo import MongoClient, DESCENDING
from bson.json_util import ObjectId
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
    documents = db.text_document.find({}).sort("_id", DESCENDING).limit(GET_LAST_N_RECORD)
    return render_template('search.html', documents=documents)


@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'Save' in request.form:
        if len(request.form['message']) > 3:
            TextDocument(link=request.form['link'],
                         tag=request.form['tag'],
                         message=request.form['message'],
                         title=request.form['title']).save()

            return redirect(url_for("home"))

    if 'Close' in request.form:
        return redirect(url_for("home"))

    if 'Extract' in request.form:
        if ("http" or "https") in request.form['link']:
            lang = language_controller(request.form['link'])
            text = TextParser(request.form['link'], lang=lang).parse_text()
            title = TextParser(request.form['link'], lang=lang).parse_title()
            url = TextParser(request.form['link'], lang=lang).parse_url()
            return render_template("add_new_note.html", text=text, title=title, url=url)

    return render_template('add_new_note.html')


@app.route('/show_text/<document_id>', methods=['GET', 'POST'])
def get_text(document_id):
    document = db.text_document.find({'_id': ObjectId(document_id)})
    return render_template("show_text.html", document=document)


@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    user_information = db.text_document.find({"tag": regex_mongo(search_term)})

    return render_template('results.html', user_information=user_information)


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0', port=5000)
    app.debug = True
