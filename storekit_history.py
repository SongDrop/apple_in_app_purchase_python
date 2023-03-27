import requests, time, json
import jwt


def generate_token(ISSUER_ID, KEY_ID,PRIVATE_KEY):
    EXPIRATION_TIME = int(round(time.time() + (10.0 * 60.0))) # 10 minutes timestamp
    payload = {
        "iss": ISSUER_ID,
        "exp": EXPIRATION_TIME,
        "aud": "appstoreconnect-v1"
    }
    headers = {
        "alg": "ES256",
        "kid": KEY_ID,
        "typ": "JWT"
    }
    f = open(PRIVATE_KEY, "r")
    private_key = f.read()
    token = jwt.encode(payload=payload, key=private_key, algorithm="ES256", headers=headers)
    return token


def get_receipt(issuer_id, key_id, private_key_path, original_transaction_id):
    # decode the bytes and create the get request header

    # API Request
    JWT = 'Bearer ' + generate_token(issuer_id, key_id, private_key_path).decode('UTF-8')
    URL = f'https://api.appstoreconnect.apple.com/v1/receipts/{original_transaction_id}'
    HEAD = {'Authorization': JWT}

    # send the get request
    #response = requests.get(URL, params={'limit': 200}, headers=HEAD)
    response = requests.get(URL, headers=HEAD)
    print("STATUS_CODE",response.status_code)
    print("JSON_RESPONSE",response.json())

    if response.status_code == 200:
        responseBody = response.json()#json.loads(response.data)
        status = response.status_code
        if status == 0:
            return responseBody
        else:
            raise Exception(f"IAP_STATUS_ERROR_{response.status_code}")
    else:
        raise Exception(f"IAP_STATUS_ERROR_{response.status_code}")
