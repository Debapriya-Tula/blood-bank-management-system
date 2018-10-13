from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

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
            'name': name,
            'email': email,
            'uname': uname,
            'dob':dob,
            'line1':line1,
            'line2':line2,
            'city':city,
            'postalcode':postalcode,
            'country':country,
        }
		template = loader.get_template('confirm_register.html')
		return HttpResponse(template.render(contect,request))
	else:
		template = loader.get_template('register.html')
		return HttpResponse(template.render())

def index(request):
	template = loader.get_template('index.html')
	return HttpResponse(template.render())
