# lambda_function.py
import json
from my_pulp_script import hiryou_pulp

def lambda_handler(event, context):
    body = json.loads(event['body'])

    result = hiryou_pulp(
        c_yasai=body["c_yasai"],
        c_hiryou=body["c_hiryou"],
        custom_yasai=body["custom_yasai"],
        custom_hiryou=body["custom_hiryou"]
    )

    return {
        'statusCode': 200,
        'body': result,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
