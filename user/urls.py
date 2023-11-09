from django.urls import path, include
from user import views
from django.contrib.auth import views as auth_views
app_name = 'user'

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path('logout/', views.log_out, name='logout'),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('profile/', views.profile, name='profile'),
    #path("accounts/kakao/login/", views.kakao_login, name="kakao_login"),
    #path("accounts/kakao/login/callback/", views.kakao_callback, name="kakao_callback"),

    #path("verify/<str:key>", views.complete_verification, name="complete-verification"),
    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
    path('kakao/login/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),

    path('google/login', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),  
    path('google/login/finish/', views.GoogleLogin.as_view(), name='google_login_todjango'),

    path('naver/login', views.naver_login, name='naver_login'),
    path('naver/callback/', views.naver_callback, name='naver_callback'),  
    path('naver/login/finish/', views.NaverLogin.as_view(), name='naver_login_todjango'),
]