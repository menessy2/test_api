from django.db import models
import datetime
from django.contrib.auth.models import User
import string


HTTP_METHODS = [
        ( 'GET' ,  'GET' ), 
        ( 'POST' ,  'POST' ), 
        ( 'PUT' ,  'PUT' ), 
]



class Test_Case(models.Model):
    name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(default=datetime.datetime.now())
    belong_to_user = models.ForeignKey(User)


class Request(models.Model):
    url = models.URLField()
    body = models.TextField(null=True, blank=True)
    method = models.CharField(choices=HTTP_METHODS, max_length=5)
    belong_to_test_case = models.ForeignKey(Test_Case)
    headers = models.TextField(null=True, blank=True)
    

class Listener(models.Model):
    testing_url = models.CharField(max_length=255, unique=True)
    belong_to_test_case = models.ForeignKey(Test_Case)
    
    
class Response(models.Model):
    status = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(default=datetime.datetime.now())
    belong_to_request = models.ForeignKey(Request, null=True, blank=True)
    belong_to_listener = models.ForeignKey(Listener, null=True, blank=True)
    headers = models.TextField(null=True, blank=True)
    
    
#class Header(model.Model):
#    name = models.CharField(max_length=255, null=True, blank=True)
#    value = models.CharField(max_length=255, null=True, blank=True)
#    belong_to_request = models.ForeignKey(Request, null=True, blank=True)
#    belong_to_response = models.ForeignKey(Response, null=True, blank=True)
    

    
    
