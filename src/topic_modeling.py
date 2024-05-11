from numpy import ceil, integer
from lib.functions import *
from gensim.test.utils import datapath
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)    
    

class topic_modeling_class:

    
    directorio_raw= None
    directorio_processed= None   
    directorio_dataframes= None 
    directorio_keywords= None  
    cantidad_topics = None           


    def __init__(self, cantidad_topics = None, filename=None):           
        self.directorio_raw='data\\raw\\'
        self.directorio_processed='data\\processed\\'  
        self.directorio_keywords='data\\dataframes\\keywords' 
        self.directorio_dataframes=filename
        self.cantidad_topics = cantidad_topics

    
    def modelar(self):
        # Cargamos y leemos el archivo final          
        archivo_ruta_carga = self.directorio_dataframes
        
        #contenido=load_txt(archivo_ruta_carga)    
        final_dataframe = pd.read_csv(archivo_ruta_carga) 
         
        # Extraemos solo la columna contenido y asignamos a una variable array 
        contenido = final_dataframe.Contenido.values

        # Extraemos la columna url
        url = final_dataframe.URL.values

        # Dividimos el contenido dentro de una lista
        #data = list(contenido.split())
        data_words = list(sent_to_words(contenido))
        #print('Imprimir data words')
        
        # Creación del Diccionario
        id2word = corpora.Dictionary(data_words)
        # Creación del Corpus
        texts = data_words

        # Frecuencia de los términos
        corpus = [id2word.doc2bow(text) for text in texts]
        # View
        #print('Imprimir corpus')
        #input(corpus)

        # Numeros de topics
        numero_topics = self.cantidad_topics        

        # Modelo LDA con hiperparametros establecidos
        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=numero_topics, 
                                                #random_state=100,
                                                #update_every=1,
                                                #chunksize=100,
                                                passes=220,
                                                alpha='auto',
                                                per_word_topics=True
                                                )

        # Imprimir los Keyword en los topics
        print('Imprimir Keyword en los topics y sus pesos correspondientes')
        pprint(lda_model.print_topics(num_words=15))

        #Se guarda un archivo con todos los keywords relevantes
        resultado_final=''

        for i in range(numero_topics):            
            best_words = lda_model.print_topic(topicno=i, topn=15)
            Topic = '\n Topic '+str(i)+':'
            lista = re.findall(r'[a-z]+', best_words) 
            result = ', '.join(lista)            
            resultado_final = resultado_final+Topic+result       

        download_txt(self.directorio_keywords,resultado_final)     
        
        #doc_lda = lda_model[corpus]

        # Sistema de evaluación que tan bueno es el modelo
        # Compute Perplexity. # A measure of how good the model is. Lower is better.
        print('\nPerplejidad: ', lda_model.log_perplexity(corpus))  
        # Compute Coherence Score
        coherence_model_lda = CoherenceModel(model=lda_model, texts=data_words, dictionary=id2word, coherence='c_v')
        coherence_lda = coherence_model_lda.get_coherence()
        print('\nPuntuación de coherencia: ', coherence_lda)

        # Guardar el modelo
        # Guardar el modelo
        filename = 'models\\modelo1.sav'
        pickle.dump(lda_model, open(filename, 'wb'))  

        lda_model.save('models\\lda.model')   
        
        # Para imprimir los resultados    

        #  Visualize the topics       
        lda_vis = gensimvis.prepare(lda_model, corpus, id2word, sort_topics=True)
        #pyLDAvis.display(lda_vis)
        pyLDAvis.save_html(lda_vis, 'LDA_Visualization.html')
        
        