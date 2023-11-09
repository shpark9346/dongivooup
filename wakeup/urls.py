from django.urls import path
from . import views

app_name= 'wakeup'

urlpatterns = [
    path('confirm/', views.confirm, name='confirm'),
    path('success/', views.success, name='success'),
    path('timer/', views.timer, name='timer'),
]