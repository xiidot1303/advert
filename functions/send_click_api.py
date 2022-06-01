import requests
import json
import calendar
import time
import hmac
import hashlib
import base64
from config import *



### CLICK



# gmt stores current gmtime
gmt = time.gmtime()  
# ts stores timestamp
ts = calendar.timegm(gmt)

text = str(ts) + CLICK_SECRET_KEY
hash_object = hashlib.sha1(bytes(text, 'utf8'))
digest = hash_object.hexdigest()

headers = {'Accept': 'application/json', 'Auth': '{}:{}:{}'.format(CLICK_MERCHANT_USER_ID, digest, str(ts)), 'Content-Type': 'application/json'}

def create_invoice(amount, phone, trans_id):
    # create invoice
    url = "https://api.click.uz/v2/merchant/invoice/create"
    data = {
        "service_id": CLICK_SERVICE_ID,
        "amount": amount,
        "phone_number": phone,
        "merchant_trans_id": trans_id,
    }
    try:
        r = requests.post(url=url, data=json.dumps(data), headers=headers, timeout=3)
        content = json.loads(r.content.decode())
        
        return content['invoice_id']
    except requests.Timeout:
        return 'timeout'
    except:
        return 'error'
