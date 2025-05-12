import json
from lambda_function import lambda_handler

def main():
    # DetaやFastAPIではなく Lambda handler に直接渡す形式
    data = {
        'c_yasai': 'オリジナル野菜1',
        'c_hiryou': ['オリジナル肥料1','発酵鶏ふん','骨粉','化成肥料(8-8-8)','もみ殻'],
        'custom_yasai': {
            'yasai': ['オリジナル野菜1', 'オリジナル野菜2'],
            'N': [49, 48],
            'P': [70, 71],
            'K': [58, 58],
            'W': [2000, 2000]
        },
        'custom_hiryou': {
            'hiryou': ['オリジナル肥料1', 'オリジナル肥料2'],
            'Price': [0.084740741, 0.084740741],
            'N': [0.018, 0.02],
            'P': [0.025, 0.067],
            'K': [0.024, 0.045]
        }
    }

    # Lambda handler用のevent構造
    event = {
        'body': json.dumps(data)
    }

    # Lambda handler 呼び出し
    response = lambda_handler(event, None)
    print("Status Code:", response["statusCode"])
    print("Result:")
    print(json.dumps(json.loads(response["body"]), ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
