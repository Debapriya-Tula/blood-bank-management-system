from django.urls import path
from . import views
app_name="hospital_portal"
urlpatterns = [
    path('hospital/', views.hospital, name='hospital'),
]
