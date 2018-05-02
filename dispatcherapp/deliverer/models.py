from django.db import models
from jsonfield import JSONField

# Create your models here.
class Website(models.Model):

    url = models.CharField(max_length=100)
    date = models.DateField()
    versions = JSONField()