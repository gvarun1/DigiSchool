from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import Template, Context
from digiSchool.loginApp import models as login_model
from digiSchool.profileApp import models as profile_model
from django.middleware import csrf



# ALL must be based on sessions which means, in each view, there must be a ifelse claues where if recieved session (from the request) is active then only the page is render, else the login page is rendered.
def profilePage(request, userid):
	try:
		integer_check = int(userid)
	except:
		return HttpResponse('''<body><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')
	return render(request, "profile_page.html", {"user_id" : profile_model.profilePageData.objects.filter(userDBmodeldata=login_model.UserDB.objects.filter(id=userid)[0])[0]})