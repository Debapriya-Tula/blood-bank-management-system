from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.utils import *
from django.utils.timezone import utc
from django.contrib import messages
from .tasks import *
from django.contrib.admin.views.decorators import staff_member_required

bloodtypes=('A+','A-','B+','B-','O+','O-','AB+','AB-')

@staff_member_required
def display_home(request):
	return render(request, 'InventoryManagement/home.html')

@staff_member_required
def display_RBCL(request):
	items = RBCL.objects.all()
	items1 = RBCLs.objects.all()
	removeExpired()
	thaw_blood(bloodtypes)
	context = {
		'items1':items1,

	}

	return render(request, 'InventoryManagement/index.html', context)

@staff_member_required
def display_Plasma(request):
	items = Plasma.objects.all()
	items1 = Plasmas.objects.all()
	context = {
		'items1':items1,

	}
	return render(request, 'InventoryManagement/index.html', context)

@staff_member_required
def display_Platelets(request):
	items = Platelet.objects.all()
	items1 = Platelets.objects.all()
	context = {
		'items1':items1,

	}
	return render(request, 'InventoryManagement/index.html', context)

@staff_member_required
def display_Frozen(request):
	items1 = Frozen_Cryos.objects.all()
	context = {
		'items1':items1,

	}
	return render(request, 'InventoryManagement/index.html', context)

@staff_member_required
def addstock(request):
	form = AddStock()
	if request.method == "POST":
		form = AddStock(request.POST)
		if form.is_valid():
			units = form.cleaned_data['units']
			bloodtype = form.cleaned_data['blood_type']
			R=RBCLs.objects.get(blood_type=bloodtype)
			Pl=Plasmas.objects.get(blood_type=bloodtype[:-1])
			P=Platelets.objects.get(id=1)
#If there is enough stock of all components, then the blood is frozen and kept in a different stprage place.
			add_Stock(bloodtype, units)
			messages.success(request, f'Stock successfully added.')
			return redirect('inv-RBC')
	context = {
		"form" : form
	}
	return render(request, "InventoryManagement/add_stock.html", context)


def add_Stock(bloodtype,units):
	print(bloodtype)
	R=RBCLs.objects.get(blood_type=bloodtype)
	Pl=Plasmas.objects.get(blood_type=bloodtype[:-1])
	P=Platelets.objects.get(id=1)
	if R.current_inv>60 and Pl.current_inv>40 and P.current_inv>40:
		FC=frozen_cryo(blood_type=bloodtype, units=units)
		FC.save() 
		FC=Frozen_Cryos.objects.get(blood_type=bloodtype)
		FC.current_inv+=units
		FC.save()
	else:
		RB = RBCL(blood_type=bloodtype, units=units)
		RB.save()
		RB=RBCLs.objects.get(blood_type=bloodtype)
		RB.current_inv+=units
		RB.save()
		Pl = Plasma(blood_type=bloodtype[:-1], units=units)
		Pl.save()
		Pl=Plasmas.objects.get(blood_type=bloodtype[:-1])
		Pl.current_inv+=units
		Pl.save()
		P = Platelet(units=units)
		P.save()
		P=Platelets.objects.get(id=1)
		P.current_inv+=units
		P.save()
		

def is_enough_stock(component, bloodtype, units):
	RB=RBCLs.objects.get(blood_type=bloodtype)
	Pl=Plasmas.objects.get(blood_type=bloodtype[:-1])
	P=Platelets.objects.get(id=1)
	if component=='RBCLs':
		if RB.current_inv<units:
			return False
		else:
			return True
	if component=='Plasmas':
		if Pl.current_inv<units:
			return False
		else:
			return True
	if component=='Platelets':
		if P.current_inv<units:
			return False
		else:
			return True


