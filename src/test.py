# Importamos las funciones
from lib.functions import * 

# Cargamos y leemos el archivo   
archivo_ruta_carga = 'data\\raw\\alfa_sin_html'
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

# PoS
print('AQUI')
doc_pos = nlp(contenido)
pos_aux=""
for token in doc_pos:
    if token.pos_ == "NOUN":
        pos_aux = pos_aux+" "+str(token)
        print(token, token.pos_)
        contenido=pos_aux


print(contenido)

# Lista de verbos
# print("Verbos:", [token for token in doc_pos if token.pos_ == "VERB"])
# Obs: Verificar porque algunos no son verbos

# Lemmatization
doc_lemma = nlp(contenido)
lemma_aux = ""
for token in doc_lemma:  
    lemma_aux = lemma_aux +"  "+token.lemma_
    contenido = lemma_aux +"  "+token.lemma_  
    #print(token," - ", token.lemma_) 



#Aqui tambien se puede llamar a funciones de bigramas, trigramas etc para ampliar analisis visual exploratorio