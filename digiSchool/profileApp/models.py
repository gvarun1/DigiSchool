from django.db import models

from digiSchool.loginApp.models import UserDB

class profilePageData(models.Model):
	userDBmodeldata = models.OneToOneField(UserDB, on_delete=models.CASCADE)
	profilepic = models.CharField(max_length=500, default="bg_logo.jpg") # Just a url path to image file stored. # Add some default photo.