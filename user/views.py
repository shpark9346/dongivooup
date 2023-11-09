import os, json
from django.conf import settings
import requests
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout  
from . import forms
from . import models
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.naver import views as naver_view
from rest_framework import status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from rest_framework import status
from json.decoder import JSONDecodeError
from django.conf import settings
from setting.models import Point

# Create your views here.
#def login(request):
#    return render(request, 'login.html')

def join(request):
    return render(request, 'join.html')

def profile(request):
    return render(request, 'profile.html')

class LoginView(FormView):
    template_name = "login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("main:main")
    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form) 

def log_out(request):
    logout(request) 
    return redirect(reverse("main:main"))

class SignUpView(FormView): 
    template_name = "signup.html" 
    form_class = forms.SignUpForm 
    success_url = reverse_lazy("main:main")
    initial = {
        "email": "dongivooup@test.com",
        "name": "돈기부",
        "nickname": "tes",
        "phone": "01012345679",
    }
    
    def form_valid(self, form): 
        form.save() 
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        print(email, password)
        user = authenticate(self.request, email=email, password=password)
        Point.objects.create(user=user, balance=0, deduction=0)
        if user is not None:
            login(self.request, user)
        #name = self.cleaned_data.get("name")
        #nickname = self.cleaned_data.get("nickname")
        #phone = self.cleaned_data.get("phone")
        return super().form_valid(form) 

#카카오 로그인
BASE_URL = 'http://127.0.0.1:8000/'
KAKAO_CALLBACK_URI = BASE_URL + 'user/kakao/callback/'
GOOGLE_CALLBACK_URI = BASE_URL + 'user/google/callback/'
NAVER_CALLBACK_URI = BASE_URL + 'user/naver/callback/'

state = getattr(settings, 'STATE')

def kakao_login(request):
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    return redirect(
    f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )
   
    

class KakaoException(Exception): # 에러처리를 위해 class 생성
    pass

def kakao_callback(request):
    #try:
    code = request.GET.get("code") # 👈 임시 코드를 받아옵니다.
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    redirect_uri = KAKAO_CALLBACK_URI
    """
    Access Token Request
    """
    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}")
    #token_req = request.get(
    #    f"https://kauth.kakao.com/oauth/token?application/x-www-form-urlencoded&grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}"
    #)
    token_req_json = token_req.json()
    error = token_req_json.get("error", None)
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    """
    Email Request
    """
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_json = profile_request.json()
    print(profile_json)
    kakao_account = profile_json.get('kakao_account')
    """
    kakao_account에서 이메일 외에
    카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
    print(kakao_account) 참고
    """
    print(kakao_account)
    email = kakao_account.get('email')
    print(email)
    """
    Signup or Signin Request
    """
    try:
        user = models.User.objects.get(email=email)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect(reverse("main:main"))
    except models.User.DoesNotExist:
        return redirect(reverse("user:login"))

class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI

def google_login(request):
    """
    Code Request
    """
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


def google_callback(request):
    client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get('code')
    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get('access_token')
    """
    Email Request
    """
    email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    email_req_json = email_req.json()
    email = email_req_json.get('email')
    """
    Signup or Signin Request
    """
    try:
        user = models.User.objects.get(email=email)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect(reverse("main:main"))
    except models.User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        return redirect(reverse("user:signup"))

class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client


#naver login
import urllib.parse
def naver_login(request):
    """
    Code Request
    """
    client_id = getattr(settings, "NAVER_CLIENT_ID")
    redirect_uri = urllib.parse.quote(NAVER_CALLBACK_URI)
    print(redirect_uri)
    state = "RANDOM_STATE"
    return redirect(f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state={state}")

def naver_callback(request):
    client_id = getattr(settings, "NAVER_CLIENT_ID")
    client_secret = getattr(settings, "NAVER_SECRET")
    code = request.GET.get('code')
    state = request.GET.get('state')
    redirect_uri = NAVER_CALLBACK_URI.encode()
    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&code={code}&state={state}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get('access_token')
    """
    User Request
    """
    user_info_request = requests.get(
        "https://openapi.naver.com/v1/nid/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if user_info_request.status_code != 200:
        return JsonResponse({"error": "failed to get email."}, status=status.HTTP_400_BAD_REQUEST)
    user_info = user_info_request.json().get("response")
    email = user_info["email"]
    """
    Signup or Signin Request
    """
    if email is None:
        return JsonResponse({
            "error": "Can't Get Email Information from Naver"
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = models.User.objects.get(email=email)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect(reverse("main:main"))
    except models.User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        return redirect(reverse("user:signup")) 


class NaverLogin(SocialLoginView):
    adapter_class = naver_view.NaverOAuth2Adapter
    callback_url = urllib.parse.quote(NAVER_CALLBACK_URI)
    client_class = OAuth2Client