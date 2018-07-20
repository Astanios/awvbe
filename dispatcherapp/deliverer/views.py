from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from deliverer.models import Website
from deliverer.serializers import WebsiteSerializer
from django.http import HttpResponse
from solrcloudpy.connection import SolrConnection
from urllib.request import urlopen

import datetime, json, re, glob, os
global log
log = open("log.txt", "w")
conn = SolrConnection(server=["localhost:8987","localhost:7578"], detect_live_nodes=False, user=None, password=None, timeout=10)
coll = conn['archivoWebVenezuela']
SolrURL = 'http://localhost:8001/'

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def matchSite(site):
    result = re.match(r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$', site)
    return bool(result)

@csrf_exempt
def home(request):  
    if request.method == 'GET':
        now = datetime.datetime.now()
        html = "<html><head><style>body{color:blue;}</style></head><body>It is now %s.</body></html>" % now
        return HttpResponse(html)

@csrf_exempt
def jsontest(request):
    data = json.loads(request.body)
    query = data['query']

    if matchSite(query):
        param=  'URL:*'+query+'*'
        respuesta = coll.search({'q':param})
        aux= respuesta.result.response['docs']
        urlsList = []
        dateList = []
        for entry in aux:
            tempmonth = str(entry['month']).replace('[','').replace(']','')
            tempday = str(entry['day']).replace('[','').replace(']','')
            aux = str(entry['year']).replace('[','').replace(']','') + '-' + ('0' if int(tempmonth) < 10 else '') + tempmonth + '-' + ('0' if int(tempday) < 10 else '') + tempday
            dateList.append(aux)
            urlsList.append(entry['URL'])
        response = {
            'type': 'url',
            'url': query,
            'versions': len(aux),
            'list': dateList,
            'urlsList': urlsList
        }
    else:
        param=  'URL:*'+query+'*'
        respuesta = coll.search({'q':param})
        aux = respuesta.result.response['docs']
        urlsList = []
        for entry in aux:
            urlsList.append(entry['URL'])
        response = {
            'type': 'keyword',
            'keywords': query,
            'versions': len(aux),
            'list': urlsList
        }
    
    return JsonResponse(response)
    
    
@csrf_exempt
def siteretrieve(request):
    data = json.loads(request.body)
    query = ''.join(data['site_version'])
    aux = query[(query.rfind('/'))+1:]
    aux = aux[:40] + '.html'
    
    for root, dirs, files in os.walk('../../indexadorsolr/scriptIndexador/'):
        if aux in files:
            aux = os.path.join(root, aux)

    with urlopen(aux) as url:
        s = url.read()

    print(s)


    '''

    for (dirpath, dirnames, filenames) in walk('../../indexadorsolr/scriptIndexador/'):
        for files in filenames:
            #print(files)
            #log.write(str(files)+'\n')
            if str(files).find(aux):
                #print ('encontrado!')
                #aux = dirpath
                print(aux)
                break
    print(aux)
    '''
    now = datetime.datetime.now()
    html = "<html><head><style>body{color:blue;}</style></head><body>It is now %s.</body></html>" % now
    doc = '<!DOCTYPE html><html><head><style>div.container{width: 100%; border: 1px solid gray;}header, footer{padding: 1em; color: white; background-color: black; clear: left; text-align: center;}nav{float: left; max-width: 160px; margin: 0; padding: 1em;}nav ul{list-style-type: none; padding: 0;}nav ul a{text-decoration: none;}article{margin-left: 170px; border-left: 1px solid gray; padding: 1em; overflow: hidden;}</style></head><body><div class="container"><header> <h1>City Gallery</h1></header> <nav> <ul> <li><a href="#">London</a></li><li><a href="#">Paris</a></li><li><a href="#">Tokyo</a></li></ul></nav><article> <h1>London</h1> <p>London is the capital city of England. It is the most populous city in the United Kingdom, with a metropolitan area of over 13 million inhabitants.</p><p>Standing on the River Thames, London has been a major settlement for two millennia, its history going back to its founding by the Romans, who named it Londinium.</p></article><footer>Copyright &copy; W3Schools.com</footer></div></body></html>'
    
    return HttpResponse(doc)