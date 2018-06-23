from django.db import models

# Create your models here.
class GitUsers(models.Model):
	user_login = models.CharField(null=True,blank=True,max_length=320)
	user_id = models.IntegerField(null=True,blank=True)
	email = models.EmailField(max_length=500,null=True,blank=True)
	user_avatar = models.CharField(null=True, blank=True,max_length=500)
	user_name = models.CharField(max_length=400,null=True,blank=True)
	created_on = models.DateField(auto_now=False, auto_now_add=False,null=True)
	updated_on = models.DateField(auto_now=False, auto_now_add=False,null=True)
	html_url = models.CharField(null=True,blank=True,max_length=600)
	location = models.CharField(null=True,blank=True,max_length=320)
	company = models.CharField(null=True,blank=True,max_length=400)
	log_date = models.DateField(auto_now=False, auto_now_add=True,null=True)

	def __str__(self):
		return self.user_login

