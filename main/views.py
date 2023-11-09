from django.shortcuts import render, redirect
from setting.models import Time_settings


# Create your views here.
def info(request):
    return render(request, 'info.html')

def main(request):
    return render(request, 'main.html')


# Time_settings 객체를 count하고, 객체가 존재하면 timer.html 페이지를 렌더링
# def main(request):
#     time_count = Time_settings.objects.all()
#     count = time_count.count()
#     if count == 0:
#         return render(request, 'main.html')
#     else:
#         return render(request, 'timer.html')

