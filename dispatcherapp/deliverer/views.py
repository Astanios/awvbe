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

import datetime
import json
import re

conn = SolrConnection(server=["localhost:8987","localhost:7578"], detect_live_nodes=False, user=None, password=None, timeout=10)
coll = conn['archiveWebVenezuela']

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
        response = {
            'type': 'url',
            'url': query,
            'versions': 4,
            'list': [
                datetime.datetime.now(),
                datetime.datetime(2018,3, 13, 0, 0),
                datetime.datetime(2018,5, 20, 0, 0),
                datetime.datetime(2009,3, 13, 0, 0)
            ]
        }
    else:
        response = {
            'type': 'keyword',
            'results': 2,
            'list': [
                "www.google.com",
                "www.w3schrools.com",
                "www.netflix.com"
            ]
        }
    return JsonResponse(response)
    
    
@csrf_exempt
def siteretrieve(request):
    now = datetime.datetime.now()
    html = "<html><head><style>body{color:blue;}</style></head><body>It is now %s.</body></html>" % now
    doc = '<!DOCTYPE html><html><head><style>div.container{width: 100%; border: 1px solid gray;}header, footer{padding: 1em; color: white; background-color: black; clear: left; text-align: center;}nav{float: left; max-width: 160px; margin: 0; padding: 1em;}nav ul{list-style-type: none; padding: 0;}nav ul a{text-decoration: none;}article{margin-left: 170px; border-left: 1px solid gray; padding: 1em; overflow: hidden;}</style></head><body><div class="container"><header> <h1>City Gallery</h1></header> <nav> <ul> <li><a href="#">London</a></li><li><a href="#">Paris</a></li><li><a href="#">Tokyo</a></li></ul></nav><article> <h1>London</h1> <p>London is the capital city of England. It is the most populous city in the United Kingdom, with a metropolitan area of over 13 million inhabitants.</p><p>Standing on the River Thames, London has been a major settlement for two millennia, its history going back to its founding by the Romans, who named it Londinium.</p></article><footer>Copyright &copy; W3Schools.com</footer></div></body></html>'
    return HttpResponse(doc)
    """
@csrf_exempt
def website(request, url):
    Retrieve, update or delete a serie.

    if request.method == 'GET':
        serializer = WebsiteSerializer(serie)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = Website(website, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        website.delete()
        return HttpResponse(status=204)


@csrf_exempt
def website_list(request):

    List all code serie, or create a new serie.

    if request.method == 'GET':
        websites = Website.objects.all()
        serializer = WebsiteSerializer(websites, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = WebsiteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def website_detail(request, pk):

    Retrieve, update or delete a serie.

    try:
        website = Website.objects.get(pk=pk)
    except Website.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = WebsiteSerializer(serie)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = Website(website, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        website.delete()
        return HttpResponse(status=204)

    """