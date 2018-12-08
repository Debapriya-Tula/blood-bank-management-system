from django.urls import path
from . import views

app_name="patient_portal"
urlpatterns = [

    path('patient/', views.patient, name='patient'),
    path('nearest/',views.nearest,name="nearest"),
    ]

#<input type="checkbox" name="suffered" value="6"  tabindex="32">
