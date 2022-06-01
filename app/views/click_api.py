import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from app.models import *


@csrf_exempt
def prepare(request):
    data = request.body.decode()
    click_trans_id = data['click_trans_id']
    merchant_trans_id = int(data['merchant_trans_id'])
    amount = data['amount']

    response = {'click_trans_id': click_trans_id, 'merchant_trans_id': merchant_trans_id, 'merchant_prepare_id': 103, 
        'error': 0, 'error_note': ''}
    if data['error'] == 0:
        try:
            st_obj = Statement.objects.get(pk=merchant_trans_id)
        except:
            response['error'] = -5
            response['error_note'] = 'User does not exist'
            return  JsonResponse(response)
        
        


    return JsonResponse(response)


@csrf_exempt
def complate(request):
    data = request.body.decode()
    click_trans_id = data['click_trans_id']
    merchant_trans_id = data['merchant_trans_id']

    response = {'click_trans_id': click_trans_id, 'merchant_trans_id': merchant_trans_id, 'merchant_confirm_id': 103, 
        'error': 0, 'error_note': ''}
    return JsonResponse(response)


