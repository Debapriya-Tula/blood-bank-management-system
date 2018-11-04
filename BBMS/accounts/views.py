from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, RequestContext
from .models import donors, temp_db
from django.template.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
#from django.views.decorators.csrf import requires_csrf_token
from random import randint as rand
import hashlib

def md5hash(msg):
	rs = hashlib.md5(msg.encode())

def drop(name):
#	tp=temp_db.objects.raw("DELETE FROM accounts_temp_db WHERE uname='"+name+"';")
	temp_db.objects.filter(uname=name).delete()
#	tp=temp_db.objects.get(uname=name)
#	tp.DELETE

def get_data(column, value, datab):
	query = datab.objects.get(uname=value)
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

def confirm_register(request):
	if request.method == "POST":
		code = request.POST.get('code')
		uname = request.POST.get('username') 
		try:
			cd=get_data('code',uname,temp_db)
			if int(cd) == int(code):
				return HttpResponse("<h1>Successful Sign Up "+str(uname)+"</h1>")
			else:
				return HttpResponse("<h1>OTP didint match</h1>")
		except Exception as e:
			print(e)
			return HttpResponse("<h1>Internal server problem.<br></h1><p> Please give us a little while.</p>")

#@requires_csrf_token
def register(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		uname = request.POST.get('uname')
		email = request.POST.get('email')
		passwd = request.POST.get('passwd')
		dob = request.POST.get('dob')
		line1 = request.POST.get('line1')
		line2 = request.POST.get('line2')
		city = request.POST.get('city')
		postalcode = request.POST.get('postalcode')
		country = request.POST.get('country')
		context = {
			'uname': uname,
		}
#		context.update(csrf(request))
		drop(uname)
		code = rand(100000,999999)
		tp = temp_db(uname=uname,code=code)
		tp.save()
		new_entry = donors(name=name,email=email,uname=uname,passwd=passwd,dob=dob,line1=line1,line2=line2,postalcode=postalcode,city=city,country=country,email_verified=0)
		new_entry.save()
		sub="OTP for registration in Blood_bank_management_website"
		body="This is a computer generated mail. Please do not reply back to this email.<br> The OTP code for your registration process is"+str(code)
		sendmail(email,sub,code)
		template = loader.get_template('confirm_register.html')
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
		uname=request.POST.get('uname')
		password=request.POST.get('password')
#		p=donors.objects.raw('SELECT * FROM accounts_donors WHERE uname="'+str(uname)+'" and passwd="'+str(password)+'"')
#		try:
		p=donors.objects.get(uname=uname,passwd=password)
		print(p)
		context = {"uname":uname}
		try:
			print(request.session['sess_id'])
			if request.session['sess_id']=='bbms_'+str(uname):
				print("working")
				return HttpResponse(template.render(context,request))
		except:
			template = loader.get_template('aflogin.html')
			request.session['sess_id']='bbms_'+str(uname)
			return HttpResponse(template.render(context,request))

	else:
		if request.session.has_key('sess_id'):
			template = loader.get_template('aflogin.html')
			return HttpResponse(template.render())
		else:
			template = loader.get_template('login.html')
			return HttpResponse(template.render())

def logout(request):
	try:
		del request.session['sess_id']
	except:
		pass
	return HttpResponse("<p>You're logged out.</p>")