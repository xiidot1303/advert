import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse


@csrf_exempt
def prepare(request):
    data = request.body.decode()
    click_trans_id = data['click_trans_id']
    merchant_trans_id = data['merchant_trans_id']

    response = {'click_trans_id': click_trans_id, 'merchant_trans_id': merchant_trans_id, 'merchant_prepare_id': 103, 
        'error': 0, 'error_note': ''}
    return JsonResponse(response)


@csrf_exempt
def complate(request):
    data = request.body.decode()
    click_trans_id = data['click_trans_id']
    merchant_trans_id = data['merchant_trans_id']

    response = {'click_trans_id': click_trans_id, 'merchant_trans_id': merchant_trans_id, 'merchant_confirm_id': 104, 
        'error': 0, 'error_note': ''}
    return JsonResponse(response)


