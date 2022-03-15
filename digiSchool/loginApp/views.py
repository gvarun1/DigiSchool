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
		return HttpResponse('<body><meta http-equiv="refresh" content="0; url="http://127.0.0.1:8000/signup/"/></body>')

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

#-----------------------------------In-Progress View functions.-------------------------------------

def contactPage(request):
	csrf_token = csrf.get_token(request)
	return render(request, 'contact_page.html', {"csrf_token":csrf_token})

def loginPage(request):
	if len(request.POST) == 3 and request.POST.get("uname", False) and request.POST.get("pswd", False):
		Authentication = False
		if request.GET and len(request.GET) > 0:
			"""A Malicious user trying to change the method, to look for sec breach"""
			return HttpResponse('<body><meta http-equiv="refresh" content="0; url="http://127.0.0.1:8000/login/"/></body>')
		
		requestInput = request.POST
		uname = requestInput.get("uname", False)
		passwd = requestInput.get("pswd", False)

		if not uname or not passwd:
			# Password or username is not given.
			return HttpResponse("Please enter username and password.") # Create a redirect to login page.

		"""****************Passwd is passed through our hashing algorithm***********************************"""

		if len(login_model.UserDB.objects.filter(email_addr=uname)) == 0:
			# User does not exist.
			return HttpResponse("Please signup first.") # Create a redirect to signup page.
		
		usercheck = login_model.UserDB.objects.filter(email_addr=uname)
		
		if usercheck[0].passwd == passwd:
			Authentication = True
		if Authentication:
			return HttpResponse("Redirect to profile page") # TBD.
		else:
			return HttpResponse("Enter Correct password") # Redirect to login page.
	else:
		# any other thing such as no GET parameters or malicious parameter will lead to login page.
		csrf_token = csrf.get_token(request)
		templateto = Template(r'''<form action="/login/" method="POST">{% csrf_token %}<input type="text" name="uname"><input type="text" name="pswd"><input type="submit" value="Login"></form>''')
		return HttpResponse(templateto.render(Context({"csrf_token":csrf_token})))