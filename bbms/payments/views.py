from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
import stripe
from .models import *
from .forms import *
from django.conf import settings
from django.utils import timezone
import random
import string
from datetime import date
import datetime
from InventoryManagement.models import *
from django.contrib import messages
 
stripe.api_key = settings.STRIPE_SECRET_KEY
total = 0

def home(request):
	pop=0
	context={'pop':pop}
	return render(request, 'payments/home.html', context)

def buy_blood(request):
	if request.method == "POST":
		print("submitted successfully")
		if request.session.has_key('sess_id_user'):
			uname = request.session['sess_id_user'].lstrip('bbms_user')
			pt = Patient_reg.objects.get(username=uname)
			form = blood_buyform(request.POST, request.FILES)
			if form.is_valid():
				blood_type = form.cleaned_data['blood_type']
				units = form.cleaned_data['units']
				prescription = form.cleaned_data['prescription']
				P=patientDetail(username=pt, blood_type=blood_type, units=units, prescription=prescription)
				P.save()
				messages.success(request, f'Your order has been placed. You will soon be notified via E-mail')
				return redirect('processed')
	form = blood_buyform()

	context={
		'form':form,
	}
	return render(request, "payments/buy_blood.html", context)

def bblood(request):
	if request.method == "POST":
		print("submitted successfully")
		if request.session.has_key('sess_id_user'):
			uname = request.session['sess_id_user'].lstrip('bbms_user')
			pt = Patient_reg.objects.get(username=uname)
			blood_type = request.POST.get('bgroup')
			units = request.POST.get('units')
			prescription = request.POST.get('picture')
			P=patientDetail(username=pt, blood_type=blood_type, units=units, prescription=prescription)
			P.save()
			messages.success(request, f'Your order has been placed. You will soon be notified via E-mail')
			return redirect('processed')
	

def donate_blood(request):
	form = blood_donateform()
	#form1 = disease()
	if request.method == "POST":
		if request.session.has_key('sess_id_user'):
			uname = request.session['sess_id_user'].lstrip('bbms_user')
			pt = Donor_reg.objects.get(username=uname)
			form = blood_donateform(request.POST)
			#form1 = disease(request.POST)
			if form.is_valid(): #and form1.is_valid():
				date = form.cleaned_data['date']
				print()
				print()
				print("working")
#				print(pt,date)
				print()
				print()
				DD = donorDetail(username=pt, date=date)
				DD.save()
				'''Asthma = form.cleaned_data['Asthma']
																Cancer = form.cleaned_data['Cancer']
																Cardiac_Disease = form.cleaned_data['Cardiac_Disease']
																Diabetes = form.cleaned_data['Diabetes']
																Hypertension = form.cleaned_data['Hypertension']
																Psychiatric_Disorder = form.cleaned_data['Psychiatric_Disorder']
																Epilepsy = form.cleaned_data['Epilepsy']'''
				'''DI = Diseases(donor=DD, Asthma=Asthma, Cancer=Cancer, Cardiac_Disease=Cardiac_Disease, Diabetes=Diabetes, Hypertension=Hypertension,Pyschiatric_Disorder=Psychiatric_Disorder, Epilepsy=Epilepsy)'''
				messages.success(request, f'We appreciate your donation. You will soon be notified via E-mail')
				return redirect('processed')

	context={
		'form':form,
		#'form1':form1,
	}
	return render(request, "payments/donate_blood.html", context)

def hospital_blood(request):
	form = blood_hospitalform()
	if request.method == "POST":
		if request.session.has_key('sess_id_user'):
			print("working")
			uname = request.session['sess_id_user'].lstrip('bbms_hospital')
			print(uname)
			pt = Hospital_reg.objects.get(username=uname)
			print('working',uname)
			form = blood_hospitalform(request.POST)
			if form.is_valid():
				blood_type = form.cleaned_data['blood_type']
				units = form.cleaned_data['units']
				component = form.cleaned_data['component']
				BH = hospitalDetail(username=pt, blood_type=blood_type, units=units, component=component)
				BH.save()
				messages.success(request, f'Your order has been placed. You will soon be notified via E-mail')
				return redirect('processed')

	context={
		'form':form,
		

	}
	return render(request, "payments/hospital_blood.html", context)

def processed(request):
	pop=0
	context={
		'pop':pop
	}
	return render(request,"payments/processed.html",context)

def authenticate(request):
	form = admin_fillform()
	if request.method == 'POST':
		form = admin_fillform(request.POST)
		if form.is_valid():
			form.save()
		return redirect('final')



	context = {'form':form,}
	return render(request,"payments/authenticate.html", context) 


def generate_order_id():
    date_str = date.today().strftime('%d%m%Y')[2:] + str(datetime.datetime.now().second)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    return date_str + rand_str

def get_existing_order():
	customer_order = patientDetail.objects.filter(order_complete=False)
	return customer_order

def order_component():
	customer_order = finalorder.objects.filter(order_complete=False)
	return customer_order

'''def get_existing_order_price():
	customer_order = order_component()
	OR = get_existing_order()
	price=[]
	bloodtype=[]
	for O in OR:
		bloodtype.append(O.blood_type)
	count=0
	for order in customer_order:
		component = order.component
		if component == 'RBCLs':
			R=RBCLs.objects.get(blood_type=bloodtype[count])
		elif component == 'Plasmas':
			R=Plasmas.objects.get(blood_type=bloodtype[count][:-1])
		else:
			R=Platelets.objects.get(id=1)
		price.append(R.price)
		count+=1
	return price'''

def final(request):
	items=get_existing_order()
	items2=order_component()
	#price=get_existing_order_price()

	context = {
		'items':items,
		'items2':items2,
	}
	return render(request, 'payments/finalize.html', context)



def checkout(request):
	total=0
	publishKey=settings.STRIPE_PUBLISHABLE_KEY
	orders = get_existing_order()
	#price = get_existing_order_price()
	count=0
	for order in orders:
		total+=order.units
	if request.method == 'POST':
		token = request.POST.get('stripeToken', False)
		if token:
			try:
				charge = stripe.Charge.create(
					amount = total*500/70,
					currency = 'usd',
					description = 'CHarge Example',
					source = token,
				)
				return redirect('pay')
				'''return redirect(reverse('update', 
																			kwargs={
																				'token':token
																	}))'''
			
			except:
				pass
	
	total=0
	for order in orders:
		total+=order.units
	amount=(total)*500/70
	context = {
			'order':orders,
			'amount':amount,
			'STRIPE_PUBLISHABLE_KEY': publishKey,
	}
	return render(request, 'payments/checkout.html', context)


def update_transaction(request, token):
	
	total=0
	orders = get_existing_order()
	for order in orders:
		order.order_complete=True
		order.date_ordered=timezone.now
		total+=order.units
		order.save()
	order_id=generate_order_id()
	amount=total*500

	transaction = Transaction(token = token,
						order_id = order_id,
						amount = amount,
						success = True
						)
	transaction.save()
	print(transaction)

	messages.info(request, "Thank You for the Purchase")
	return render(request, 'payments/update.html')






