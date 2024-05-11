# Importamos las funciones
from lib.functions import * 

class web_scrapping_class:
    # Atributos
    url = None
    directorio = None
    url_domain_con_html = None
    url_domain_sin_html = None    

    # Definimos un constructor inicial
    def __init__(self, url = None):

        # Asignamos valor al atributo
        self.url= url
        self.directorio = 'data\\raw\\'

        # Se utiliza expresión regular para capturar solo el texto del dominio y así guardar con nombre diferenciado. 
        # La estructura debe empezar con www. para respetar la expresión regular
        res=re.findall(r'(?<=\.)([^.]+)(?:\.(?:co\.uk|ac\.us|[^.]+(?:$|\n)))',self.url)             
        
        self.url_domain_con_html = res[0]+'_con_html'
        self.url_domain_sin_html = res[0]+'_sin_html'

    # Definimos método principal 
    def scrappear(self):

        # request        
        page = request(self.url)    

        # Extraemos texto de la página (con html tags)
        page_text = page.text

        # Parseamos el contenido 
        soup = BeautifulSoup(page.text, 'html.parser')
        # Extraemos cuerpo de la página (solo texto sin html tags)
        page_body = soup.body.text
        # Aqui se puede ir extrayendo cualquier seccion, etiqueta, clase etc.        

        #Directorios
        directorio_con_html = self.directorio+self.url_domain_con_html  
        directorio_sin_html = self.directorio+self.url_domain_sin_html 

        # Guardamos archivos raw con etiquetas html y en los dos formatos .csv y .txt            
        #download_txt(directorio_con_html,page_text)
        #download_csv(self.url,directorio_con_html,page_text)

        # Guardamos archivos raw sin etiquetas html y en los dos formatos .csv y .txt       
        download_txt(directorio_sin_html,page_body)
        #download_csv(self.url,directorio_sin_html,page_body)
    
    # Métodos Getters and Setters

    def getUrl(self):
        return self.url
    
    def getDirectorio(self):
        return self.directorio
    
    def getUrlDomainConHtml(self):
        return self.url_domain_con_html
    
    def getUrlDomainSinHtml(self):
        return self.url_domain_sin_html

    def setUrl(self, url = None):
        self.url = url
    
    def setDirectorio(self, directorio = None):
        self.directorio = directorio
    
    def setUrlDomainConHtml(self, url_domain_con_html = None):
        self.url_domain_con_html = url_domain_con_html
    
    def setUrlDomainSinHtml(self, url_domain_sin_html = None):
        self.url_domain_sin_html = url_domain_sin_html