from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from .models import Map
from data_parser import load_clubs

# Create your views here.
def index(request):
    mapobj = None
    try:
        mapobj = Map.objects.get(id=1)
    except Map.DoesNotExist:
        pass
    template = loader.get_template('map.html')
    context = RequestContext(request, {
        'map': mapobj
    })
    return HttpResponse(template.render(context))

class UploadForm(forms.Form):
    file = forms.FileField()

def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        print request.FILES
        if form.is_valid():
            template = loader.get_template('upload_resp.html')
            context = RequestContext(request, load_clubs(request.FILES['file']))
            return HttpResponse(template.render(context))
        return HttpResponseRedirect('/upload/')
    else:
        form = UploadForm()
    template = loader.get_template('upload.html')
    context = RequestContext(request, {'form': form})
    return HttpResponse(template.render(context))
