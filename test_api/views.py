from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django import forms
import random
import httplib
import urllib
from urlparse import urlparse
from models import *

class request_form (forms.Form):
    url = models.URLField()
    body = models.TextField(null=True, blank=True)
    method = models.CharField(choices=HTTP_METHODS, max_length=5)
    #headers = models.CharField(max_length=255, null=True, blank=True)


def id_generator(size=50, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

@csrf_exempt
def home(request):
    
    if request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect('/profile')
            
        return render_to_response("landing_page.html", {} , RequestContext(request)) 
        
    user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
    if user:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/profile')
        else:
            return render_to_response("landing_page.html", { 'error' : 'User was suspended' } , RequestContext(request)) 
    else:
        return HttpResponseRedirect('') 
            
            
    
@login_required
def profile(request):
    
    return render_to_response("profile_page.html", { } , RequestContext(request)) 
    
    
@login_required
def create_test_case(request):

    Test_Case.objects.create(name=request.POST.get('name'))
    return render_to_response("test_creation.html", { 'success' : 'Test was created successfully' } , RequestContext(request)) 
    
    

@login_required
def create_listener(request, test_case_id):
    
    test_case = Test_Case.objects.get(id=test_case_id)
    listener = Listener.objects.create(testing_url=str(request.user.username)+id_generator(), belong_to_test_case=test_case)
    unique_listener = 'http://'+request.get_host()+'/test_case/listener/' + str(listener.testing_url)
    return render_to_response("test_creation.html", { 'Listener_url' : unique_listener } , RequestContext(request)) 
    
@login_required
def create_request(request, test_case_id):

    if request.method == 'POST':
        form = request_form(request.POST)

        if form.is_valid():
            test_case = Test_Case.objects.get(id = test_case_id)
            new_request = Request.objects.create(url = form.url, body = form.body, method = form.method, belong_to_test_case = test_case)
            p = urlparse(form.url)
            
            if p.scheme == 'http':
                con = httplib.HTTPConnection(p.hostname(), 80)
            elif p.scheme == 'https' :
                con = httplib.HTTPSConnection(p.hostname(), 443)
            else:
                return render_to_response("profile_page.html", { 'error' : 'Only http and https protocols are supported' } , RequestContext(request))

            con.request(form.method, p.path, form.body, request.POST.get('headers'))
            resp = con.getresponse()
            new_response = Response.objects.create(status = resp.status, body = resp.read(), belong_to_request = new_request)
            return render_to_response("profile_page.html", { 'Response_url' : new_response } , RequestContext(request)) 

        else:
            return render_to_response("profile_page.html", { 'error' : 'One of the fields you have entered is invalid' } , RequestContext(request))


