from django.urls import path
from . import views

app_name = "donor_portal"
urlpatterns = [
    path('donor/', views.donor, name='donor'),
]
