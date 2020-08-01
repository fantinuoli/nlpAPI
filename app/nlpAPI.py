from flask import Flask, render_template, url_for, request
import re
import pandas as pd
import spacy
from spacy import displacy
import en_core_web_sm
from flask import Markup

nlp = spacy.load('en_core_web_sm')

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

#this is the web interface to demonstrate the NER extraction
@app.route('/process',methods=["POST"])
def process():
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		doc = nlp(rawtext)
		mkd_text = displacy.render(doc,style='ent')
		mkd_text_coded = Markup(mkd_text)

	return render_template("index.html", mkd_text=mkd_text_coded)

#this needs to be deleted, it has no function 
@app.route('/ner')
def api_articles():
    return 'List of ' + url_for('api_articles')

#this the API call
#I need to modify it in order to extract ALL or a subset of NER
@app.route('/ner/<rawtext>')
def getNER(rawtext):
    doc = nlp(rawtext)
    d = []
    num_of_results_GPE = 0
    for ent in doc.ents:
        d.append((ent.label_, ent.text))
        df = pd.DataFrame(d, columns=('named entity', 'output'))
        GPE_named_entity = df.loc[df['named entity'] == 'GPE']['output']
        
        #to get number of NER
        results_GPE = GPE_named_entity
        num_of_results_GPE = len(results_GPE)
    
    if num_of_results_GPE > 0:
        return GPE_named_entity.to_json(orient='split')
    else:
        return "undef"#need to return a useful answer

if __name__ == '__main__':
    app.run(debug=True)
