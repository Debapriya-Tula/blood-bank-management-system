from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from rest_framework import status
from accounts.models import Donor_reg, Donor_details
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import Donor_detailsSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import requests
from django.template.context_processors import csrf
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Donor_detailslist(APIView):

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self,request):
		Donor_detailss =Donor_details.objects.all()
		serializer = Donor_detailsSerializer(Donor_detailss,many=True)
		return Response(serializer.data)

"""@api_view()
class Donor_detailsListView(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self,request):
		Donor_detailss = Donor_details.objects.all()
		serializer = Donor_detailsSerializer(Donor_detailss,many=True)
		return Response(serializer.data)

	def post(self,request):
		serializer = Donor_detailsSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)"""

def getjs(request):
	url = 'http://192.168.137.1:8000/api/donorlist/'
	headers = {'Authorization': 'Token bb3b127a1bdab092f3bd2bf5ae6a6720312e5cc7'}
	r = requests.get(url, headers=headers)
	json_data = json.loads(r.text)
	return HttpResponse(str(json_data))

def getapi(request):
	if request.method == 'POST':
		return HttpResponseRedirect('/api/get_api/ ')
	else:
		template = loader.get_template('get_api_token.html')
		context = {}
		context.update(csrf(request))
		return HttpResponse(template.render(context,request))