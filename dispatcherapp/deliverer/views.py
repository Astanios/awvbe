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
from os import walk

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
    F = open(aux, 'rb')
    doc = F.read()

    return HttpResponse(doc)