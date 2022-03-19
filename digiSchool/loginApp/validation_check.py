def nameCheck(value):
	MaxAllowed = 20
	value = value.strip()
	if len(value) > 20 or len(value) < 1:
		return False
	for char in value:
		if (ord(char) > 122 or ord(char) < 97):
			return False
		else:
			continue
	return True

def classCheck(value):
	value = value.strip()
	if len(value) > 2 or len(value) < 1:
		return False
	new_value = ""
	for v in value:
		if (ord(v) > 57 or ord(v) < 48):
			return False
		else:
			new_value += v
	if len(new_value) > 2 or len(new_value) < 1:
		return False
	try:
		integer_check = int(new_value)
	except:
		return False
	if integer_check > 12 or integer_check < 1:
		return False
	return True

def sectionCheck(value):
	value = value.strip()
	if len(value) != 1:
		return False
	if value.upper() not in ["A", "B", "C", "D", "E", "F"]:
		return False
	return True

def rCheck(value):
	value = value.strip()
	if len(value) > 11 or len(value) < 10:
		return False
	new_value = ""
	for v in value:
		if (ord(v) > 57 or ord(v) < 48):
			return False
		else:
			new_value += v
	if len(new_value) > 11 or len(new_value) < 10:
		return False
	try:
		integer_check = int(new_value)
	except:
		return False
	return True

def contactCheck(value):
	value = value.strip()
	if len(value) > 10 or len(value) < 4:
		return False
	new_value = ""
	for v in value:
		if (ord(v) > 57 or ord(v) < 48):
			return False
		else:
			new_value += v
	if len(new_value) > 10 or len(new_value) < 4:
		return False
	try:
		integer_check = int(new_value)
	except:
		return False
	return True

def schoolNameCheck(value):
	MaxAllowed = 200
	value = value.strip()
	if len(value) > 200 or len(value) < 10:
		return False
	return True

def categoryCheck(value):
	value = value.strip()
	if value.upper() not in ["STUDENT", "TEACHER"]:
		return False
	return True

def passwordCheck(value):
	value = value.strip()
	if len(value) < 8 or len(value) > 25:
		return False
	else:
		return True

def emailCheck(value):
	return True