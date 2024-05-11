# Importamos las librerias
import re
import io
import os
from os import path
from os import remove
import csv
import math
import requests
import numpy as np
import pandas as pd
import sklearn
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from PIL import Image
from platform import python_version
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from sklearn.feature_extraction.text import CountVectorizer
import urllib3
# Desactivamos advertencias de certificado ssl
urllib3.disable_warnings()
import spacy
import gensim
from gensim.utils import simple_preprocess
from gensim.test.utils import datapath
import gensim.corpora as corpora
from gensim.models import CoherenceModel
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
from IPython.core.display import HTML
import pickle 
from pprint import pprint
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    import imp

# Definimos todas las funciones
def request(url):	
  try:
    page = requests.get(url, verify=False)
    return page
  except requests.exceptions.ConnectionError:
    requests.status_code = "Connection refused"  

def download_txt(directorio,page_text):	
  base_dir=directorio+'.txt'    
  text_file = io.open(base_dir, "w",encoding='UTF8')
  n = text_file.write(page_text)
  text_file.close()

def load_txt(archivo_ruta):	
  archivo = open(archivo_ruta+'.txt',encoding='utf8')
  contenido = archivo.read()
  archivo.close()
  return contenido

def download_csv(url,directorio,page_text):	
  base_dir=directorio+'.csv' 
  header = ['url', 'texto']
  data = [url, page_text]
  with io.open(base_dir, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    # write the data
    writer.writerow(data)

def create_individual_dataframe(url,dominio,contenido,nombre_archivo):	
  columns = ['URL', 'DOMINIO', 'CONTENIDO']
  data = [[url, dominio, contenido]]
  # Create the pandas DataFrame
  df = pd.DataFrame(data, columns = columns)
  ruta_dataframe = 'data\\dataframes\\'+nombre_archivo+'.csv'
  df.to_csv(ruta_dataframe, index=False)

def create_final_dataframe():	
  # Se define el directorio donde se buscará los dataframes individuales
  path = 'data\\dataframes\\'
  # Función para listar todos los archivos dentro de un directorio
  fileslist = os.listdir(path)
  # print(fileslist)

  # Se define un nuevo dataframe final
  dfinal = pd.DataFrame(columns=['URL', 'DOMINIO', 'CONTENIDO'])
  # Se recorre todos los dataframes individuales para poder concatenar en uno final.
  for file in fileslist:  
      path_i = path+file    
      df=pd.read_csv(path_i)        
      dfinal = pd.concat([dfinal, df], axis=0,ignore_index=True)    

  # Luego de concatenar guardamos en el directorio
  dfinal.to_csv('data\\dataframes\\final_dataframe.csv',index=False)
  

def lower_case_convertion(text):	
	lower_text = text.lower()
	return lower_text

def remove_html_tags(text):  
	html_pattern = r'<.*?>'
	without_html = re.sub(pattern=html_pattern, repl=' ', string=text)
	return without_html

from bs4 import BeautifulSoup
def remove_html_tags_beautifulsoup(text):	
	parser = BeautifulSoup(text, "html.parser")
	without_html = parser.get_text(separator = " ")
	return without_html

def remove_urls(text):  	
	url_pattern = r'https?://\S+|www\.\S+'
	without_urls = re.sub(pattern=url_pattern, repl=' ', string=text)
	return without_urls

def remove_numbers(text):	
	number_pattern = r'\d+'
	without_number = re.sub(pattern=number_pattern, repl=" ", string=text)
	return without_number

from num2words import num2words
def num_to_words(text):	
	# splitting text into words with space
	after_spliting = text.split()
	for index in range(len(after_spliting)):
		if after_spliting[index].isdigit():
			after_spliting[index] = 'digit'
      #after_spliting[index] = num2words(after_spliting[index], lang='es')
  # joining list into string with space
	numbers_to_words = ' '.join(after_spliting)
	return numbers_to_words

# spelling correction using spellchecker
def spell_autocorrect(text):  
  from autocorrect import Speller  
  from nltk.tokenize import sent_tokenize, word_tokenize
  import nltk
  nltk.download('punkt') 
  correct_spell_words = []
	# initialize Speller object for english language with 'en'
  spell_corrector = Speller(lang='es')
  for word in word_tokenize(text):
    # correct spell word
	  correct_word = spell_corrector(word)
	  correct_spell_words.append(correct_word)
  correct_spelling = ' '.join(correct_spell_words)
  return correct_spelling

import unidecode
def accented_to_ascii(text):
	# apply unidecode function on text to convert
	# accented characters to ASCII values  
  text = unidecode.unidecode(text)
  return text

# Implementation of Stemming using PorterStemming from nltk library
from nltk.stem import PorterStemmer
def porter_stemmer(text):
	# word tokenization
	tokens = word_tokenize(text)
	for index in range(len(tokens)):
		# stem word to each word
		stem_word = stemmer.stem(tokens[index])
		# update tokens list with stem word
		tokens[index] = stem_word
	# join list with space separator as string
	return ' '.join(tokens)

from nltk.stem import WordNetLemmatizer
def lemmatization(text):
	# word tokenization
  from nltk.tokenize import sent_tokenize, word_tokenize
  import nltk
  nltk.download('punkt') 
  nltk.download('wordnet') 
  tokens = word_tokenize(text)
  for index in range(len(tokens)):
    # lemma word
    lemma_word = lemma.lemmatize(tokens[index])
    tokens[index] = lemma_word
  return ' '.join(tokens)
 
# Implementation of emoji removing
def remove_emojis(text):	
	emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)

	without_emoji = emoji_pattern.sub(r'',text)
	return without_emoji

