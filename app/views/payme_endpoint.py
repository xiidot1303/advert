from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from jsonrpcserver import method, Result, Success, dispatch


@csrf_exempt
def payme_endpoint(request):    
    file = open('endpoint_response', 'wb')
    file.write('get')
    file.close()
    return HttpResponse(
        dispatch(request.body.decode()), content_type="application/json"
    )