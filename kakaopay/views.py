from django.shortcuts import render, redirect, get_object_or_404
import requests
from setting.models import Point

# Create your views here.


def kakaoPay(request):
    point = get_object_or_404(Point, user=request.user.id)
    return render(request, 'charge.html',{'point':point})

def kakaoPayLogic(request):
    _admin_key = '3f8b880b8db630416875075a37e81ccb' # 입력필요
    _url = f'https://kapi.kakao.com/v1/payment/ready'
    _headers = {
        'Authorization': f'KakaoAK {_admin_key}',
    }
    _data = {
        'cid': 'TC0ONETIME',
        'partner_order_id':'partner_order_id',
        'partner_user_id':'partner_user_id',
        'item_name':'10000 포인트 충전',
        'quantity':'1',
        'total_amount':'10000',
        'vat_amount':'0',
        'tax_free_amount':'0',
        # 내 애플리케이션 -> 앱설정 / 플랫폼 - WEB 사이트 도메인에 등록된 정보만 가능합니다
        # * 등록 : http://IP:8000 
        'approval_url':'http://127.0.0.1:8000/pay/paySuccess', 
        'fail_url':'http://127.0.0.1:8000/pay/payFail',
        'cancel_url':'http://127.0.0.1:8000/pay/payCancel'
    }
    _res = requests.post('https://kapi.kakao.com/v1/payment/ready', data=_data, headers=_headers)
    _result = _res.json()
    request.session['tid'] = _result['tid']
    return redirect(_result['next_redirect_pc_url'])

def paySuccess(request):
    _url = 'https://kapi.kakao.com/v1/payment/approve'
    _admin_key = '3f8b880b8db630416875075a37e81ccb' # 입력필요
    _headers = {
        'Authorization': f'KakaoAK {_admin_key}'
    }
    _data = {
        'cid':'TC0ONETIME',
        'tid': request.session['tid'],
        'partner_order_id':'partner_order_id',
        'partner_user_id':'partner_user_id',
        'pg_token': request.GET['pg_token']
    }
    _res = requests.post(_url, data=_data, headers=_headers)
    _result = _res.json()
    if _result.get('msg'):
        return redirect('/pay/payFail')
    else:
        # return render(request, 'charge-success.html')
        return redirect('kakao:payCharge')
    
def payCharge(request):
    point = get_object_or_404(Point, user=request.user.id)
    point.balance += 10000
    point.save()
    return render(request,'charge-success.html')



def payFail(request):
    return render(request, 'charge-failure.html')

def payCancel(request):
    return render(request, 'charge-cancel.html')