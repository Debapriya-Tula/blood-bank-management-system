from django.urls import path,include
from . import views

app_name="home"

urlpatterns = [
	path(r'index/', views.index, name='index'),
]
