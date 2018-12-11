from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('patient/', views.patient, name='patient'),
]


#<input type="checkbox" name="suffered" value="6"  tabindex="32">

