
from django.http import HttpResponse,HttpResponseRedirect
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
from InventoryManagement.views import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from accounts.models import *
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from patient_portal.models import *
from donor_portal.models import *
from hospital_portal.models import *
from django.core.mail import send_mail
from accounts.views import sendmail

stripe.api_key = settings.STRIPE_SECRET_KEY
total = 0
token = 0

def home(request):
	pop=0
	context={'pop':pop}
	return render(request, 'payments/home.html', context)


def processed(request):
	pop=0
	context={
		'pop':pop
	}
	return render(request,"payments/processed.html",context)

@staff_member_required
def listOrders(request):
	querylist=DataBase.objects.filter(auth_complete=False)
	if querylist:
		context={'items1':querylist}
		return render(request, 'payments/list_user_orders.html', context)  
	else:
		context={'items1':0}
		return render(request, 'payments/no_one_left.html', context)

@staff_member_required
def authenticate(request, num):
	obj=DataBase.objects.get(id=num)
	form = admin_fillform()
	if request.method == 'POST':
		form = request.POST
		
		obj1=finalorder.objects.create(order=obj, component=form['component'])
		obj.auth_complete=True
		#email = obj.user_name.email
		#sub = "Confirmed your order for requesting blood"
		#body = "We got a request from your account that you need "+str(obj.blood_group)+" of "+str(obj.blood_units)+" units. Your prescription is authenticated.<br>Proceed to checkout. <a href='127.0.0.1:8000/payments/finalize/'>Click here</a>"
		#sendmail(email,sub,body)
		obj.save()
		return redirect('final')
		#return HttpResponse("Hello")



	context = {'form':form, 'obj':obj}
	return render(request,"payments/authenticate.html", context) 

@staff_member_required
def donorList(request):
	item1=[]
	querylist=Donor_DataBase.objects.filter(donation_complete=False)
	if querylist:
		for query in querylist:
			dondet=Donor_details.objects.get(userd=query.user_name)
			bloodtype=dondet.blood_group
			obd = {'id': query.id, 'blood_group': bloodtype, 'don_or_sell':query.don_or_sell, 'user':query.user_name.username}
			item1.append(obd)
		context={'items1':item1}
		print(item1)
		return render(request, 'payments/list_donors.html', context)
	else:
		context={'items1':0}
		return render(request, 'payments/no_one_left.html', context)

@staff_member_required
def authdonor(request,num):
	print('entering')
	obj=Donor_DataBase.objects.get(id=num)
	form=admin_donorform()
	if request.method == 'POST':
		form = request.POST
		print('not received',obj, form['units'])
		obj1=finaldonation.objects.create(donation=obj, units=int(form['units']))
		obj.donation_complete=True
		dondet=Donor_details.objects.get(userd=obj.user_name)
		bloodtype=dondet.blood_group
		print(bloodtype)
		add_Stock(bloodtype,int(form['units']))
		obj.save()
		return redirect('home')

	context = {'form':form}
	return render(request,"payments/authenticate_donor.html", context)



def generate_order_id():
    date_str = date.today().strftime('%d%m%Y')[2:] + str(datetime.datetime.now().second)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    return date_str + rand_str

def get_existing_order_patient(request):
	if request.session.has_key('sess_id_user'):
		un = str(request.session['sess_id_user']).split('_')[2]
		user = Patient_reg.objects.get(username = un)
		customer_order = DataBase.objects.filter(user_name=user,auth_complete=True,order_complete=False)
		return customer_order
	else:
		return HttpResponseRedirect('/accounts/login')

def get_existing_order_hospital(request):
	if request.session.has_key('sess_id_user'):
		un = str(request.session['sess_id_user']).split('_')[2]
		user = Hospital_reg.objects.get(username = un)
		customer_order = Hospital_DataBase.objects.filter(hosp_id=user,order_complete=False)
		return customer_order
	else:
		return HttpResponseRedirect('/accounts/login')


def order_component():
	customer_order = finalorder.objects.filter(order_complete=False)
	return customer_order

def get_price(component, bloodtype):
	print(component)
	if component == 'RBCLs':
		Rb=RBCLs.objects.get(blood_type=bloodtype)
		return Rb.price
	elif component == 'Plasmas':
		Pl=Plasmas.objects.get(blood_type=bloodtype[:-1])
		return Pl.price
	elif component == 'Platelets':
		P=Platelets.objects.get(id=1)
		return P.price

