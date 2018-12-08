"""bbms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path(r'', include('home.urls')),
#	path(r'nbbanks', include('nearest_bbanks.urls')),
	path(r'admin/', admin.site.urls),
	path(r'accounts/', include('accounts.urls')),
	#path(r'csystem/', include('csystem.urls')),
#	path(r'api-auth/', include('rest_framework.urls')),
	path(r'inventory/', include('InventoryManagement.urls')),
	path(r'payments/', include('payments.urls')),
	path(r'hospital_portal/', include('hospital_portal.urls')),
	path(r'donor_portal/', include('donor_portal.urls')),
	path(r'patient_portal/', include('patient_portal.urls')),
	path(r'chat/', include('chat.urls')),
	path(r'oauth/', include('allauth.urls')),

]

'''if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)'''