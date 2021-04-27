from flask import Blueprint, Flask, g, jsonify, render_template, request, Response, redirect, url_for, send_from_directory
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
import os
import datetime
import webbrowser
import json
import requests
from flask_json import FlaskJSON, JsonError, json_response, as_json
from deep_translator import GoogleTranslator
import lda as topic_model

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get("query")
        lang = request.form.get("lang")

        if lang == "text_es":
            #translate detected query to target language
            query = GoogleTranslator(source='auto', target='es').translate(query)
            url = 'http://127.0.0.1:8990/solr/clir/select?q=(text_es:(' + query + ') OR title_es:(' + query + '))'
            r = requests.get(url)
            results = r.json()['response']['docs']
            final = list()
            for doc in results:
                add = [str(doc['title_es']), str(doc['text_es'])]
                final.append(tuple(add))
            # topic modeling on results
            # update new expanded query
            new_query = query

            try:
                new_query = new_query + topic_model.get_topics(final)
            except ValueError:
                pass
            url_new = 'http://127.0.0.1:8990/solr/clir/select?q=(text_es:(' + new_query + ') OR title_es:(' + new_query + '))'
            r_new = requests.get(url_new)
            results_new = r_new.json()['response']['docs']
            final_results = list()
            for doc in results_new:
                add = [str(doc['title_es']), str(doc['text_es'])]
                final_results.append(tuple(add))

            return render_template("resultos.html", name = final_results, q = new_query)

        if lang == "text_en":
            query = GoogleTranslator(source='auto', target='en').translate(query)
            url = 'http://127.0.0.1:8990/solr/clir/select?q=(text_en:(' + query + ') OR title_en:(' + query + '))'
            r = requests.get(url)
            results = r.json()['response']['docs']
            final = list()
            for doc in results:
                add = [str(doc['title_en']), str(doc['text_en'])]
                final.append(tuple(add))
            #get topic model terms with scores & update new expanded query
            new_query = query
            try:
                new_query = new_query + topic_model.get_topics(final)
            except ValueError:
                pass
            url_new = 'http://127.0.0.1:8990/solr/clir/select?q=(text_en:(' + new_query + ') OR title_en:(' + new_query + '))'
            r_new = requests.get(url_new)
            results_new = r_new.json()['response']['docs']
            final_results = list()
            for doc in results_new:
                add = [str(doc['title_en']), str(doc['text_en'])]
                final_results.append(tuple(add))

            return render_template("results.html", name = final_results, q = new_query)

        if lang == "default":
            query = GoogleTranslator(source='auto', target='en').translate(query)
            url = 'http://127.0.0.1:8990/solr/clir/select?q=(text_en:(' + query + ') OR title_en:(' + query + '))'
            r = requests.get(url)
            results = r.json()['response']['docs']
            final = list()
            for doc in results:
                add = [str(doc['title_en']), str(doc['text_en'])]
                final.append(tuple(add))
            #get topic model terms with scores & update new expanded query
            new_query = query
            try:
                new_query = new_query + topic_model.get_topics(final)
            except ValueError:
                pass
            url_new = 'http://127.0.0.1:8990/solr/clir/select?q=(text_en:(' + new_query + ') OR title_en:(' + new_query + '))'
            r_new = requests.get(url_new)
            results_new = r_new.json()['response']['docs']
            final_results = list()
            for doc in results_new:
                add = [str(doc['title_en']), str(doc['text_en'])]
                final_results.append(tuple(add))

            return render_template("results.html", name = final_results, q = new_query)

    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)
