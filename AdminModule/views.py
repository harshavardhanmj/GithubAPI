from django.shortcuts import render, render_to_response
import requests
import json
import datetime
from datetime import timedelta
from .models import GitUsers
from django.db.models import Q
from .forms import SearchData, FetchData
from django.core import files
from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView
# Create your views here.

#Facilate single html page with multiple forms and listview to occupy fetch github data, search upon criteria, list all the user details 
class MainView(TemplateView):
	template_name = 'admin.html'

	def get(self, request, *args, **kwargs):
		FetchData_form = FetchData(self.request.GET or None)
		SearchData_form = SearchData(self.request.GET or None)
		context = self.get_context_data(**kwargs)
		context['FetchData_form'] = FetchData_form
		context['SearchData_form'] = SearchData_form
		return self.render_to_response(context)

	def get_context_data(self, **kwargs):
		currentDate = datetime.datetime.now().date()
		kwargs['object_list'] = GitUsers.objects.all()
		kwargs['day'] = GitUsers.objects.filter(log_date=currentDate).count()
		dateItr = 0
		userCount = 0
		while dateItr < 31:
			diffDate = currentDate - timedelta(days=dateItr)
			tempUserCount = GitUsers.objects.filter(log_date=diffDate).count()
			userCount = userCount + tempUserCount
			if dateItr == 7:
				kwargs['week'] = userCount
			dateItr = dateItr + 1
		kwargs['month'] = userCount
		return super(MainView, self).get_context_data(**kwargs)

#Class to fetch github user upon API calls to github webservice triggered by user inputs of starting ID to fetched and next consecutive users to be fetched
class FetchDataView(FormView):
	form_class = FetchData
	template_name = 'admin.html'
	success_url = '/'

	def post(self, request, *args, **kwargs):
		FetchData_form = self.form_class(request.POST)
		SearchData_form = SearchData()
		if FetchData_form.is_valid():
			starting_id = request.POST.get("starting_id")
			no_of_records = request.POST.get("no_of_records")
			itr_obj = 0
			requestUrl = "https://api.github.com/users?since=" + starting_id + "; rel= next "
			data = requests.get(requestUrl)
			json_data = data.json()
			while(itr_obj < int(no_of_records)):
				try:
					requestUrlIndi = "https://api.github.com/users/" + json_data[itr_obj]['login']
					dataIndi = requests.get(requestUrlIndi)
					jsonIndi = dataIndi.json()
					itr_obj = itr_obj + 1
					qs = GitUsers.objects.filter(user_login = jsonIndi['login'])
					if qs:
						split_createdAt = jsonIndi['created_at'].split("T")
						split_updatedAt = jsonIndi['updated_at'].split("T")
						qs1 = GitUsers.objects.get(user_login = jsonIndi['login'])
						qs1.user_id = jsonIndi['id']
						qs1.email = jsonIndi['email']
						qs1.user_avatar = jsonIndi['avatar_url']
						qs1.user_name = jsonIndi['name']
						qs1.created_on = split_createdAt[0]
						qs1.updated_on = split_updatedAt[0]
						qs1.html_url = jsonIndi['html_url']
						qs1.location = jsonIndi['location']
						qs1.company = jsonIndi['company']
						qs1.save();
					else:
						split_createdAt = jsonIndi['created_at'].split("T")
						split_updatedAt = jsonIndi['updated_at'].split("T")
						GitUsers.objects.create(user_login = jsonIndi['login'], 
							user_id = jsonIndi['id'],
							email = jsonIndi['email'],
							user_name = jsonIndi['name'],
							user_avatar = jsonIndi['avatar_url'],
							created_on = split_createdAt[0],
							updated_on = split_updatedAt[0],
							html_url = jsonIndi['html_url'],
							location = jsonIndi['location'],
							company = jsonIndi['company'])
				except:
					itr_obj = itr_obj + 1
					continue
			return self.render_to_response(self.get_context_data(success=True))
		else:
			return self.render_to_response(self.get_context_data(FetchData_form=FetchData_form, SearchData_form=SearchData_form))

	def get_context_data(self, **kwargs):
		currentDate = datetime.datetime.now().date()
		kwargs['object_list'] = GitUsers.objects.all()
		kwargs['day'] = GitUsers.objects.filter(log_date=currentDate).count()
		dateItr = 0
		userCount = 0
		while dateItr < 31:
			diffDate = currentDate - timedelta(days=dateItr)
			tempUserCount = GitUsers.objects.filter(log_date=diffDate).count()
			userCount = userCount + tempUserCount
			if dateItr == 7:
				kwargs['week'] = userCount
			dateItr = dateItr + 1
		kwargs['month'] = userCount
		return super(FetchDataView, self).get_context_data(**kwargs)	


#Class to avail single criteria search upon login, mail, and created on date
class SearchDataView(FormView):
	form_class = SearchData
	template_name = 'admin.html'
	success_url = '/'

	def post(self, request, *args, **kwargs):
		SearchData_form = self.form_class(request.POST)
		FetchData_form = FetchData()
		object_list = GitUsers.objects.all()
		if SearchData_form.is_valid():
			username = request.POST.get("username")
			created_on = request.POST.get("created_on")
			email = request.POST.get("email")
			if created_on:
				object_list = GitUsers.objects.filter(Q(user_login__iexact = username) | Q(email__iexact = email) | Q(created_on = created_on))
			else:
				object_list = GitUsers.objects.filter(Q(user_login__iexact = username) | Q(email__iexact = email))
			if not username and not created_on and not email:
				object_list = GitUsers.objects.all()
			return self.render_to_response(self.get_context_data(success=True, object_list=object_list))
		else:
			return self.render_to_response(self.get_context_data(FetchData_form=FetchData_form, SearchData_form=SearchData_form,object_list=object_list))

	def get_context_data(self, **kwargs):
		currentDate = datetime.datetime.now().date()
		kwargs['day'] = GitUsers.objects.filter(log_date=currentDate).count()
		dateItr = 0
		userCount = 0
		while dateItr < 31:
			diffDate = currentDate - timedelta(days=dateItr)
			tempUserCount = GitUsers.objects.filter(log_date=diffDate).count()
			userCount = userCount + tempUserCount
			if dateItr == 7:
				kwargs['week'] = userCount
			dateItr = dateItr + 1
		kwargs['month'] = userCount
		return super(SearchDataView, self).get_context_data(**kwargs)	