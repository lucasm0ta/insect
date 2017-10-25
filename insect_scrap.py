
from bs4 import BeautifulSoup
import urllib3, certifi, json, os, urllib.request
from urllib.parse import urlparse

# Caminho onde vai ser salvo as imagens
direct = "/home/evarildo/UnB/PVC/P4/img/"

# Função que pega a partir da categoria as suas respectivas imagens e salva em uma pasta com o nome estranho contendo
# o ID da categoria.
def getImages(url):
    #print(url)
    numreq = 25 # Numero de imagens por cada request
    req = 8 # Numero de requests por categoria
    #Ou seja, 8*25 = 200 por categoria deve dar ATÉ 200 imagens

    api = "https://api.bugwood.org/rest/api/image/.json?include=descriptor,dateupdated,citation&fmt=datatable&order[0][column]=10&order[0][dir]=desc&columns[8][searchable]=false&columns[1][searchable]=false&columns[7][searchable]=false&columns[10][searchable]=false&columns[4][searchable]=false&columns[11][searchable]=false&page=#&length=*&$&systemid=2"
    api = api.replace('*', numreq)
    query = urlparse(url).query
    print(query)
    path = direct+query
    if not os.path.exists(path):
        os.makedirs(path)
    for i in range(req):
        aux = api.replace('#', str(i + 1))
        aux = aux.replace('$', query)
        print("Request Nº: "+i+1)

        http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
        r = http.request(
            "GET",
            aux,
            headers={
                "Host":"api.bugwood.org",
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv: 55.0) Gecko/20100101 Firefox/55.0",
                "Accept":"text/html, application/xhtml+xml, application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language":"en-US,en;q=0.5",
                "Accept-Encoding":"gzip, deflate, br",
                "DNT":"1",
                "Connection":"keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Pragma":"no-cache",
                "Cache-Control": "no-cache",

            }
        )

        soup = BeautifulSoup(r.data, 'lxml')
        imgs = json.loads(soup.p.string)
        for img in imgs['data']:
            baseurl = str(img[7][2:])
            imgid = str(img[0])
            resolution = "768x512"  # A resolução da imagem pode ser 192x128, 384x256, 768x512.
                                    # quanto maior, menos imagens
            req = "http://www."+ baseurl + resolution + "/" + imgid + ".jpg"
            print("http://www."+ baseurl + resolution + "/" + imgid + ".jpg")
            urllib.request.urlretrieve(req, path + "/" + imgid + ".jpg")

        # print(soup.find_all('img', {'class':'img-responsive'}))


base = 'https://www.insectimages.org/'
site= 'https://www.insectimages.org/index.cfm#order'
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
r = http.request('GET', site)
soup = BeautifulSoup(r.data, 'lxml')

cont = soup.find_all("div", {"class":"well"})[0]
links = set()
for link in cont.find_all('a'):
    links.add(link.get('href'))

for link in links:
    getImages(base + link[1:]) # Remove first '/'

# Exemplo de links da API do site
#https://api.bugwood.org/rest/api/image/.json?include=descriptor,dateupdated,citation&fmt=datatable&order[0][column]=10&order[0][dir]=desc&columns[8][searchable]=false&columns[1][searchable]=false&columns[7][searchable]=false&columns[10][searchable]=false&columns[4][searchable]=false&columns[11][searchable]=false&page=1&length=24&order=98&systemid=2
#https://api.bugwood.org/rest/api/image/.json?include=descriptor,dateupdated,citation&fmt=datatable&order[0][column]=10&order[0][dir]=desc&columns[8][searchable]=false&columns[1][searchable]=false&columns[7][searchable]=false&columns[10][searchable]=false&columns[4][searchable]=false&columns[11][searchable]=false&page=2&length=24&order=98&systemid=2
#https://api.bugwood.org/rest/api/image/.json?include=descriptor,dateupdated,citation&fmt=datatable&order[0][column]=10&order[0][dir]=desc&columns[8][searchable]=false&columns[1][searchable]=false&columns[7][searchable]=false&columns[10][searchable]=false&columns[4][searchable]=false&columns[11][searchable]=false&page=1&length=24&order=131&systemid=2