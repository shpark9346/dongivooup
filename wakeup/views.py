from django.shortcuts import render
from setting.models import Time_settings
from datetime import datetime
# Create your views here.

def timer(request):
    time_list = Time_settings.objects.filter(user=request.user, onoff=True)

    if not time_list:
        return render(request, 'main.html')

    else:
        days = ['월', '화', '수', '목', '금', '토', '일']
        for time in time_list:
            date_target = time.date

            if date_target == '주말':
                date_target = '토, 일'
            elif date_target == '평일':
                date_target = '월, 화, 수, 목, 금'
            elif date_target == '매일':
                date_target = '월, 화, 수, 목, 금, 토, 일'

            hour_target = int(time.hour)
            min_target = int(time.min)

            time_now = datetime.time(datetime.now())
            date_now = days[datetime.today().weekday()]
            hour_now = time_now.hour
            min_now = time_now.minute

            if time.ampm == 'pm':
                hour_target += 12

            if date_now in date_target:
                before = 10
                after = 10

                if min_target < before:
                    if hour_target == 0:
                        hour_target_before = 23
                    else:
                        hour_target_before = hour_target - 1
                    min_target_before = 60 + min_target - before
                else:
                    hour_target_before = hour_target
                    min_target_before = min_target - before

                
                if 60 < min_target + after:
                    if hour_target == 23:
                        hour_target_after = 0
                    else:
                        hour_target_after = hour_target + 1
                    min_target_after = min_target + after - 60
                else:
                    hour_target_after = hour_target
                    min_target_after = min_target + after

                time_before = 60*hour_target_before + min_target_before
                time_after = 60*hour_target_after + min_target_after
                time_now = 60*hour_now + min_now

                if hour_target_before == 23:
                    if hour_now == 0:
                        time_now += 60*24
                    if hour_target_after == 0:
                        time_after += 60*24

                if time_before <= time_now <= time_after:
                    return render(request, 'timer.html')

        return render(request, 'notyet.html')

    

def confirm(request):
    return render(request, 'confirm.html')

def success(request):
    return render(request, 'success.html')

