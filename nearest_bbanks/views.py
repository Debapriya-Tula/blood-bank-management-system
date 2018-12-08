from django.shortcuts import render
from django.http import HttpResponse
from ipware import get_client_ip

def index(request):
	ip, is_routable = get_client_ip(request)
	if ip is None:
		print("Unable to get the client's IP address'")
	else:
		print("We got the client's IP address. It is",ip)
		if is_routable:
			print("The client's IP address is publicly routable on the Internet")
		else:
			print("The client's IP address is private")
	return HttpResponse("Hello")