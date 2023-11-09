from django.urls import path
from . import views

app_name= 'kakao'

urlpatterns = [
    path('', views.kakaoPay, name='pay'),
    path('kakaoPayLogic/', views.kakaoPayLogic, name='logic'),
    path('paySuccess/', views.paySuccess, name='success'),
    path('payFail/', views.payFail, name='fail'),
    path('payCancel/', views.payCancel, name='cancel'),
    path('payCharge/', views.payCharge, name='payCharge'),
]