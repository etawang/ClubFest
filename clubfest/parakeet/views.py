from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Map

# Create your views here.
def index(request, table_id=None):
    try:
        map_obj = Map.objects.get(id=1)
    except Map.DoesNotExist:
        pass
    template = loader.get_template('map.html')
    context = RequestContext(request, {
        'map': map_obj,
        'selected_table': table_id
    })
    return HttpResponse(template.render(context))
