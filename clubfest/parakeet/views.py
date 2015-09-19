from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from .models import Map, Table, Club
from data_parser import load_clubs

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

class ChangeClubForm(forms.Form):
	club_id = forms.IntegerField(label="Club ID:")

class SearchClubForm(forms.Form):
	club_name = forms.CharField(label="Club Name:", required=False)
	club_category = forms.ChoiceField (choices=Club.CATEGORY_CHOICES, label="Club category", required=False)

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

 	form2 = SearchClubForm(request.GET)
	if form2.is_valid():
	  	club_name=form2.cleaned_data['club_name']
	  	club_categ3ory =form2.cleaned_data['club_category']
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
