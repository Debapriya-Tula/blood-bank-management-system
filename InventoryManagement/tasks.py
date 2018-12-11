from __future__ import absolute_import, unicode_literals
from .models import * 

from celery import task

bloodtypes=('A+','A-','B+','B-','O+','O-','AB+','AB-')

@task()													
def removeExpired():
	RB=RBCL.objects.all()
	Pl=Plasma.objects.all()
	P=Platelet.objects.all()
	for R in RB:
		print(R)
		if R.time_left<=0 and R.available:
			print("RBC time left is : "+str(R.time_left))
			R1=RBCLs.objects.get(blood_type=R.blood_type)
			R1.current_inv-=R.units
			R1.save()
			R.available = False
	for p in Pl:
		print(p)
		if p.time_left<=0 and R.available:
			print("p time left is : "+str(p.time_left))
			p1=Plasmas.objects.get(blood_type=p.blood_type)
			p1.current_inv-=p.units
			p1.save()
			p.available = False
	for R in P:
		print(R)
		if R.time_left<=0 and R.available:
			print("Platelet time left is : "+str(R.time_left))
			R1=Platelets.objects.get(id=1)
			R1.current_inv-=R.units
			R1.save()
			R.available = False


@task()
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
					add_stock(bloodtype,P.units)
					P.delete()
			elif FC.current_inv>10:
				FC.current_inv-=10
				R.current_inv+=10
				FC=frozen_cryo.objects.filter(blood_type=bloodtype).order_by('donate_date')
				count=10
				for F in FC:
					if F.units<count:
						P=frozen_cryo.objects.get(id=query.id)
						add_stock(bloodtype, P.units)
						P.delete()
						count-=units
					else:
						P=Platelet.objects.get(id=query.id)
						P.units-=count
						add_stock(bloodtype, P.units)
						P.save()
						break