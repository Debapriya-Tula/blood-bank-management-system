from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from .models import *
from accounts.models import Patient_reg, Patient_details
from .forms import *
from django.contrib import messages
from accounts.models import veremail
from accounts.views import confirm_register, dropindb
from random import randint as rand

# Create your views here.


def home(request):
    return render(request, 'home.html')


def patient(request):
    saved = False
    if request.method == 'POST':
        if request.session.has_key('sess_id_user'):
            un = str(request.session['sess_id_user']).split('_')[2]
            user = Patient_reg.objects.get(username = un)
            if user.email_verified:
                details = request.POST
                picture = request.FILES
                ob = DataBase.objects.create(user_name=user, picture=picture['picture'], blood_units=details['blood_units'], blood_group=details['blood_group'], to_time=details['to_time'], from_time=details['from_time'])
                PD = Patient_details.objects.get(userp=user)
                ph_no=PD.ph_no
                email=user.email
                fname=user.first_name
                lname=user.last_name
                print(PD)
                tell_admin(email,fname,lname,ph_no)
                messages.success(request, f'Your order has been placed. You will soon be notified via E-mail')
                return redirect('processed')


            else:
                dropindb(vermail, un)
                code = rand(100000, 999999)
                ef = veremail.objects.create(ab=int(code), uname=un)
                #em_verify(email, code)
                context = {'uname':un, 'catg': 'user'}
                return render(request, 'confirm_register.html', context)
        else:
            return HttpResponseRedirect('/accounts/login')
    else:
        profile_form = Profile_Form()
        return render(request, 'patient.html', {'form': profile_form})


from django.core.mail import send_mail
from django.conf import settings


def send_email(message,recipient_list):
    subject = 'New user'
    email_from = settings.EMAIL_HOST_USER
    send_mail( subject, message, email_from, recipient_list)
    #return HttpResponse("I am done")


def tell_admin(email,fname,lname,ph_no):
    message = "A new User, {0} {1} with mail-id {2} has sent details".format(fname,lname,email)
    recipient_list = [str(email)]

            #Send the mail to the admin who will check for detail authentication
    send_email(message,recipient_list)

            #Send a whatsapp message to the user
    #from .whatsapp import fill_details
    #fill_details(ph_no)
    #print("Working")

            #submit = Person.objects.order_by('-id')[0]
            #print(str(form))
    #return HttpResponse("The task is done")


