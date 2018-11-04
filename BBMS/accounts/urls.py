from django.urls import path,include
from . import views

urlpatterns = [
	path(r'register/', views.register, name='register'),
	path(r'confirm_register/', views.confirm_register, name='confirm_register'),
	path(r'login/', views.login, name='login'),
#	path(r'^oauth/', include('social_django.urls', namespace='social')),
	path(r'aflogin/', views.login, name='aflogin'),
	path(r'logout/', views.logout, name='aflogin'),
#	path(r'profile/', views.login, name='aflogin'),
#	path(r'login_result/', views.login_user, name='login'),
#	path(r'^oauth/', include('social_django.urls', namespace='social')),
]
