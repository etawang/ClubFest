from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Map
from .models import Club


# Create your views here.
def index(request, table_id=None):
    try:
        map_obj = Map.objects.get(id=1)
    except Map.DoesNotExist:
        pass
    try:
        club_object = Club.objects.get(id=2)
    except Club.DoesNotExist
        pass
    #template = loader.get_template('map.html')
    template = loader.get_template('search.html')
    context = RequestContext(request, {
        'map': map_obj,
        'club': club_obj,
        'selected_table': table_id
    })
    return HttpResponse(template.render(context))
