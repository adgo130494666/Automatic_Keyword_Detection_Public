from gensim.models import ldamodel
from pandas.core.frame import DataFrame
from lib.functions import * 
from web_scraping import web_scrapping_class as ws
from html_procesing import html_procesing_class as hp
from topic_modeling import topic_modeling_class as tm
from sklearn.feature_extraction.text import CountVectorizer
import numpy

class url_predicting_class:

    # Atributos
    url = None 
    dominio =  None      

    # Definimos un constructor inicial
    def __init__(self, url = None, dominio= None):

        # Asignamos valor al atributo
        self.url= url
        self.dominio= dominio

    def predecir(self):

        #SCRAPPING
        pag_raw_pred = ws(self.url)
        pag_raw_pred.scrappear()   

        print('SCRAPPING')        

        #PROCESSING
        ruta_archivo_a_procesar_pred = pag_raw_pred.url_domain_sin_html
        pag_proc_pred = hp(ruta_archivo_a_procesar_pred,self.url,self.dominio)    
        pag_proc_pred.procesar() 

        #contenido=load_txt(archivo_ruta_carga)  
        ruta_archivo_a_predecir = 'data\\processed\\'+ruta_archivo_a_procesar_pred
        contenido_pred=load_txt(ruta_archivo_a_predecir)  #edu_sin_html

        # print(contenido_pred)     

        columns = ['Contenido']
        data = [contenido_pred]
        # Create the pandas DataFrame
        df_pred = pd.DataFrame(data, columns = columns)
                    
        # Extraemos solo la columna contenido y asignamos a una variable array 
        #data = list(contenido.split())
        contenido_pred_df = df_pred.Contenido.values

        #PREPARATION
        # Dividimos el contenido dentro de una lista                    
        data_words_pred = list(sent_to_words(contenido_pred_df))       
        # ('data words')             
        # print(data_words_pred)

        # Creación del Diccionario
        id2word_pred = corpora.Dictionary(data_words_pred) 

        # Creación del Corpus       
        texts_pred = data_words_pred
        # Frecuencia de los términos
        corpus_pred = [id2word_pred.doc2bow(text) for text in texts_pred]
        # print('corpus')  
        # input(corpus_pred)

        #Arimos el archivo del modelo preentrenado para compararlo con la url propuesta
        filename_pred = 'models\\modelo1.sav'
        loaded_model_pred = pickle.load(open(filename_pred, 'rb'))

        #loaded_model_pred =  gensim.models.ldamodel.LdaModel.load('models\\lda.model')

        print('PREDICCION')
        # Init output
        sent_topics_df = pd.DataFrame()

        # Get main topic in each document
        for i, row in enumerate(loaded_model_pred[corpus_pred]):
            row = sorted(row[i], key=lambda x:x[1], reverse=True)
            # Get the Dominant topic, Perc Contribution and Keywords for each document
            for j, (topic_num, prop_topic) in enumerate(row):
                if j == 0:  # => dominant topic
                    wp = loaded_model_pred.show_topic(topic_num,15)
                    topic_keywords = ", ".join([word for word, prop in wp])
                    sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
                else:
                    break

        sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

        # Add original text to the end of the output
        contents = pd.Series(texts_pred)
        sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)

        
        # Format
        df_dominant_topic = sent_topics_df.reset_index()
        df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']


        # Luego de concatenar guardamos en el directorio
        df_dominant_topic.to_csv('data\\dataframes\\url_predict.csv',index=False)             
        


 
