# Importamos las funciones
from lib.functions import * 

class html_procesing_class:
  # Atributos
  url = None
  dominio = None 
  archivo_a_procesar = None 
  directorio_raw= None
  directorio_processed= None
  contenido= None

  # Definimos un constructor inicial
  def __init__(self, archivo_a_procesar = None, url = None, dominio = None, ):  
    self.url= url  
    self.dominio= dominio  
    self.archivo_a_procesar= archivo_a_procesar
    self.directorio_raw='data\\raw\\'
    self.directorio_processed='data\\processed\\'
    self.contenido='Sin contenido'
    
  # Definimos método principal 
  def procesar(self):
    # Cargamos y leemos el archivo   
    archivo_ruta_carga = self.directorio_raw+self.archivo_a_procesar
    contenido=load_txt(archivo_ruta_carga)

    # Convertir en minusculas
    lowercase_result = lower_case_convertion(contenido)
    contenido = lowercase_result

    # Remover urls
    urls_result = remove_urls(contenido)
    contenido = urls_result

    # Convertir numeros a letras. Sustituye por clase digit
    numbers_result = num_to_words(contenido)
    contenido = numbers_result
    
    # Quitar acentos
    accented_result = accented_to_ascii(contenido)
    contenido = accented_result

    # Eliminar espacios
    space_result = remove_extra_spaces(contenido)
    contenido = space_result

    # Remover puntuaciones
    punct_result = remove_punctuation(contenido)
    contenido = punct_result
    #input(contenido)

    # Remover caracteres individuales
    sc_result = remove_single_char(contenido)
    contenido = sc_result
    #input(contenido)

    #GX Eliminar stopwords lo volvia  poner aqui para elinimar la plabra "el"
    text_aux = remove_stopwords(contenido)
    contenido = text_aux
    #input(contenido)

    # Pipeline Español
    nlp = spacy.load('es_core_news_sm')    

    # Lemmatization
    doc_lemma = nlp(contenido)
    lemma_aux = ""
    for token in doc_lemma:  
      lemma_aux = lemma_aux +"  "+token.lemma_
      contenido = lemma_aux +"  "+token.lemma_  
      #print(token," - ", token.lemma_) 

    # PoS
    doc_pos = nlp(contenido)
    pos_aux=""
    for token in doc_pos:
      if token.pos_ == "NOUN":
        pos_aux = pos_aux+" "+str(token)
        #print(token, token.pos_)
        contenido=pos_aux
    
    #input(contenido)
      
    # Lista de verbos
    # print("Verbos:", [token for token in doc_pos if token.pos_ == "VERB"])
    # Obs: Verificar porque algunos no son verbos  

    
    # Guardamos archivo procesado .txt   
    archivo_ruta_descarga = self.directorio_processed+self.archivo_a_procesar
    download_txt(archivo_ruta_descarga,contenido)

    #Pintamos nube de palabras
    #pintar_wordcloud(contenido)

    # Guardamos el archivo en dataframe csv independiente    
    #create_individual_dataframe(self.url, self.dominio, contenido,self.archivo_a_procesar)      

    self.contenido=contenido

#Aqui tambien se puede llamar a funciones de bigramas, trigramas etc para ampliar analisis visual exploratorio