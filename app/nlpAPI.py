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

@app.route('/process',methods=["POST"])
def process():
	if request.method == 'POST':
		#choice = request.form['taskoption']
		rawtext = request.form['rawtext']
		doc = nlp(rawtext)
		mkd_text = displacy.render(doc,style='ent')
		value = Markup(mkd_text)

		d = []
		for ent in doc.ents:
			d.append((ent.label_, ent.text))
			df = pd.DataFrame(d, columns=('named entity', 'output'))
			ORG_named_entity = df.loc[df['named entity'] == 'ORG']['output']
			PERSON_named_entity = df.loc[df['named entity'] == 'PERSON']['output']
			GPE_named_entity = df.loc[df['named entity'] == 'GPE']['output']
			MONEY_named_entity = df.loc[df['named entity'] == 'MONEY']['output']
			
			results_ORG = ORG_named_entity
			num_of_results_ORG = len(results_ORG)
			results_PERSON = PERSON_named_entity
			num_of_results_PERSON = len(results_PERSON)
			results_GPE = GPE_named_entity
			num_of_results_GPE = len(results_GPE)
			results_MONEY = MONEY_named_entity
			num_of_results_MONEY = len(results_MONEY)
            
			num_of_results = num_of_results_ORG + num_of_results_PERSON + num_of_results_GPE + num_of_results_MONEY
	
	return render_template("index.html",mkd_text=value, results_ORG=results_ORG,results_PERSON=results_PERSON,results_GPE=results_GPE, results_MONEY=results_MONEY, num_of_results = num_of_results)

@app.route('/ner')
def api_articles():
    return 'List of ' + url_for('api_articles')

@app.route('/ner/<rawtext>')
def getNER(rawtext):
    doc = nlp(rawtext)
    d = []
    for ent in doc.ents:
        d.append((ent.label_, ent.text))
        df = pd.DataFrame(d, columns=('named entity', 'output'))
        GPE_named_entity = df.loc[df['named entity'] == 'GPE']['output']

    return GPE_named_entity.to_json(orient='split')

if __name__ == '__main__':
    app.run(debug=True)
