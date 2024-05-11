from lib.functions import * 
from web_scraping import web_scrapping_class as ws
from html_procesing import html_procesing_class as hp
from topic_modeling import topic_modeling_class as tm

from gensim.models import ldamodel
from pandas.core.frame import DataFrame

from flask import Flask
from flask import redirect
from flask import url_for
from flask import request 
from flask import jsonify
from url_predicting import url_predicting_class as up

app = Flask(__name__)

@app.before_request
def before():
    print("This is executed BEFORE each request.")      

@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"

@app.route('/<int:number>/')
def incrementer(number):
    return "Incremented number is " + str(number+1)

@app.route('/<string:name>/')
def hello(name):
    return "Hello " + name

@app.route('/person/')
def hello1():
    return jsonify({'name':'Jimit','address':'India'}), 418

#Para formulario
@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name
 
@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

@app.route('/predecir/<path:url_pred>')
def opcion_menu(url_pred): 
    
    dominio= '-'            
    url = up(url_pred,dominio)              
    url.predecir()    
    
    df = pd.read_csv('data\\dataframes\\url_predict.csv')
    #Document_No = str(df.loc[0,"Document_No"])
    v_dominant_Topic = str(df.loc[0,"Dominant_Topic"])
    v_topic_Perc_Contrib = str(df.loc[0,"Topic_Perc_Contrib"])
    v_keywords = str(df.loc[0,"Keywords"])
    v_text = str(df.loc[0,"Text"])

    keywords_dataframe = pd.read_csv('data\\dataframes\\keywords.txt')
    if 'receta' in v_keywords: 
        v_topico='Cocina'
    if 'master' in v_keywords: 
        v_topico='Educacion'
    if 'traduccion' in v_keywords: 
        v_topico='Traduccion'
    if 'cuenta'in v_keywords:
        v_topico='Bancos'
    if 'cirugia'in v_keywords:
        v_topico='Salud'
    
    return jsonify({'Dominant_Topic':v_topico,'Perc_Contribution':v_topic_Perc_Contrib,'Topic_Keywords':v_keywords}), 418
    #return jsonify({'Dominant_Topic':v_dominant_Topic,'Perc_Contribution':v_topic_Perc_Contrib,'Topic_Keywords':v_keywords,'Texts':v_text}), 418     
    
        


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)