from django.db import models
from django.core.exceptions import ValidationError

# Validators.
def is_a_number(cn):
	try:
		num = int(cn)
		if len(num) == 10:
			pass
		else:
			raise ValidationError("Not a valid number.")
	except:
		raise ValidationError
def is_a_section(sec):
	if sec.upper() in ["A", "B", "C", "D", "E", "F"]:
		pass
	else:
		raise ValidationError("Not a valid class section.")

# Classes.
class UserDB(models.Model):
	first_name = models.CharField(max_length=40)
	last_name = models.CharField(max_length=40)
	email_addr = models.EmailField()
	class_int = models.IntegerField()
	class_section = models.CharField(max_length=1, validators=[is_a_section])
	school_name = models.CharField(max_length=100)
	contact_detail = models.CharField(max_length=10, validators=[is_a_number])
	passwd = models.CharField(max_length=300) # Must be already hashed+salted at the user end itself (i.e. the data coming to us is already a hash value).