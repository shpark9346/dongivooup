from dataclasses import fields
from unicodedata import name
from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from . import models

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))

    class Meta:
        model = models.User
        fields = ("email", "password")

class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ( 
            "email",
            "password",
            "name",
            "nickname",
            "phone",
        )
     
    password = forms.CharField()
    password1 = forms.CharField()
    
    def clean_password1(self):
        print(self)
        print(self.cleaned_data)
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            print(password, password1)
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password
    def save(self, *args, **kwargs): # save 매서드 가로채기
        user = super().save(commit=False) # Object는 생성하지만, 저장 x
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password1")
        user.email = email
        user.set_password(password) # set_password는 비밀번호를 해쉬값으로 변환
        user.save() 

    
        
    


  
       

