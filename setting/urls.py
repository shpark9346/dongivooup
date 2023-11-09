from django.urls import path
from . import views

app_name= 'setting'

urlpatterns = [
    path('', views.setting, name='setting'),
    path('time-list/', views.time_list, name='time-list'),
    path('time-set/', views.time_set, name='time-set'),
    path('time-update/<str:time_id>/', views.time_update, name='time-update'),
]