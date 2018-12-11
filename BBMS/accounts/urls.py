from django.urls import path,include
from . import views

app_name = 'accounts'

urlpatterns = [
	path(r'register/', views.register, name='register'),
	path(r'confirm_register/', views.confirm_register, name='confirm_register'),
	path(r'login/', views.login, name='login'),
	path(r'aflogin/', views.aflogin, name='aflogin'),
	path(r'logout/', views.logout, name='aflogin'),
	path(r'forgot_password/', views.fpassinit, name='fpassinit'),
	path(r'forgot_password/verify/', views.fpassotp, name='fpassotp'),
	path(r'forgot_password/verify/change_pass/', views.chpass, name='chpass'),
	path(r'profile/', views.profile, name='profile'),
	path(r'profile/upprofile/', views.uppurofile, name='profile'),
	path(r'profile/upsett/', views.upsett, name='profile'),
#	path(r'microsoft/', include('microsoft_auth.urls', namespace='microsoft')),
#	path(r'profile/', views.login, name='aflogin'),
#	path(r'login_result/', views.login_user, name='login'),
]