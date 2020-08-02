from flask import Flask, render_template, url_for, request
import re
import json
import pandas as pd
import spacy
from spacy import displacy
import en_core_web_sm
from flask import Markup

#next are for keyword
from collections import Counter
from string import punctuation

nlp_en = spacy.load('en_core_web_sm')
nlp_fr = spacy.load('fr_core_news_sm')

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

#this is the web interface to demonstrate the NER extraction
@app.route('/process',methods=["POST"])
def process():
    mkd_text_coded=''
    
    if request.method == 'POST':
        text = request.form['rawtext']
        lang = request.form['language']
        action = request.form['action']

        if lang == "english":
            doc = nlp_en(text)
        elif lang == "french":
            doc = nlp_fr(text)

        if action == "ner":
            mkd_text = displacy.render(doc,style='ent')
            mkd_text_coded = Markup(mkd_text)
        elif action == "keyword":
            #keywords = set(extract_keywords(text))#no duplicates
            keywords_all = extract_keywords(text)
            keywords = Counter(keywords_all).most_common(5)
            mkd_text_coded = Markup(keywords)

    return render_template("index.html", mkd_text=mkd_text_coded)

def extract_keywords(text):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN']
    doc = nlp_en(text.lower())
    for token in doc:
        if(token.text in nlp_en.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            result.append(token.text)
    return result
    
#this the API call
@app.route('/api/v1.0/ner', methods=['GET'])
def getNER():
    lang = request.args.get('lang')
    text = request.args.get('text')

    my_dict = {}
    
    if lang == "en":
        doc = nlp_en(text)
    elif lang == "fr":
        doc = nlp_fr(text)
    else:
        my_dict['status'] = "language not supported"
        return json.dumps(my_dict)

    d = []
    counter = 0
    for ent in doc.ents:
        my_dict[counter] = [ent.label_, ent.text]
        counter += 1
    
    my_dict['status'] = len(my_dict)
    return json.dumps(my_dict)

if __name__ == '__main__':
    app.run(debug=True)
