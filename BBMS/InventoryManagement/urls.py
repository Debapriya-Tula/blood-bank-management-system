from django.urls import path
from django.conf.urls import url
from .views import *
from . import views

urlpatterns = [
	path('', views.display_RBCL, name='inv-RBC'),
	path('plasma/', views.display_Plasma, name='inv-Plasma'),
	path('platelet/', views.display_Platelets, name='inv-Platelet'),
	path('addstock/', views.add_stock, name='inv-add'),
	path('deletestock/', views.delete_stock, name='inv-delete'),
	path('unit_account/', views.display_unitexpiration, name='inv-unit'),
]