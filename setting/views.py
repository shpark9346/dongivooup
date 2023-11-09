from django.shortcuts import render, redirect, get_object_or_404
from . models import Time_settings, Point
import json

# Create your views here.
def setting(request):
    point = get_object_or_404(Point, user=request.user.id)
    return render(request, 'setting.html', {'point': point})

def time_list(request):
    time_index = Time_settings.objects.filter(user=request.user.id)
    return render(request, 'time-list.html', {'time_index':time_index})

def time_set(request):
    if request.method == 'GET':
        return render(request, 'time-set.html')
    else:
        time = Time_settings()
        time.user = request.user
        time.hour = request.POST['hour']
        time.min = request.POST['min']
        time.ampm = request.POST['ampm']
        time.date = request.POST.getlist('date')
        if time.date == ['월','화','수','목','금','토','일']:
            time.date = '매일'
        elif time.date == ['월','화','수','목','금']:
            time.date = '평일'
        elif time.date == ['토','일']:
            time.date = '주말'
        else:
            time.date = ','.join(time.date)
        time.save()
        return redirect('setting:time-list')

def time_update(request, time_id):
    time = get_object_or_404(Time_settings, pk=time_id)
    print(time.id)
    if request.method == 'POST':
        time.hour = request.POST['hour']
        time.min = request.POST['min']
        time.ampm = request.POST['ampm']
        time.date = request.POST.getlist('date')

        if time.date == ['월','화','수','목','금','토','일']:
            time.date = '매일'
        elif time.date == ['월','화','수','목','금']:
            time.date = '평일'
        elif time.date == ['토','일']:
            time.date = '주말'
        else:
            time.date = ','.join(time.date)

        time.save()
        print(time.id)
        return redirect('setting:time-list')

    else:
        return render(request, 'time-update.html', {'time':time})
