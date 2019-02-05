from flask import Flask, render_template, request
from pymongo import MongoClient,DESCENDING
from bson.objectid import ObjectId
import re
from mongo_schema import TextDocument
from settings import *

app = Flask(__name__)
client = MongoClient('mongodb://{}:{}'.format(MONGO_HOST_NAME, MONGO_HOST_PORT))
db = client.lootnotes


def regex_mongo(text):
    return re.compile('.*' + text + '.*', re.IGNORECASE)


@app.route('/')
def home():
    documents = db.text_document.find({}).sort("_id",DESCENDING).limit(10) # get last 10 rows
    return render_template('search.html',documents=documents)


@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        tag_list = ["tag", "title", "message"]
        for item in tag_list:
            if len(request.form[item]) < 3:
                print("Zorunlu alan ")
                break
            else:
                TextDocument(link=request.form['link'],
                             tag=request.form['tag'],
                             message=request.form['message'],
                             title=request.form['title']).save()
                return render_template("search.html")

    return render_template('add_new_note.html')


@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    user_information = db.text_document.find({"tag": regex_mongo(search_term)})

    return render_template('results.html', user_information=user_information)


@app.route('/show_text/<document_id>', methods=['GET', 'POST'])
def get_text(document_id):
    document_information = db.text_document.find({'_id': ObjectId(document_id)})
    return render_template("show_text.html", document_information=document_information)


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0', port=5000)
    app.debug = True
