#	Import modules and models

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from .models import veremail, Patient_reg, Patient_details, Donor_reg, Donor_details, Hospital_reg
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
#from django.views.decorators.csrf import requires_csrf_token
from random import randint as rand
import hashlib
from .forms import loginform, passconfrm

#	declare variables for further use

dbp = {'donor' : Donor_reg, 'user' : Patient_reg, 'hospital' : Hospital_reg}
dbt = {'donor' : Donor_details, 'user' : Patient_details}


# Hash function

def md5hash(msg):
	rs = hashlib.md5(msg.encode())
	return str(rs.hexdigest())

#	Delete values in a database when username is given for OTP verification

def dropindb(db,name):
	db.objects.filter(uname=str(name)).delete()


#	Get data from a certain database and certain value for known username

def get_data(column, value, datab):
	query = datab.objects.get(uname=str(value))
	return getattr(query, column)

#	mail function to send email

def sendmail(email,subject,body):
	import pythoncom
	import win32com.client as win32
	pythoncom.CoInitialize()
	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.To = email
	mail.Subject = subject
	mail.HTMLBody = '<p>'+str(body)+'</p>'
	mail.send


# Function to create session for number of tries for a login or a bypassing OTP 

def tryreq(response,request):

	if 'sess_try' in request.COOKIES:
		try_no = int(request.COOKIES['sess_try'])
		print("tried ",try_no,"times")
		if try_no>3:	#	Set maximum number of tries (initally 3s)
			return True
		else:
			response.set_cookie('sess_try' , str(try_no+1))
	else:
		response.set_cookie('sess_try' , str(0))

	return False

#	Function to change in the databse to show that email is verifed

def em_verified(name,db):
	if db == "donor":
		Donor_reg.objects.filter(username=name).update(email_verified=1)
	elif db == "users":
		Patient_reg.objects.filter(username=name).update(email_verified=1)
	elif db == "hospital":
		Hospital_reg.objects.filter(username=name).update(email_verified=1)

#	Confirm registration function. User is redirected to this view for OTP verification

def confirm_register(request):

	if request.method == "POST":
		context = request.POST
		code = request.POST.get('code')
		uname = request.POST.get('uname')
		print(uname,code)
		md = request.POST.get('catg')
		cd=get_data('ab',uname,veremail)

		if int(cd) == int(code):	#	Checks if OTP's matches or not
			em_verified(uname,md)
			return HttpResponseRedirect('/accounts/login')
		else:
			template = loader.get_template('confirm_register.html')
			context['error'] =  "Sorry. OTP didn't mtach."
			context.update(csrf(request))

			response = HttpResponse(template.render(context,request))
			tryreq(response,request)
			return response


#	Uploads the data to the database

def uptodb(ctg,details,cd):
	print(details)

	#	Checks who is the requested user.

	if str(ctg) == 'donor':
		ne = Donor_reg.objects.create(username = details['uname'] ,email = details['email'], password = md5hash(details['passwd']), first_name = details['fname'], las_name = details['lname'], email_verified=0)
		new_entry = Donor_details.objects.create(userd = ne, ad_line1 = details['line1'], ad_line2 = details['line2'], pincode = details['postalcode'], city = details['city'], state = details['state'], gender = details['gender'], ph_no = details['ph_no'], d_o_b=details['dob'], weight = details['weight'], height = details['height'], blood_group = details['bgroup'])

	elif str(ctg) == 'hospital':
		ne = Hospital_reg.objects.create(username = details['uname'] ,email = details['email'], password = md5hash(details['passwd']), hospital_name = details['name'], ad_line1 = details['line1'], ad_line2 = details['line2'], pincode = details['postalcode'], city = details['city'], state = details['state'], license = details['license'], semail_verified = 0)

	elif str(ctg) == 'users':
		ne = Patient_reg.objects.create(username = details['uname'] ,email = details['email'], password = md5hash(details['passwd']), first_name = details['fname'], last_name = details['lname'], email_verified=0)
		new_entry = Patient_details.objects.create(userp = ne, gender = details['gender'], ph_no = details['ph_no'], d_o_b = details['dob'], blood_group = details['bgroup'])

	ef = veremail.objects.create(ab=int(cd), uname=str(details['uname']))
	print('created otp')


#	Register main view