def deletestock(component, bloodtype, units):
	if component=='RBCLs':
		RB=RBCLs.objects.get(blood_type=bloodtype)
		if RB.current_inv>=units:
			RB.current_inv-=units
			RB.save()
			queryset = RBCL.objects.filter(blood_type=bloodtype, available=True).order_by('donate_date')
			unit=units
			for query in queryset:
				if query.units <= unit:
					RB=RBCL.objects.get(id=query.id)
					unit-=query.units
					RB.available = False
					RB.time_left = 0
					RB.save()
				else:
					RB=RBCL.objects.get(id=query.id)
					RB.units-=unit
					RB.save()
					RB1=RBCL(blood_type=RB.blood_type, units=units, donate_date=RB.donate_date, time_left=0.0, available=False)
					RB1.save()
					break

	if component == 'Plasmas':
		Pl=Plasmas.objects.get(blood_type=bloodtype[:-1])
		if Pl.current_inv>=units:
			Pl.current_inv-=units
			Pl.save()
			queryset = Plasma.objects.filter(blood_type=bloodtype[:-1], available=True).order_by('donate_date')
			unit=units
			for query in queryset:
				if query.units <= unit:
					Pl=Plasma.objects.get(id=query.id)
					unit-=query.units
					Pl.available = False
					Pl.time_left = 0
					Pl.save()						
				else:
					Pl=Plasma.objects.get(id=query.id)
					Pl.units-=unit
					Pl.save()
					Pl1=Plasma(blood_type=Pl.blood_type, units=units, donate_date=Pl.donate_date, time_left=0.0, available=False)
					Pl1.save()
					break

	if component == 'Platelets':
		P=Platelets.objects.get(id=1)
		if P.current_inv>=units:
			P.current_inv-=units
			P.save()
			queryset = Platelet.objects.filter(available=True).order_by('donate_date')
			unit=units
			for query in queryset:
				if query.units <= unit:
					P=Platelet.objects.get(id=query.id)
					unit-=query.units
					P.available = False
					P.time_left = 0
					P.save()
				else:
					P=Platelet.objects.get(id=query.id)
					P.units-=unit
					P.save()
					Pl1=Platelet(units=units, donate_date=P.donate_date, time_left=0.0, available=False)
					Pl1.save()
					break




@staff_member_required
def delete_stock(request):
	form=DeleteStock()
	if request.method == "POST":
		form = DeleteStock(request.POST)
		if form.is_valid():
			units = form.cleaned_data['units']
			bloodtype = form.cleaned_data['blood_type']
			component = form.cleaned_data['component']
#Checks in all components, and deletes the corresponding unit from the inventory and also deducts the units from objects of individual inventory according to the oldest			
			if component == 'RBCL':
				RB=RBCLs.objects.get(blood_type=bloodtype)
				if RB.current_inv>=units:
					RB.current_inv-=units
					RB.save()
					queryset = RBCL.objects.filter(blood_type=bloodtype, available=True).order_by('donate_date')
					unit=units
					for query in queryset:
						if query.units <= unit:
							RB=RBCL.objects.get(id=query.id)
							unit-=query.units
							RB.available = False
							RB.time_left = 0
							RB.save()
						else:
							RB=RBCL.objects.get(id=query.id)
							RB.units-=unit
							RB.save()
							RB1=RBCL(blood_type=RB.blood_type, units=units, donate_date=RB.donate_date, time_left=0.0, available=False)
							RB1.save()
							break
					messages.success(request, f'Delete Successful')
					return redirect('inv-RBC')
				else:
					messages.error(request, f'Inventory does not have enough stock. The delete cannot happen')
					return redirect('inv-RBC')
			if component == 'Plasma':
				Pl=Plasmas.objects.get(blood_type=bloodtype[:-1])
				if Pl.current_inv>=units:
					Pl.current_inv-=units
					Pl.save()
					queryset = Plasma.objects.filter(blood_type=bloodtype[:-1], available=True).order_by('donate_date')
					unit=units
					for query in queryset:
						if query.units <= unit:
							Pl=Plasma.objects.get(id=query.id)
							unit-=query.units
							Pl.available = False
							Pl.time_left = 0
							Pl.save()						
						else:
							Pl=Plasma.objects.get(id=query.id)
							Pl.units-=unit
							Pl.save()
							Pl1=Plasma(blood_type=Pl.blood_type, units=units, donate_date=Pl.donate_date, time_left=0.0, available=False)
							Pl1.save()
							break
					messages.success(request, f'Delete Successful')
					return redirect('inv-RBC')
				else:
					messages.error(request, f'Inventory does not have enough stock. The delete cannot happen')
					return redirect('inv-RBC')


			if component == 'Platelet':
				P=Platelets.objects.get(id=1)
				if P.current_inv>=units:
					P.current_inv-=units
					P.save()
					queryset = Platelet.objects.filter(available=True).order_by('donate_date')
					unit=units
					for query in queryset:
						if query.units <= unit:
							P=Platelet.objects.get(id=query.id)
							unit-=query.units
							P.available = False
							P.time_left = 0
							P.save()
						else:
							P=Platelet.objects.get(id=query.id)
							P.units-=unit
							P.save()
							Pl1=Platelet(units=units, donate_date=P.donate_date, time_left=0.0, available=False)
							Pl1.save()
							break
					messages.success(request, f'Delete Successful')
					return redirect('inv-RBC')
				else:
					messages.error(request, f'Inventory does not have enough stock. The delete cannot happen')
					return redirect('inv-RBC')
			return redirect('inv-RBC')
	context = {
		"form" : form
	}
	return render(request, "InventoryManagement/delete_stock.html", context)


