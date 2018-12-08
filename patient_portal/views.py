from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import *
from .forms import *

# Create your views here.


def home(request):
    return render(request, 'home.html')


def patient(request):
    saved = False
    if request.method == 'POST':
        profile_form = Profile_Form(request.POST, request.FILES)
        print(profile_form)
        if profile_form.is_valid():
            profile_model = DataBase()
            profile_model.picture = profile_form.cleaned_data["picture"]
            profile_model.pic_name = profile_form.cleaned_data['pic_name']
            profile_model.save()
            saved = True
            return render(request, 'home.html')
    else:
        profile_form = Profile_Form()
    return render(request, 'patient.html', {'form': profile_form})

def nearest(request):
    return render(request, 'nearestbloodbanks.html', {})