def register(request):
	if request.method == 'POST':
		flagem = 0
		flagun = 0
		type = request.POST.get('category')
		if str(type) == str("donor"):
			details = {
				'fname' : request.POST.get('fname'),
				'lname' : request.POST.get('lname'),
				'uname' : request.POST.get('uname'),
				'email' : request.POST.get('email'),
				'passwd' : request.POST.get('passwd'),
				'dob' : request.POST.get('dob'),
				'line1' : request.POST.get('line1'),
				'line2' : request.POST.get('line2'),
				'city' : request.POST.get('city'),
				'postalcode' : request.POST.get('postalcode'),
				'state' : request.POST.get('state'),
				'country' : request.POST.get('country'),
				'gender' : request.POST.get('gender'),
				'ph_no' : request.POST.get('phno'),
				'bgroup' : request.POST.get('bgroup'),
				'height' : request.POST.get('height'),
				'weight' : request.POST.get('weight'),
			}
			a=Donor_reg.objects.filter(email = details['email'])
			if a:
				flagem = 1
			b=Donor_reg.objects.filter(username = details['uname'])
			if b:
				flagun = 1

		elif str(type) == str("hospital"):
			details = {
				'name' : request.POST.get('name'),
				'uname' : request.POST.get('uname'),
				'email' : request.POST.get('email'),
				'passwd' : request.POST.get('passwd'),
				'line1' : request.POST.get('line1'),
				'line2' : request.POST.get('line2'),
				'city' : request.POST.get('city'),
				'postalcode' : request.POST.get('postalcode'),
				'country' : request.POST.get('country'),
				'state' : request.POST.get('state'),
				'license' : request.POST.get('license'),
			}
			a=Hospital_reg.objects.filter(email = details['email'])
			if a:
				flagem = 1
			b=Hospital_reg.objects.filter(username = details['uname'])
			if b:
				flagun = 1

		elif str(type) == str("users"):
			details = {
				'fname' : request.POST.get('fname'),
				'lname' : request.POST.get('lname'),
				'uname' : request.POST.get('uname'),
				'email' : request.POST.get('email'),
				'passwd' : request.POST.get('passwd'),
				'dob' : request.POST.get('dob'),
				'gender' : request.POST.get('gender'),
				'ph_no' : request.POST.get('phno'),
				'bgroup' : request.POST.get('bgroup'),
			}
			a=Patient_reg.objects.filter(email = details['email'])
			if a:
				flagem = 1
			b=Patient_reg.objects.filter(username = details['uname'])
			if b:
				flagun = 1
		if details:
			unm =  details['uname']		
		context = {
				'uname' : unm,
				'catg' : 'type',
			}
		dropindb(veremail,unm)
		email = details['email']
		context.update(csrf(request))
		code = rand(100000,999999)
		if flagem==0:
			if flagun == 0:
				print('working')
				uptodb(type,details,code)
				sub="OTP for registration in Blood_bank_management_website"
				body="This is a computer generated mail. Please do not reply back to this email.<br> The OTP code for your registration process is "+str(code)
				sendmail(email,sub,body)
				template = loader.get_template('confirm_register.html')
				return HttpResponse(template.render(context,request))
			else:
				context['eunm'] = 'uname' 
		else:
			context['eem'] = 'email' 
		template = loader.get_template('register.html')
		print('loaded template')
		return HttpResponse(template.render(context,request))


	else:
		template = loader.get_template('register.html')
		context = {}
		context.update(csrf(request))
		return HttpResponse(template.render(context,request))

def index(request):
	template = loader.get_template('index.html')
	return HttpResponse(template.render())

def login(request):
	if request.method == "POST":
		
		dd = request.POST
		wry = dd['Who_are_you']
		uname = dd['username']
		passwd = dd['password']
		print(uname)
		if str(wry) == 'donor':
			fndb = Donor_reg
		elif str(wry) == 'hospital':
			fndb = Hospital_reg
		elif str(wry) == 'user':
			fndb = Patient_reg
#		try:
		rs = fndb.objects.filter(username=uname,password=md5hash(passwd))
		if rs:
			context = {'uname':uname}
			template = loader.get_template('aflogin.html')
			request.session['sess_id_'+str(wry)]='bbms_'+str(wry)+'_'+str(uname)
			context[str(wry)] = uname
			if request.session.has_key('sess_togo'):
				togo = request.session['sess_togo']
				del request.session['sess_togo']
				if togo=='donor':
					return HttpResponseRedirect('/donor_portal/')
				elif togo=='hospital':
					return HttpResponseRedirect('/hospital_portal/')
				elif togo=='patient':
					return HttpResponseRedirect('/patient_portal/')
			return HttpResponseRedirect('/')

		else:
			template = loader.get_template('login.html')
			context = { 'form':loginform }

			context['error'] = "Sorry. Invalid credentils."
			response = HttpResponse(template.render(context,request)) 

			if tryreq(response,request):
				return HttpResponse("You've tried incorrectly three times. Please try again after some time")

			return response

	else:
		template = loader.get_template('login.html')
		context = { 'form':loginform }
		return HttpResponse(template.render(context,request))

def aflogin(request):

	flag = 0
	context = {}
	if request.session.has_key('sess_id_user'):
		un = str(request.session['sess_id_user']).split('_')
		context['user'] = un[2]
		flag = 1

	if request.session.has_key('sess_id_hospital'):
		un = str(request.session['sess_id_hospital']).split('_')
		context['hospital'] = un[2]
		flag = 1 

	if request.session.has_key('sess_id_donors'):
		un = str(request.session['sess_id_donors']).split('_')
		context['donor'] = un[2]
		flag = 1

	if flag==1:
		template = loader.get_template('aflogin.html')
		return HttpResponse(template.render(context,request))
	else:
