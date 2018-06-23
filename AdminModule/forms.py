import datetime
from django import forms

#Form to perform single criteria search or filtering of github users
class SearchData(forms.Form):
	username = forms.CharField(required=False)
	created_on = forms.DateField(required=False)
	email = forms.EmailField(required=False)

#Form to fetch the github users based on user request through web service calls to github
class FetchData(forms.Form):
	starting_id = forms.IntegerField(required=True)
	no_of_records = forms.IntegerField(required=True)

	def clean_no_of_records(self):
		no_of_records = self.cleaned_data.get("no_of_records")
		if no_of_records > 10:
			raise forms.ValidationError("Max Record is 10")