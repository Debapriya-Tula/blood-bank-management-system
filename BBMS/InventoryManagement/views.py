from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.utils import *
from django.utils.timezone import utc
from django.contrib import messages

def home(request):
	return render(request, 'index.html')

def display_RBCL(request):
	items = RBCL.objects.all()
	items1 = RBCLs.objects.all()
	context = {
		'items1':items1,

	}

	return render(request, 'index.html', context)

def display_Plasma(request):
	items = Plasma.objects.all()
	items1 = Plasmas.objects.all()
	context = {
		'items1':items1,

	}
	return render(request, 'index.html', context)


def display_Platelets(request):
	items = Platelet.objects.all()
	items1 = Platelets.objects.all()
	context = {
		'items1':items1,

	}
	return render(request, 'index.html', context)

def add_stock(request):
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
			if R.current_inv>60 and Pl.current_inv>40 and P.current_inv>40:
				FC=frozen_cryo(blood_type=bloodtype, units=units)
				FC.save() 
				FC=Frozen_Cryos.objects.get(blood_type=bloodtype)
				FC.current_inv+=units
				FC.save()
#If not, then the blood is divided and stored			
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
			messages.success(request, f'Stock successfully added.')
			return redirect('inv-RBC')
	context = {
		"form" : form
	}
	return render(request, "add_stock.html", context)

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
				if RB.current_inv>units:
					RB.current_inv-=units
					RB.save()
					queryset = RBCL.objects.filter(blood_type=bloodtype).order_by('donate_date')
					unit=units
					for query in queryset:
						if query.units <= unit:
							RB=RBCL.objects.get(id=query.id)
							unit-=query.units
							RB.delete()
						else:
							RB=RBCL.objects.get(id=query.id)
							RB.units-=unit
							RB.save()
							break
					messages.success(request, f'Delete Successful')
					return redirect('inv-RBC')
				else:
					messages.error(request, f'Inventory does not have enough stock. The delete cannot happen')
					return redirect('inv-RBC')
			if component == 'Plasma':
				Pl=Plasmas.objects.get(blood_type=bloodtype[:-1])
				if Pl.current_inv>units:
					Pl.current_inv-=units
					Pl.save()
					queryset = Plasma.objects.filter(blood_type=bloodtype[:-1]).order_by('donate_date')
					unit=units
					for query in queryset:
						if query.units <= unit:
							Pl=Plasma.objects.get(id=query.id)
							unit-=query.units
							Pl.delete()						
						else:
							Pl=Plasma.objects.get(id=query.id)
							Pl.units-=unit
							Pl.save()
							break
					messages.success(request, f'Delete Successful')
					return redirect('inv-RBC')
				else:
					messages.error(request, f'Inventory does not have enough stock. The delete cannot happen')
					return redirect('inv-RBC')


			if component == 'Platelet':
				P=Platelets.objects.get(id=1)
				if P.current_inv>units:
					P.current_inv-=units
					P.save()
					queryset = Platelet.objects.order_by('donate_date')
					unit=units
					for query in queryset:
						if query.units <= unit:
							P=Platelet.objects.get(id=query.id)
							unit-=query.units
							P.delete()
						else:
							P=Platelet.objects.get(id=query.id)
							P.units-=unit
							P.save()
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
	return render(request, "delete_stock.html", context)


def calculate_time(objectlist, timenow):
	for obj in objectlist:
		timediff = timenow - obj.donate_date
		timediff = timediff.total_seconds()/3600
		#tim=format_timedelta(timediff)
		obj.time_passed = int(obj.expiry-timediff)


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

def display_unitexpiration(request):
	count = [0,0,0]
	now = timezone.now()
	items1=RBCL.objects.all()
	calculate_time(items1, now)
	for item in items1:
		count[0]+=item.units
	items2=Plasma.objects.all()
	calculate_time(items2, now)
	for item in items2:
		count[1]+=item.units
	items3=Platelet.objects.all()
	calculate_time(items3, now)
	for item in items3:
		count[2]+=item.units

	context = {
		'items1':items1,
		'items2':items2,
		'items3':items3,
		'count1':count[0],
		'count2':count[1],
		'count3':count[2],
	}
	return render(request, "unit_account.html", context)

'''def thaw_blood(bloodtypes):
	for bloodtype in bloodtypes:
		R=RBCLs.objects.get(blood_type=bloodtype)
		FC=Frozen_Cryos.objects.get(blood_type=bloodtype)
		if R.current_inv<10:
			if FC.current_inv>0 and FC.current_inv<10:
				FC.current_inv=0
				FC=frozen_cryo.objects.filter(blood_type=bloodtype)
				for F in FC:
					P=frozen_cryo.objects.get(id=query.id)
					R.current_inv+=P.units
					RB = RBCL(blood_type=bloodtype, units=P.units)
					P.delete()
			elif FC.current_inv>10:
				FC.current_inv-=10
				R.current_inv+=10
				FC=frozen_cryo.objects.filter(blood_type=bloodtype).order_by('donate_date')
				count=10
				for F in FC:
					if F.units<count:
						P=frozen_cryo.objects.get(id=query.id)
						RB = RBCL(blood_type=bloodtype, units=P.units)
						P.delete()
						count-=units
					else:
						P=Platelet.objects.get(id=query.id)
						P.units-=count
						RB = RBCL(blood_type=bloodtype, units=count)
						P.save()
						break
'''


	


