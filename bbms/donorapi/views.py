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
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission

def api_register(request):
	if request.method == 'POST':
		p1 = Permission.objects.get(name='Can view donor_details')
		p2 = Permission.objects.get(name='Can view donor_reg')
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			user.user_permissions.add(p1)
			user.user_permissions.add(p2)
			return HttpResponseRedirect('/api/get_api')
	else:
		form = UserCreationForm()
		context = {'form': form}
		context['nbar'] = 'api'
	return render(request, 'api_register.html', context)


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

def getjs(request):
	url = 'http://127.0.0.1:8000/api/donorlist/'
	headers = {'Authorization': 'Token 50fbb8cd0534631d2a42698979e10482f5569ee6'}
	r = requests.get(url, headers=headers)
	json_data = json.loads(r.text)
	return HttpResponse(str(json_data))

def getapi(request):
	if request.method == 'GET':
		template = loader.get_template('get_api_token.html')
		context = {}
		context.update(csrf(request))
		context['nbar'] = 'api'
		return HttpResponse(template.render(context,request))