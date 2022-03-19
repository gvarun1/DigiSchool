from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import Template, Context
from digiSchool.loginApp import models as login_model
from django.middleware import csrf


#-----------------------------------Completed View functions-------------------------------------
def signUpPage(request):
	csrf_token = csrf.get_token(request)
	return render(request, 'signup_page.html', {"csrf_token":csrf_token , "error_signing" : False, "user_exist": False})


def signUpPosted(request):
	# Security check for method-interchange vaulnerablity: https://blog.nvisium.com/method-interchange-forgotten
	if request.GET or len(request.GET) > 0:
		return HttpResponse('<body><meta http-equiv="refresh" content="0; url="/signup/"/></body>')

	csrf_token = csrf.get_token(request)
	
	requestInput = request.POST
	f_name, l_name = requestInput.get("fn", False), requestInput.get("ln", False)
	e_addr, contact = requestInput.get("ea", False), requestInput.get("cd", False)
	cls_int, cls_sec = requestInput.get("cl", False), requestInput.get("cs", False)
	rollnumber, s_name = requestInput.get("rn", False), requestInput.get("sn", False)
	passwd = requestInput.get("pswd", False)
	
	"""****************passwd is passed through our hashing algorithm***********************************"""
	# After this, the "passwd" contains a Hashed + Salted password.

	if len(login_model.UserDB.objects.filter(email_addr=e_addr)) > 0:
		return render(request, 'signup_page.html', {"csrf_token":csrf_token , "error_signing" : False, "user_exist": True})
	
	try:
		setting_user = login_model.UserDB(first_name = f_name, last_name = l_name, email_addr=e_addr, class_int=cls_int, class_section=cls_sec, rollnumber=rollnumber, school_name = s_name, contact_detail=contact, passwd=passwd)
	except:
		return render(request, 'signup_page.html', {"csrf_token":csrf_token , "error_signing" : True, "user_exist": False})
	setting_user.save()

	return render(request, 'signup_success.html')

def contactPage(request):
	csrf_token = csrf.get_token(request)
	return render(request, 'contact_page.html', {"csrf_token":csrf_token , "query_submitted": False, "upload_error": False})

def loginPage(request):
	csrf_token = csrf.get_token(request)
	return render(request, "login_page.html", {"csrf_token":csrf_token, "error_login":False, "user_not_exist":False, "invalid_password":False})

#-----------------------------------In-Progress View functions.-------------------------------------


def homePage(request):
	if request.POST:
		return HttpResponse() # to replace with 404 not found.
	return render(request, "home_page.html") # Home page html.

def contactPageSubmitted(request):
	if request.GET:
		csrf_token = csrf.get_token(request)
		return render(request, 'contact_page.html', {"csrf_token":csrf_token , "query_submitted": False, "upload_error": True})

	csrf_token = csrf.get_token(request)
	requestInput = request.POST
	query_email = requestInput.get("query_email")
	query_url = requestInput.get("query_url", None)
	query_content = requestInput.get("query_description")

	try:
		setting_query = login_model.QueryStore(queryAddress = query_email, queryurl = query_url, queryContent = query_content)
		setting_query.save()
	except:
		return render(request, 'contact_page.html', {"csrf_token":csrf_token , "query_submitted": False, "upload_error": True})

	return render(request, 'contact_page.html', {"csrf_token":csrf_token , "query_submitted": True, "upload_error": False})


def loginPageCheck(request):
	if request.GET and len(request.GET) > 0:
			return HttpResponse('<body><meta http-equiv="refresh" content="0; url="/login/"/></body>')
	
	if len(request.POST) == 3 and request.POST.get("uname", False) and request.POST.get("pswd", False):
		Authentication = False
		csrf_token = csrf.get_token(request)

		requestInput = request.POST
		uname = requestInput.get("uname", False)
		passwd = requestInput.get("pswd", False)

		if len(uname) == 0 or len(passwd) == 0:
			# Password or username is not given maybe due to burpsuite inputs.
			return render(request, "login_page.html", {"csrf_token":csrf_token, "error_login" : True, "user_not_exist": False, "invalid_password":False})

		if len(login_model.UserDB.objects.filter(email_addr=uname)) == 0:
			# User does not exist.
			return render(request, "login_page.html", {"csrf_token":csrf_token, "error_login" : False, "user_not_exist": True, "invalid_password":False})
		

		"""****************Passwd is passed through our hashing algorithm***********************************"""

		usercheck = login_model.UserDB.objects.filter(email_addr=uname)
		
		if usercheck[0].passwd == passwd:
			Authentication = True

		# Get user profile id or something and then use this id as a template variable to render things.
		if Authentication:
			return HttpResponse("Redirect to profile page") # TBD.
		else:
			return render(request, "login_page.html", {"csrf_token":csrf_token, "error_login" : False, "user_not_exist": False, "invalid_password": True})
		
	return render(request, "login_page.html", {"csrf_token":csrf_token, "error_login" : True, "user_not_exist": False, "invalid_password":False})