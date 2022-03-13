from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import Template, Context
from digiSchool.loginApp import models as login_model
from django.middleware import csrf
# Create your views here.

def signUpPage(request):
	csrf_token = csrf.get_token(request)
	templateto = Template(r'''<form action="/signup/posted/" method="POST">{% csrf_token %}<input type="text" name="fn"><input type="text" name="ln"><input type="text" name="ea"><input type="text" name="cd"><input type="text" name="cl"><input type="text" name="cs"><input type="text" name="sn"><input type="text" name="pswd"><input type="submit" value="Create"></form>''')
	return HttpResponse(templateto.render(Context({"csrf_token":csrf_token})))


def signUpPosted(request):
	# A security check
	if request.GET or len(request.GET) > 0:
		"""A Malicious user trying to change the method, to look for sec breach"""
		return HttpResponse('<body><meta http-equiv="refresh" content="0; url="http://127.0.0.1:8000/signup/"/></body>')
	
	uInput = request.POST
	f_name, l_name = uInput.get("fn", False), uInput.get("ln", False)
	e_addr, contact = uInput.get("ea", False), uInput.get("cd", False)
	cls_int, cls_sec = uInput.get("cl", False), uInput.get("cs", False)
	s_name = uInput.get("sn", False)
	passwd = uInput.get("pswd", False) 
	
	"""****************Passwd is passed through our hashing algorithm***********************************"""

	# After this, the "passwd" contains a Hashed + Salted password.

	if len(login_model.UserDB.objects.filter(email_addr=e_addr)) > 0:
		return HttpResponse("<p>user already exists.</p>") # Create a redirect to login page.
	try:
		setting_user = login_model.UserDB(first_name = f_name, last_name = l_name, email_addr=e_addr, class_int=cls_int, class_section=cls_sec, school_name = s_name, contact_detail=contact, passwd=passwd)
	except:
		# Replace with the actual error page. and finallly return to the sign up page.
		return HttpResponse('<p> Error in some data, please signup again.</p><meta http-equiv="refresh" content="0; url="http://127.0.0.1:8000/signup/"/>')
	setting_user.save()

	return HttpResponse(f"User {f_name} Succesfully created.")



def loginPage(request):
	if len(request.GET) == 2 and request.GET.get("uname", False) and request.GET.get("pswd", False):
		Authentication = False
		if request.POST or len(request.POST) > 0:
			"""A Malicious user trying to change the method, to look for sec breach"""
			return HttpResponse('<body><meta http-equiv="refresh" content="0; url="http://127.0.0.1:8000/login/"/></body>')
		
		uInput = request.GET
		uname = uInput.get("uname", False)
		passwd = uInput.get("pswd", False)

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
		templateto = Template(r'''<form action="/login/" method="GET"><input type="text" name="uname"><input type="text" name="pswd"><input type="submit" value="Create"></form>''')
		return HttpResponse(templateto.render(Context({})))