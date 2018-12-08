from django.urls import path
from . import views

urlpatterns = [
    path('nearest/', views.nearest, name='nearest'),
    path('patient/', views.patient, name='patient'),
]


#<input type="checkbox" name="suffered" value="6"  tabindex="32">