def calculate_time(objectlist, timenow):
	for obj in objectlist:
		timediff = timenow - obj.donate_date
		timediff = timediff.total_seconds()/3600
		#tim=format_timedelta(timediff)
		obj.time_left = int(obj.expiry-timediff)


'''def format_timedelta(td):
    hours, remainder = divmod(td.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    hours, minutes, seconds = int(hours), int(minutes), int(seconds)
    if hours < 10:
        hours = '0%s' % int(hours)
    if minutes < 10:
        minutes = '0%s' % minutes
    if seconds < 10:
        seconds = '0%s' % seconds
    return '%s:%s:%s' % (hours, minutes, seconds)'''

@staff_member_required
def display_unitexpiration(request):
	count = [0,0,0]
	now = timezone.now()
	items1=RBCL.objects.all()
	calculate_time(items1, now)
	for item in items1:
		if item.available:
			count[0]+=item.units
	items2=Plasma.objects.all()
	calculate_time(items2, now)
	for item in items2:
		if item.available:
			count[1]+=item.units
	items3=Platelet.objects.all()
	calculate_time(items3, now)
	for item in items3:
		if item.available:
			count[2]+=item.units

	context = {
		'items1':items1,
		'items2':items2,
		'items3':items3,
		'count1':count[0],
		'count2':count[1],
		'count3':count[2],
	}
	return render(request, "InventoryManagement/unit_account.html", context)



def thaw_blood(bloodtypes):
	for bloodtype in bloodtypes:
		R=RBCLs.objects.get(blood_type=bloodtype)
		Pl=Plasmas.objects.get(blood_type=bloodtype[:-1])
		P=Platelets.objects.get(id=1)
		FC=Frozen_Cryos.objects.get(blood_type=bloodtype)
		if R.current_inv<10 or Pl.current_inv<10 or P.current_inv<10:
			if FC.current_inv>0 and FC.current_inv<10:
				FC.current_inv=0
				FC=frozen_cryo.objects.filter(blood_type=bloodtype)
				for F in FC:
					P=frozen_cryo.objects.get(id=F.id)
					add_Stock(bloodtype,P.units)
					P.delete()
			elif FC.current_inv>10:
				FC.current_inv-=10
				R.current_inv+=10
				FC=frozen_cryo.objects.filter(blood_type=bloodtype).order_by('donate_date')
				count=10
				for F in FC:
					if F.units<count:
						P=frozen_cryo.objects.get(id=query.id)
						add_Stock(bloodtype, P.units)
						P.delete()
						count-=units
					else:
						P=Platelet.objects.get(id=query.id)
						P.units-=count
						add_Stock(bloodtype, P.units)
						P.save()
						break



	


