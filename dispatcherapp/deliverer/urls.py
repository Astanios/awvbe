from django.conf.urls import url
from deliverer import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^json/$', views.jsontest),
    url(r'^site/$', views.siteretrieve),
]