from django.shortcuts import render

def donor(request):
    return render(request,'donor.html')


def login(request):
    return render(request, 'login.html')
