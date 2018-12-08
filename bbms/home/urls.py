from django.urls import path,include
from . import views

app_name = 'home' 
urlpatterns = [
	path(r'', views.index, name='index'),
	path(r'transaction_page/', views.toportal, name='index'),
]