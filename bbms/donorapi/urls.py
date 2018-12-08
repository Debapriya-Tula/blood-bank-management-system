from django.urls import path,include
from . import views

app_name = 'donorapi'

urlpatterns = [
	path(r'', views.register, name='register'),
]