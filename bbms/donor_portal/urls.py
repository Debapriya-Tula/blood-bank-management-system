from django.urls import path
from . import views

urlpatterns = [
    path('donor/', views.donor, name='donor'),
    path('login/', views.login, name='login'),
]
