from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from accounts.models import Hospital_reg
from django.contrib import messages
from accounts.models import veremail
from accounts.views import confirm_register, dropindb, sendmail
from random import randint as rand
# Create your views here.


def home(request):
    return render(request, 'home.html')

def hospital(request):
    saved = False
    if request.method == 'POST':
        if request.session.has_key('sess_id_hospital'):
            un = str(request.session['sess_id_hospital']).split('_')[2]
            user = Hospital_reg.objects.get(username = un)
            if user.email_verified:
                details = request.POST
                ob = Hospital_DataBase.objects.Create(hosp_id = user, blood_units=details['blood_units'], blood_group=details['blood_group'], blood_component=details['blood_component'])
                email = user.email
                username = user.username
                tell_admin(email,username)
                messages.success(request, f'Your order has been placed. You will soon be notified via E-mail')
                return redirect('processed_hospital')


            else:
                dropindb(vermail, un)
                code = rand(100000, 999999)
                ef = veremail.objects.create(ab=int(code), uname=un)
                #em_verify(email,code)
                context = {'uname':un, 'catg': 'hospital'}
        else:
            return HttpResponseRedirect('/accounts/login') 
    else:
        hospital_form = Hospital_Form()
        return render(request, 'hospital.html', {'form': hospital_form})






# Create your views here.


def tell_admin(email,username):
    message = "A new hospital, {0} with mail-id {2} has sent details".format(username,email)
            #Send the mail to the admin who will check for detail authentication
    sendmail(email, "Hospital requested for blood",message)

            #Send a whatsapp message to the user
    #from .whatsapp import fill_details
    #fill_details(fm.user_no)
    #print("Working")

            #submit = Person.objects.order_by('-id')[0]
            #print(str(form))
    #return HttpResponse("The task is done")
    




