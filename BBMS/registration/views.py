from django.shortcuts import render
from django.http import HttpResponse

from registration.models import Register
# Create your views here.

def index(request):
    return HttpResponse("Bingo!")
