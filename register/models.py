from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from oauth2client.contrib.django_util.models import CredentialsField

# Create your models here.
class Users (models.Model):
	kris_user_id = models.CharField(max_length=100, null=False)
	gmail_authentication = models.TextField(null=True,default='')
	datecreated = models.DateField()
	kris_url = models.URLField(null=False,default='http://mykris.sqlview.com:8080/KRIS')

class gmailnotification (models.Model):
	historyId = models.CharField(max_length=20,null=False)
	expiration = models.DecimalField(max_digits=12,decimal_places=0,null=False)

class CredentialsModel(models.Model):
  id = models.ForeignKey(User, primary_key=True,on_delete=models.CASCADE)
  credential = CredentialsField

class CredentialsAdmin(admin.ModelAdmin):
    pass