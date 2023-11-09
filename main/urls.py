from django.urls import path
from . import views

app_name= 'main'

urlpatterns = [
    path('', views.info, name='info'),
    path('main/', views.main, name='main'),
]