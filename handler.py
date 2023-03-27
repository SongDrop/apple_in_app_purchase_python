import boto3
import os
import logging
import json
import storekit_history 

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ISSUER_ID = os.environ['ISSUER_ID']
KEY_ID = os.environ['KEY_ID']
PRIVATE_KEY_PATH = os.environ['PRIVATE_KEY_PATH']
original_transaction_id = os.environ['original_transaction_id']

 
#WARNING! PROTECT EXECUTE AGAINST SQL INJECTION
def lambda_handler(event, context):
    context.callbackWaitsForEmptyEventLoop = False
    logging.info('RECEIVE_APPLE_IAP_EVENT',event)
    #queryStringParameters
    #original_transaction_id = event['queryStringParameters']['original_transaction_id']
 
    #
    try:
        iap_receipt = storekit_history.get_receipt(ISSUER_ID, KEY_ID, PRIVATE_KEY_PATH, original_transaction_id)
        print("iap_receipt",iap_receipt)
 
        
        #✅SUCCESS
        result = {
            "message": "In App Purchase Receipt",
            "receipt": iap_receipt
        }
        
        return success(result)

    except Exception as err:
        #🚫RECEIPT_ERROR
        print("RECEIPT_ERROR", f"{err}")
        return log_err(f"{err}")

      
#ERROR_MESSAGE
def log_err(errmsg):
    logger.error(json.dumps(errmsg))
    return {"body": json.dumps({"error": errmsg}), "headers": {'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin':'*'}, "statusCode": 400,
            "isBase64Encoded": "false"}
            
#SUCCESS_MESSAGE
def success(result):
    return {'body': json.dumps({"result": result}), 'headers': {'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin':'*'}, 'statusCode': 200,
            'isBase64Encoded': 'false'}


# {
#   "status": 0,
#   "environment": "Sandbox",
#   "receipt": {
#     "receipt_type": "ProductionSandbox",
#     "adam_id": 0,
#     "app_item_id": 0,
#     "bundle_id": "your_product_id",
#     "application_version": "58",
#     "download_id": 0,
#     "version_external_identifier": 0,
#     "receipt_creation_date": "2022-08-21 01:54:26 ENG/GMT",
#     "receipt_creation_date_ms": "1466128466000",
#     "receipt_creation_date_pst": "2022-08-21 01:54:26 ENG/GMT",
#     "request_date": "2022-08-21 01:54:26 ENG/GMT",
#     "request_date_ms": "1466184881174",
#     "request_date_pst": "2022-08-21 01:54:26 ENG/GMT",
#     "original_purchase_date": "2022-08-21 01:54:26 ENG/GMT",
#     "original_purchase_date_ms": "1375340400000",
#     "original_purchase_date_pst": "2022-08-21 01:54:26 ENG/GMT",
#     "original_application_version": "1.0",
#     "in_app": [
#       {
#         "quantity": "1",
#         "product_id": "product_id",
#         "transaction_id": "1000000218147651",
#         "original_transaction_id": "1000000218147500",
#         "purchase_date": "2022-08-21 01:54:26 ENG/GMT",
#         "purchase_date_ms": "1466127148000",
#         "purchase_date_pst": "2022-08-21 01:54:26 ENG/GMT",
#         "original_purchase_date": "2022-08-21 01:54:26 ENG/GMT",
#         "original_purchase_date_ms": "1466127033000",
#         "original_purchase_date_pst": "2022-08-21 01:54:26 ENG/GMT",
#         "expires_date": "2016-06-17 01:37:28 Etc/GMT",
#         "expires_date_ms": "1466127448000",
#         "expires_date_pst": "2022-08-21 01:54:26 ENG/GMT",
#         "web_order_line_item_id": "1000000032727764",
#         "is_trial_period": "false"
#       }
#     ]
#   },
# }