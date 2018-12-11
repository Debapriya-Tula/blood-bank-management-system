from django.urls import path
from django.conf.urls import url
from .views import *
from . import views

urlpatterns = [
	path('', views.home, name='pay'),
	path('finalize/',views.final_patient, name='final'),
	path('finalize_hospitals/',views.final_hospital, name='final_hospital'),
	path('checkout/',views.checkout1, name='checkout'),
	path('updatetran/',views.checkout, name='update'),
	path('listorders/', views.listOrders, name='list'),
	path('listdoners', views.donorList, name='list_doner'),
	path('auth/order<int:num>/',views.authenticate, name='authentication'),
	path('auth/donation<int:num>/',views.authdonor, name='authentication_donor'),
	path('processed/',views.processed, name='processed'),
	#path('delete_order_patient/order<int:num>',views.delete_order_patient,name='delete_order_patient'),
	#path('delete_order_hospital/order<int:num>',views.delete_order_hospital,name='delete_order_hospital'),
	path('processed_hospital/',views.processedhospital, name='processed_hospital'),
	path('cant_donate/',views.cantdonate, name='cant_donate'),

]