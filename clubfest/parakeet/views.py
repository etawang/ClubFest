from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django import forms
from .models import Map, Table, Club

class ChangeClubForm(forms.Form):
  club_id = forms.IntegerField(label="Club ID:")

# Create your views here.
def index(request, table_id=None):
  try:
      map_obj = Map.objects.get(id=1)
  except Map.DoesNotExist:
      pass
  template = loader.get_template('map.html')
  request_dict = {}
  request_dict['map'] = map_obj
  if table_id:
    table_id = int(table_id)
    clubs = Club.objects.filter(table_id=table_id)
    if clubs:
      request_dict['club'] = clubs[0]
    request_dict['selected_table'] = table_id

    if request.method == 'POST':
      form = ChangeClubForm(request.POST)
      if form.is_valid():
        data = form.cleaned_data
        print data
        if clubs:
          clubs[0].table_id = -1
          clubs[0].save()
        clubs = Club.objects.filter(pk=data['club_id'])
        if clubs[0]:
          print clubs[0].club_name
          print "Selected table: " + str(table_id)
          clubs[0].table_id = table_id
          clubs[0].save()
          print "After save: " + str(clubs[0].table_id)
          request_dict['club'] = clubs[0]
        request_dict['message'] = 'Sucessfully changed club'
    else:
      form = ChangeClubForm()
    request_dict['form'] = form
  context = RequestContext(request, request_dict)
  return HttpResponse(template.render(context))