def cantdonate(request):
	pop=0
	context={
		'pop':pop
	}
	return render(request,"payments/cant_donate.html",context)


def get_total(items):
	for item in items:
		ob = finalorder.objects.get(order=item)
		price=get_price(ob.component,ob.order.blood_group)
		total=price*ob.order.blood_units
	return total

def final_patient(request):
	item1=[]
	flag=0
	items=get_existing_order_patient(request)
	if items:
		for item in items:
			ob = finalorder.objects.get(order=item)
			check = is_enough_stock(ob.component,ob.order.blood_group,ob.order.blood_units)
			print('working',item,ob)
			if check:
				price=get_price(ob.component,ob.order.blood_group)
				total=price*ob.order.blood_units
				obd = {'blood_group': ob.order.blood_group,'blood_units': ob.order.blood_units, 'component':ob.component, 'price':price, 'total':total}
				item1.append(obd)
				print(obd)
			else:
				flag=1
				break

		#price=get_existing_order_price()
	if flag:
		reason = "We're sorry but we don't have enough stock right now. You can try other bloodbanks near us."
		context = {'reason':reason}
		return render(request, 'payments/try_someplace_else.html', context)


	else:
		context = {'items':item1}
		return render(request, 'payments/finalize_hospitals.html', context)
	
'''def delete_order_patient(request, num):
	obj=DataBase.objects.get(id=num)
	obj.delete()
	return redirect('final')


def delete_order_hospital(request, num):
	obj=Hopital_DataBase.objects.get(id=num)
	obj.delete()
	return redirect('final_hospital')'''

def processedhospital(request):
	pop=0
	context={
		'pop':pop
	}
	return render(request,"payments/processed_hospital.html",context)

def final_hospital(request):
	item1=[]
	flag=0
	items=get_existing_order_hospital(request)
	for item in items:
		ob = Hospital_DataBase.objects.get(order=item)
		check = is_enough_stock(ob.blood_component,ob.blood_group,ob.blood_units)
		if check:
			price=get_price(ob.blood_component,ob.blood_group)
			total=price*ob.order.blood_units
			obd = {'blood_group': ob.blood_group,'blood_units': ob.blood_units, 'component':ob.component, 'price':price, 'total':total}
			item1.append(obd)
			print(obd)
		else:
			flag=1
			break
	#price=get_existing_order_price()
	
	if flag:
		reason = "We're sorry but we don't have enough stock right now. You can try other bloodbanks near us."
		context = {'reason':reason}
		return render(request, 'payments/try_someplace_else.html', context)
	else:
		context = {'items':item1}
		return render(request, 'payments/finalize_hospitals.html', context)

def checkout(request):
	if request.method == 'POST':
		token = request.POST['token_try']
		print(token)
		items=get_existing_order_patient(request)
		total = get_total(items)
#		charge = stripe.Charge.create(
#			amount = total/70,
#			currency = 'usd',
#			description = 'CHarge Example',
#			source = token,
#		)
		
	orders = get_existing_order_patient(request)
	for order in orders:
		order.order_complete=True
		#order.date_ordered=timezone.now
		FO=finalorder.objects.get(order=order)
		deletestock(FO.component,order.blood_group,order.blood_units)
	total=get_total(orders)


	order_id=generate_order_id()

	transaction = Transaction(token = token,
						order_id = order_id,
						amount = total,
						success = True
						)
	transaction.save()
	print(transaction)

	
	return render(request, 'payments/update.html')

def checkout1(request):
	publishKey=settings.STRIPE_PUBLISHABLE_KEY
	total=0
	if request.method == 'POST':
		items=get_existing_order_patient(request)
		total = get_total(items)

	amount = total/70
	context = {
			'amount':amount,
			'STRIPE_PUBLISHABLE_KEY': publishKey,
	}
	return render(request, 'payments/checkout.html', context)







'''if request.method == 'POST':
		try:
			token = request.POST
			token = token['stripeToken']
			charge = stripe.Charge.create(
				amount = total*500/70,
				currency = 'usd',
				description = 'CHarge Example',
				source = token,
			)
			return redirect('pay')
			return redirect(reverse('update', kwargs={'token':token}))
		
		except:
			#message.info(request, "Your card has been declined.")
			pass'''