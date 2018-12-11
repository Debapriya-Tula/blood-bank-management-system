from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from accounts.models import Donor_reg, Donor_details
from django.contrib import messages
from accounts.models import veremail
from accounts.views import confirm_register, dropindb, sendmail, em_verify
from random import randint as rand
# Create your views here.


def home(request):
    return render(request, 'home.html')

def donor(request):
    saved = False
    if request.method == 'POST':
        if request.session.has_key('sess_id_donor'):
            un = str(request.session['sess_id_donor']).split('_')[2]
            user = Donor_reg.objects.get(username = un)
            print('working')
            if user.email_verified:            
                form = Donor_Form(request.POST)
                form1 = Disease_form(request.POST)
                if form.is_valid() and form1.is_valid():
                    don_or_sell = form.cleaned_data['don_or_sell']
                    last_donate_date = form.cleaned_data['last_donate_date']
                    no1w=timezone.now()
                    diff=no1w-last_donate_date
                    if(int(diff.total_seconds())<4838400):
                        reason=" You have not crossed the optimum time period that one has to wait before full blood donation. We request you to try again after you have done so."
                        context={'reason':reason}
                        return render(request, 'payments/cant_donate.html', context)
                    else:
                        ob=Donor_DataBase.objects.create(user_name=user, don_or_sell=don_or_sell, last_donate_date=last_donate_date)
                        Asthma, Cancer, Cardiac_Disease, Diabetes, Hypertension, Kidney_Disease, Epilepsy, HIV = form1.cleaned_data['Asthma'], form1.cleaned_data['Cancer'], form1.cleaned_data['Cardiac_Disease'], form1.cleaned_data['Diabetes'], form1.cleaned_data['Hypertension'], form1.cleaned_data['Kidney_Disease'], form1.cleaned_data['Epilepsy'], form1.cleaned_data['HIV']
                        ob1=Diseases(donor=ob,Asthma=Asthma, Cancer=Cancer, Cardiac_Disease=Cardiac_Disease, Diabetes=Diabetes, Hypertension=Hypertension, Kidney_Disease=Kidney_Disease, Epilepsy=Epilepsy, HIV=HIV)
                        if Cancer == 'Yes' or Diabetes=='Yes' or Kidney_Disease=='Yes' or HIV=='Yes':
                            reason="You have been diagnosed with diseases that are not suitable for donating blood"
                            context={'reason':reason}
                            ob.delete()
                            return render(request, 'payments/cant_donate.html', context)


                        messages.success(request, f'Your request has been processed. You will soon be notified via E-mail')
                        return redirect('processed')
            else:
                dropindb(veremail,un)
                code = rand(100000,999999)
                ef = veremail.objects.create(ab=int(code), uname=un)
                print(code)
                em_verify(user.email, code)
                context = {'uname':un, 'catg': 'donor'}
                print(context)
                return render(request,'confirm_register.html',context)

        else:
            return HttpResponseRedirect('/accounts/login')
    else:
        donor_form = Donor_Form()
        disease_form = Disease_form()
        context = {
            'form':donor_form,
            'form1':disease_form,
        }
        return render(request, 'donor.html', context)






