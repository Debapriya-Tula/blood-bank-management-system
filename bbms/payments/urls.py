from django.urls import path
from django.conf.urls import url
from .views import *
from . import views

urlpatterns = [
	path('', views.home, name='pay'),
	path('buy_blood/',views.bblood, name='bblood'),
	path('bd_patient/',views.buy_blood, name='buyblood'),
	path('bd_donor/',views.donate_blood, name='donate'),
	path('bd_hospital/',views.hospital_blood, name='hospital'),
	path('finalize/',views.final, name='final'),
	path('checkout/',views.checkout, name='checkout'),
	path('updatetran/',views.update_transaction, name='update'),
	path('auth/',views.authenticate, name='authentication'),
	path('processed/',views.processed, name='processed'),

]