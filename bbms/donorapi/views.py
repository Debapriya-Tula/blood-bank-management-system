from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response 
from .serializers import Equationlogserializer, Userlogserializer


# Create your views here.

def result(request):
    print("working")
    fullname = request.POST['fullname']
    email= request.POST['email']
    ulog=userlog.objects.create(fullname=fullname,email=email)
    mass=request.POST['mass']
    acceleration=request.POST['acceleration']
    force= float(mass) * float(acceleration)
    elog=equationlog.objects.create(mass=mass,acceleration=acceleration,force=force,userlogid=ulog)
    return HttpResponse("In result page the force is {}".format(force))

#@api_view()
#def eqloglist(request):
#    eqlogs = equationlog.objects.all()
#    serializer = Equationlogserializer(eqlogs, many = True)
#    return Response(serializer.data)

class Equationloglistview(APIView):
    def get(self,request):
        eqlogs = equationlog.objects.all()
        serializer = Equationlogserializer(eqlogs, many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = Equationlogserializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)