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

def md5hash(msg):
	rs = hashlib.md5(msg.encode())
	return str(rs.hexdigest())

def dropindb(db,name):
	db.objects.filter(uname=str(name)).delete()

def get_data(column, value, datab):
	query = datab.objects.get(uname=str(value))
	return getattr(query, column)

def sendmail(email,subject,body):
	import pythoncom
	import win32com.client as win32
	pythoncom.CoInitialize()
	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.To = email
	mail.Subject = subject
	mail.Body = body
#	mail.HTMLBody = '<h2>HTML Message body</h2>' #this field is optional
	mail.send

def em_verified(name,db):
	if db == "donor":
		Donor_reg.objects.filter(username=name).update(email_verified=1)
	elif db == "users":
		Patient_reg.objects.filter(username=name).update(email_verified=1)
	elif db == "hospital":
		Hospital_reg.objects.filter(username=name).update(email_verified=1)

def confirm_register(request):
	if request.method == "POST":
		code = request.POST.get('code')
		uname = request.POST.get('uname')
		md = request.POST.get('catg')
		try:
			cd=get_data('ab',uname,veremail)
		except:
			return HttpResponse("OTP's didn't match")
		if int(cd) == int(code):
			em_verified(uname,md)
			print("Signed up successfully")
			return HttpResponseRedirect('/')
		else:
			return HttpResponse("<h1>OTP didint match</h1>")
#		except Exception as e:
#			print(e)
#			return HttpResponse("<h1>Internal server problem.<br></h1><p> Please give us a little while.</p>")

#@requires_csrf_token

def uptodb(ctg,details,cd):

	if str(ctg) == 'donor':
		ne = Donor_reg.objects.create(username = details['uname'] ,email = details['email'], password = md5hash(details['passwd']), first_name = details['fname'], las_name = details['lname'], email_verified=0)
		new_entry = Donor_details.objects.create(userd = ne, ad_line1 = details['line1'], ad_line2 = details['line2'], pincode = details['postalcode'], city = details['city'], state = details['state'], gender = details['gender'], ph_no = details['ph_no'], d_o_b=details['dob'], weight = details['weight'], height = details['height'], blood_group = details['bgroup'])

	elif str(ctg) == 'hospital':
		ne = Hospital_reg.objects.create(username = details['uname'] ,email = details['email'], password = md5hash(details['passwd']), hospital_name = details['name'], ad_line1 = details['line1'], ad_line2 = details['line2'], pincode = details['postalcode'], city = details['city'], state = details['state'], license = details['license'],email_verified = 0)

	elif str(ctg) == 'users':
		ne = Patient_reg.objects.create(username = details['uname'] ,email = details['email'], password = md5hash(details['passwd']), first_name = details['fname'], last_name = details['lname'], email_verified=0)
		new_entry = Patient_details.objects.create(userp = ne, gender = details['gender'], ph_no = details['ph_no'], d_o_b = details['dob'], blood_group = details['bgroup'])

	ef = veremail.objects.create(ab=int(cd), uname=str(details['uname']))


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
			print(details)
#			return HttpResponse("Hello")
			unm =  details['uname']		
			context = {
				'uname' : unm,
				'catg' : type,
				}
			dropindb(veremail,unm)
			email = details['email']
			context.update(csrf(request))
			code = rand(100000,999999)
			if flagem==0:
				if flagun == 0:
					uptodb(type,details,code)
					sub="OTP for registration in Blood_bank_management_website"
					body="This is a computer generated mail. Please do not reply back to this email.<br> The OTP code for your registration process is"+str(code)
					sendmail(email,sub,body)
					template = loader.get_template('confirm_register.html')
					return HttpResponse(template.render(context,request))
				else:
					HttpResponse("username already exixsts")
			else:
				return HttpResponse("email already exixsts")
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
			ret = HttpResponse(template.render(context,request))
#			ret.set_cookie('cookie_id_'+str(wry),'cookie_bbms_'+str(wry)+'_'+str(uname))
			return ret
		else:
			template = loader.get_template('login.html')
			context = { 'form':loginform }
			context['error'] = "Sorry. Invalid credentils."
			return HttpResponse(template.render(context,request))

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
		if request.session.has_key('sess_id_'+str(ctg)):
			del request.session['sess_id_'+str(ctg)]
	return HttpResponse("<p>You're logged out.</p>")

def fpassinit(request):
	if request.method == 'POST':
		context = {}
		context['email'] = request.POST.get('email')
		context['username'] = request.POST.get('uname')
		context['catg'] = request.POST.get('catg')
		print(context)
		if context['catg'] == "donor":
			fndb = Donor_reg
		elif context['catg'] == "hospital":
			fndb = Hospital_reg
		elif context['catg'] == "patient":
			fndb = Patient_reg

		ig = fndb.objects.filter(username = context['username'],email = context['email'])
		if ig:
			print('you are amazing')
			cd = rand(100000,999999)
			print(cd)
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
		print(catg)
		otp = int(request.POST.get('otp'))
		uname = request.POST.get('uname')
		print(otp,uname)
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
			print("succesfully changed password")
		return HttpResponseRedirect("/accounts/login")
	else:
		return HttpResponseRedirect("/")