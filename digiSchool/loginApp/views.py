from django.shortcuts import render # Importing general utilities.
from django.http import HttpRequest, HttpResponse
from django.template import Template, Context

# Importing models modules
from digiSchool.loginApp import models as login_model
from digiSchool.profileApp import models as profile_model

# Importing Security modules.
from django.middleware import csrf
import bcrypt
from digiSchool.loginApp import validation_check


#-----------------------------------Completed View functions-------------------------------------
def signUpPage(request):
	csrf_token = csrf.get_token(request)
	return render(request, 'signup_page.html', {"csrf_token":csrf_token , "error_signing" : False, "user_exist": False})

def signUpPosted(request):
	# Security check for method-interchange vaulnerablity: https://blog.nvisium.com/method-interchange-forgotten
	if request.GET or len(request.GET) > 0:
		return HttpResponse('''<body><meta http-equiv="refresh" content='0; url="/signup/"'/></body>''')

	# Sessions and Tokens.
	csrf_token = csrf.get_token(request)
	
	# Incoming data.
	requestInput = request.POST

	"""Default values are such that, if the value (for a key) is not in the request.POST (dictionary-like), then
		the validation will not be True. Thus lead to "error_signing".
		This above technique resolve the issue of middleman attack where data is tempered or removed (while sending
		request) by tools like burpsuite."""

	f_name, l_name = requestInput.get("fn", "").strip().lower(), requestInput.get("ln", "").strip().lower()
	cls_int, cls_sec = requestInput.get("cl", 0).strip(), requestInput.get("cs", "").strip()
	r_number, s_name = requestInput.get("rn", 0).strip(), requestInput.get("sn", "").strip()
	e_addr, contact = requestInput.get("ea", "").strip().lower(), requestInput.get("cd", 0).strip()
	passwd, category = requestInput.get("pswd", "").strip(), requestInput.get("category", "").strip().upper()

	# Processing Validations.
	first_name_check = validation_check.nameCheck(f_name)
	last_name_check = validation_check.nameCheck(l_name)
	cls_int_check = validation_check.classCheck(cls_int)
	cls_section_check = validation_check.sectionCheck(cls_sec)
	r_number_check = validation_check.rCheck(r_number)
	contact_check = validation_check.contactCheck(contact)
	s_name_check = validation_check.schoolNameCheck(s_name)
	category_check = validation_check.categoryCheck(category)
	passwd_check = validation_check.passwordCheck(passwd)
	e_addr_check = validation_check.emailCheck(e_addr)

	# password check at frontend to be done.

	if not (first_name_check and last_name_check and cls_int_check and cls_section_check and r_number_check and contact_check and s_name_check and category_check and passwd_check and e_addr_check):
		# The incoming data was corrupted (maybe using burpsuite.) (This is because, all the above validations were done at frontend, but still the value arent valid values.)
		return render(request, 'signup_page.html', {"csrf_token":csrf_token , "error_signing" : True, "user_exist": False})

	"""----------Now all the input values are valid.---------------"""

	# Just for data formating.
	f_name = f_name[0].upper() + f_name[1:]
	l_name = l_name[0].upper() + l_name[1:]

	"""----------Password Hashing + Salting---------------"""
	# Password should always be hashed and salted at the backend.

	if len(login_model.UserDB.objects.filter(email_addr=e_addr)) > 0:
		"""----------User already Exist.---------------"""
		return render(request, 'signup_page.html', {"csrf_token":csrf_token , "error_signing" : False, "user_exist": True})
	
	"""----------Now it is confirmed the user is new.---------------"""
	try:
		setting_user = login_model.UserDB(first_name = f_name, last_name = l_name, email_addr=e_addr, class_int=cls_int, class_section=cls_sec, rollnumber=r_number, school_name = s_name, contact_detail=contact, passwd=passwd, category=category)
		setting_profile = profile_model.profilePageData(userDBmodeldata = setting_user)
		setting_user.save()
		setting_profile.save()
	except:
		"""----------Some Error while setting user. Retry request.---------------"""
		return render(request, 'signup_page.html', {"csrf_token":csrf_token , "error_signing" : True, "user_exist": False})
	
	"""----------User Succesfully Created.---------------"""
	return render(request, 'signup_success.html')



def contactPage(request):
	csrf_token = csrf.get_token(request)
	return render(request, 'contact_page.html', {"csrf_token":csrf_token , "query_submitted": False, "upload_error": False})

def contactPageSubmitted(request):
	if request.GET:
		csrf_token = csrf.get_token(request)
		return render(request, 'contact_page.html', {"csrf_token":csrf_token , "query_submitted": False, "upload_error": True})

	csrf_token = csrf.get_token(request)
	
	requestInput = request.POST

	query_email = requestInput.get("query_email", "").strip()
	query_email_check = validation_check.emailCheck(query_email)

	query_url = requestInput.get("query_url", None).strip()

	query_content = requestInput.get("query_description", "").strip()
	query_content_check = validation_check.schoolNameCheck(query_content) # As it acts similar to a school name.

	if not (query_email_check and query_content_check):
		return render(request, 'contact_page.html', {"csrf_token":csrf_token , "query_submitted": False, "upload_error": True})

	try:
		setting_query = login_model.QueryStore(queryAddress = query_email, queryurl = query_url, queryContent = query_content)
		setting_query.save()
	except:
		return render(request, 'contact_page.html', {"csrf_token":csrf_token , "query_submitted": False, "upload_error": True})

	return render(request, 'contact_page.html', {"csrf_token":csrf_token , "query_submitted": True, "upload_error": False})


def loginPage(request):
	csrf_token = csrf.get_token(request)
	return render(request, "login_page.html", {"csrf_token":csrf_token, "error_login":False, "user_not_exist":False, "invalid_password":False})

#-----------------------------------In-Progress View functions.-------------------------------------


def homePage(request):
	if request.POST:
		return HttpResponse() # to replace with 404 not found.
	return render(request, "home_page.html") # Home page html.



def loginPageCheck(request):
	if request.GET and len(request.GET) > 0:
		return HttpResponse('''<body><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')
	
	csrf_token = csrf.get_token(request)

	if len(request.POST) == 3 and request.POST.get("uname", False) and request.POST.get("pswd", False):
		Authentication = False

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

		# We are using the primary key of UserDB table as user id which lead to user specific page.
		if Authentication:
			# FOr the login we directly send the page. however in case of other time (when section is active.) we will use session id and use the profileApp's viewfunctions.
			return HttpResponse(f'''<body><meta http-equiv="refresh" content='0; url="/profile/{str(usercheck[0].id)}/"'/></body>''')
		else:
			return render(request, "login_page.html", {"csrf_token":csrf_token, "error_login" : False, "user_not_exist": False, "invalid_password": True})
	return render(request, "login_page.html", {"csrf_token":csrf_token, "error_login" : True, "user_not_exist": False, "invalid_password":False})