# Implementation of removing of emoticons
"""
from emoticons_list import EMOTICONS
def remove_emoticons(text):	
	emoticon_pattern = re.compile(u'(' + u'|'.join(k for k in EMOTICONS) + u')')
	without_emoticons = emoticon_pattern.sub(r'',text)
	return without_emoticons
"""

# Removing stopwords
def remove_stopwords(text):	
  try:
      import nltk
      from nltk.corpus import stopwords      
      nltk.download('stopwords', quiet=True) 
      from nltk.tokenize import word_tokenize      
      stop_words = stopwords.words('spanish') + stopwords.words('english')
      word_list = ['digit','cookies','cookie','kaspersky','nginx','endpoint','forbiddir',
                    'enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','setiembre','octubre','noviembre','diciembre',
                    'lunes','martes','miercoles','jueves','viernes','sabado','domingo']
      stop_words.extend(word_list)
  except:
      import nltk
      from nltk.corpus import stopwords
      from nltk.tokenize import word_tokenize
      stop_words = stopwords.words('spanish') + stopwords.words('english')
      word_list = ['digit','cookies','cookie','kaspersky','nginx','endpoint','forbiddir',
                    'enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','setiembre','octubre','noviembre','diciembre',
                    'lunes','martes','miercoles','jueves','viernes','sabado','domingo']
      stop_words.extend(word_list)
      

  #text_tokens = word_tokenize(text)
  #text_aux =  [word for word in text_tokens if not word in stop_words]
  # GX puse al final len(word)>2 pare elininar palabras menores de 2 caracteres
  text_aux =  [word for word in text.split() if not word in stop_words and len(word)>4]
  text_aux_s = " ".join(text_aux)
  return text_aux_s

# Implementation of removing punctuations using string library
from string import punctuation
def remove_punctuation(text):
	return text.translate(str.maketrans('', '', punctuation))
 
## Remove single characters
def remove_single_char(text):	
	single_char_pattern = r'\s+[a-zA-Z]\s+'
	without_sc = re.sub(pattern=single_char_pattern, repl=" ", string=text)
	return without_sc



# Removing Extra Whitespaces
def remove_extra_spaces(text):	
	space_pattern = r'\s+'
	without_space = re.sub(pattern=space_pattern, repl=" ", string=text)
	return without_space


basedir = os.path.dirname(spacy.__path__[0])
if not os.path.isdir(os.path.join(basedir, 'es_core_news_sm')):
    from spacy.cli import download
    download('es_core_news_sm')


def pintar_wordcloud(contenido):
  # Create a WordCloud object
  wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')
  # Generate a word cloud
  wordcloud.generate(contenido)
  # Visualize the word cloud
  # wordcloud.to_image()
  plt.figure()
  plt.imshow(wordcloud, interpolation="bilinear")
  plt.axis("off")
  plt.show()

#Directorio de instalacion spacy
#print(basedir)

def sent_to_words(sentences):
  for sentence in sentences:
    # deacc=True removes punctuations
    yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))
