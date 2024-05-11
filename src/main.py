from gensim.models import ldamodel
from pandas.core.frame import DataFrame
from lib.functions import * 
from web_scraping import web_scrapping_class as ws
from html_procesing import html_procesing_class as hp
from topic_modeling import topic_modeling_class as tm
from url_predicting import url_predicting_class as up

if __name__ == '__main__':

    def menu():
        """
        Función que limpia la pantalla y muestra nuevamente el menu
        """
        os.system('cls') 
        print ("Selecciona una opción")
        print ("\t1 - SCRAPPING AND PROCESSING")
        print ("\t2 - MODELING")
        print ("\t3 - PREDICT")   

    while True:
        # Mostramos el menu
        menu()
    
        # solicituamos una opción al usuario
        opcionMenu = input("Inserta un numero >> ")        

        if opcionMenu=="1":
            
            input("Has pulsado la opción 1. Pulsa la tecla ENTER para continuar >> ")
            df = pd.read_csv('data\\dataframes\\Dominios.csv')             
            
            print('-----------------------EN PROCESO----------------------------')

            for i in range(len(df)):                
                url = str(df.loc[i,"URL"])
                dominio = str(df.loc[i,"Dominio"])                

                try:
                    #SCRAPPING
                    pag_raw = ws(url)
                    pag_raw.scrappear()    

                    #PROCESSING
                    ruta_archivo_a_procesar = pag_raw.url_domain_sin_html
                    pag_proc = hp(ruta_archivo_a_procesar,url,dominio)    
                    pag_proc.procesar() 

                    #ADDING CONTENT TO TABLE                   
                    df.loc[i,"Contenido"]=pag_proc.contenido 
                    #df.to_csv('data\\dataframes\\Dominios.csv',index=False)                          
                    df.to_csv('data\\dataframes\\final_dataframe.csv',index=False)   

                except Exception:
                    pass  # 'continue'

            print('-----------------------TERMINADO----------------------------')

            #Volvemos a leer el archivo
            df = pd.read_csv('data\\dataframes\\final_dataframe.csv')

            #Guardamos en un archivo las urls que no se pudo hacer correctamente scrapping
            bool_series = pd.isnull(df["Contenido"])
            dominios_null= df[bool_series]
            dominios_null.to_csv('data\\dataframes\\dominios_null.csv',index=False)  

            #Guardamos el dataframe sin valores nulos para alimentar al modelo
            df_final = df.loc[df.Contenido.notnull(), :]
            df_final.to_csv('data\\dataframes\\final_dataframe.csv',index=False) 

        elif opcionMenu=="2":
            input("Has pulsado la opción 2. Pulsa la tecla enter para continuar >> ")   

            print('-----------------------MODELING---------------------------------')
           
            fileName = 'data\\dataframes\\final_dataframe.csv'  
            cantidad_topics = int(input("Elige la cantidad de topics para el modelo, ej 6: "))
            pag_mod = tm(cantidad_topics,fileName)              
            pag_mod.modelar()
            
        elif opcionMenu=="3":
            
            input("Has pulsado la opción 3. Pulsa la tecla ENTER para continuar >> ")

            url= input('Escribe una URL: ')
            dominio= '-'
            
            url_pred = up(url,dominio)              
            url_pred.predecir()

            df = pd.read_csv('data\\dataframes\\url_predict.csv')

            print(df.to_string())
            
            
        else:
            print ("")
            input("No has pulsado ninguna opción correcta. Pulsa la tecla ENTER para volver al inicio >> ")
    