#		print("Hello")
		return HttpResponseRedirect("/accounts/login/")



def logout(request):
	if request.method == "GET":
		ctg = request.GET.get('ctg')
		if ctg == "userd":
			if request.session.has_key('sess_id_user'):
				del request.session['sess_id_user']
		if request.session.has_key('sess_id_'+str(ctg)):
			del request.session['sess_id_'+str(ctg)]
	return HttpResponse("<p>You're logged out.</p>")

def fpassinit(request):
	if request.method == 'POST':
		context = {}
		context['email'] = request.POST.get('email')
		context['username'] = request.POST.get('uname')
		context['catg'] = request.POST.get('catg')
#		print(context)
		if context['catg'] == "donor":
			fndb = Donor_reg
		elif context['catg'] == "hospital":
			fndb = Hospital_reg
		elif context['catg'] == "patient":
			fndb = Patient_reg

		ig = fndb.objects.filter(username = context['username'],email = context['email'])
		if ig:
#			print('you are amazing')
			cd = rand(100000,999999)
#			print(cd)
			sub = "Request for change in password"
			body = "We found that you are trying to change your " + str(context['catg']) + " account's password. We are sending the OTP to authenticate if this is you or not. Please do not share this OTP with anyone else. This is highly confidential. The OTP is " + str(cd)
			dropindb(veremail,context['username'])
			ef = veremail.objects.create(ab=int(cd), uname=str(context['username']))
#			sendmail(context['email'],sub,body)
			template = loader.get_template('fpassotp.html')
			return HttpResponse(template.render(context,request))

		else:
			return HttpResponse("sorry but the details are not matching with the database")
	else:
		template = loader.get_template('fpassinit.html')
		return HttpResponse(template.render())

def fpassotp(request):
	if request.method == 'POST':
		catg = request.POST.get('catg')
#		print(catg)
		otp = int(request.POST.get('otp'))
		uname = request.POST.get('uname')
#		print(otp,uname)
		try:
			context = {'uname':"Sowri",'form':passconfrm, "catg":catg}
			cd = int(get_data('ab',uname,veremail))
			if cd == otp:
				template = loader.get_template('fpassverfied.html')
				return HttpResponse(template.render(context,request))
			else:
				return HttpResponse("OTP doesn't match.")
		except:
			return HttpResponse("Sorry. But either the username doesn't exist or you've bypassed the OTP verifcation. ")

	else:
		return HttpResponseRedirect("/accounts/login/")

def chpass(request):
	if request.method == "POST":
		ctg = request.POST.get("catg")
		p1 = request.POST.get("password")
		p2 = request.POST.get("passwordconfrm")
		uname = request.POST.get("uname")
		if p1 == p2:
			print("working",p1,p2)
			fndb = None
			if ctg == "donor":
				fndb = Donor_reg
			elif ctg == "hospital":
				fndb = Hospital_reg
			elif ctg == "patient":
				fndb = Patient_reg
			fndb.objects.filter(username = uname).update(password=md5hash(p1))
#			print("succesfully changed password")
		return HttpResponseRedirect("/accounts/login")
	else:
		return HttpResponseRedirect("/")

def profile(request):
	catg = request.GET.get('catg')
	var = 'sess_id_'+str(catg)
	if request.session.has_key(var):
		print('working')
		uname = request.session[var].split("_")[2]
		print(uname)
		al = dbp[catg].objects.filter(username = uname).get()
#		dt = dbt[catg].objects.filter(userd = al).get()
		context = {'uname' : uname}
#		context['details'] = catg
		if catg=="user":
			context['catg'] = 'userd'
		else:
			context['catg'] = catg
#		context['details'] = dt
		template =  loader.get_template('profile.html')
		return HttpResponse(template.render(context,request))
	else:
		return HttpResponseRedirect('/accounts/login')

def uppurofile(request):
	if request.method == "POST":
		details = request.POST
		uname = details['uname']
		fndb = dbp[details['catg']]
		print(uname)
#		if 
#		fndb.objects.filter()
	return HttpResponse("Hello")

def upsett(request):
	if request.method == "POST":
		context = {}
		passc = request.POST
		pass1 = passc['passwd'] 
		pass2 = passc['npasswd'] 
		pass3 = passc['npasswdc']
		uname = passc['uname']
		fndb = dbp[passc['catg']]
		print(fndb)
		if fndb.objects.filter(username = uname):
			if fndb.objects.filter(password = md5hash(pass1)):
				if pass2 == pass3:
					print("yes")
					fndb.objects.filter(username = uname).update(password = md5hash(pass2))
					return HttpResponseRedirect("/")
				else:
					context['newper'] = 1
			else:
				context['oldp'] = 1
		template =  loader.get_template('profile.html')
		return HttpResponse(template.render(context,request))
	else:
		return HttpResponseRedirect("/")