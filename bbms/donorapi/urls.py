from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path(r'donorlist/', views.Donor_detailslist.as_view(), name='donorlist'),
    path(r'api_token_auth/', obtain_auth_token, name='api_token_auth'),
    path(r'get_api/', views.getapi, name='api_token_auth'),
    path(r'api_register/', views.api_register, name='api_register'),
    path(r'try/', views.getjs)
]