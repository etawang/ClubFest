from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from .models import Map, Table, Club
from data_parser import load_clubs

class UploadForm(forms.Form):
	file = forms.FileField()

def admin_login(request):
  logout(request)
  username = password = ''
  if request.POST:
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
        return HttpResponseRedirect('/')
  return render_to_response('login.html', context_instance=RequestContext(request))

@login_required(login_url='login/')
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

def get_club_list():
  club_list = []
  for club in Club.objects.all():
    club_list.append((club.pk, club.club_name))
  return club_list

class ChangeClubForm(forms.Form):
  club_id = forms.ChoiceField(choices=get_club_list(),label="Assign a club to this table:")

class SearchClubForm(forms.Form):
	club_name = forms.CharField(label="Club Name:")
	club_category = forms.ChoiceField (choices=Club.CATEGORY_CHOICES, label="Club category")

def full_map_for_map(map_obj):
  category_map = []
  for table_row in map_obj.tables:
    map_row = []
    for table in table_row:
      clubs = Club.objects.filter(table_id=table)
      if clubs:
        map_row.append((table, clubs[0].get_category_display()))
      elif table:
        map_row.append((table, 'unassigned'))
      else:
        map_row.append((table, 'blank'))
    category_map.append(map_row)
  return category_map

def index(request, table_id=None):
    try:
        map_obj = Map.objects.get(id=1)
    except Map.DoesNotExist:
        pass
    template = loader.get_template('map.html')
    request_dict = {}
    request_dict['map'] = full_map_for_map(map_obj)
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
                    club = clubs[0]
                    club.table_id = -1
                    club.save(update_fields=['table_id'])
                clubs = Club.objects.filter(pk=data['club_id'])
                if clubs[0]:
                    club = clubs[0]
                    club.table_id = table_id
                    club.save(update_fields=['table_id'])
                    request_dict['club'] = clubs[0]
                    request_dict['message'] = 'Sucessfully changed club'
        else:
            form = ChangeClubForm()
        request_dict['form'] = form

    if request.method == 'GET':
        form2 = SearchClubForm(request.GET)
        if form2.is_valid():
            club_name=form2.cleaned_data['club_name']
            club_category =form2.cleaned_data['club_category']
            if club_name !="":
                thisclub=Club.objects.filter(club_name=club_name)
                if thisclub:
                    if club_category=="":
                        request_dict['highlighted_club']=thisclub[0].table_id
                    elif thisclub[0].category==club_category:
                        print "The club you are searching is not in the given category. Please check!"
                else:
                    print "This club cannot be found."
            else:
                searchclubs=Club.objects.filter(club_category=club_category[0])
                if searchclubs:
                    for eachclub in searchclubs:
                        print eachclub.club_name
                        this_tableid=eachclub.table_id
        request_dict['form2']=form2
    context = RequestContext(request, request_dict)
    return HttpResponse(template.render(context))

@login_required(login_url='login/')
def mapgen(request, row=None, col=None):
    map_obj = Map.objects.get(id=1)
    if row and col:
        r = int(row)
        c = int(col)
        map_obj.tables[r][c] = map_obj.num_tables
        map_obj.num_tables += 1
        map_obj.save()
    template = loader.get_template('mapgen.html')
    context = RequestContext(request, {'map': map_obj})
    print map_obj.tables
    return HttpResponse(template.render(context))
