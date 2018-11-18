from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

from djtwilio import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'django1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', admin.site.urls),

    #Here we add our Twilio URLs
    url(r'^sms/$', views.sms),
    url(r'^ring/$', views.ring),
]


#phonenumbers
#Twilio
#messages
#django-patterns
