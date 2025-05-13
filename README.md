# 最適化計算API

このリポジトリは、野菜の最適な肥料配合を計算するAWS Lambda関数のソースコードを含んでいます。

## 目的

- 野菜の種類と肥料の種類を指定して、最適な肥料配合を計算
- AWS Lambda上で実行されるAPIエンドポイントとして機能
- スマートフォンアプリからのリクエストに対応

## デプロイパッケージの作成方法

1. Dockerイメージのビルドとzipファイルの作成:
```bash
docker build -t lambda-package . && docker create --name temp-container lambda-package && docker cp temp-container:/app/function.zip . && docker rm temp-container
```

2. 作成された`function.zip`をAWS Lambdaにアップロード

## APIの使用方法

### リクエスト例

```bash
curl -X POST \
  'https://your-api-gateway-url/your-stage/your-resource' \
  -H 'Content-Type: application/json' \
  -d '{
    "c_yasai": ["トマト", "ナス"],
    "c_hiryou": ["窒素", "リン酸", "カリ"],
    "custom_yasai": {
      "トマト": {
        "窒素": 2.5,
        "リン酸": 1.8,
        "カリ": 3.0
      },
      "ナス": {
        "窒素": 2.0,
        "リン酸": 1.5,
        "カリ": 2.5
      }
    },
    "custom_hiryou": {
      "窒素": 1.0,
      "リン酸": 1.0,
      "カリ": 1.0
    }
  }'
```

### リクエストパラメータ

- `c_yasai`: 計算対象の野菜のリスト
- `c_hiryou`: 計算対象の肥料のリスト
- `custom_yasai`: 野菜ごとの肥料必要量（kg/10a）
- `custom_hiryou`: 肥料ごとの単価（円/kg）

### レスポンス例

```json
{
  "statusCode": 200,
  "result": {
    "最適解": {
      "トマト": {
        "窒素": 2.5,
        "リン酸": 1.8,
        "カリ": 3.0
      },
      "ナス": {
        "窒素": 2.0,
        "リン酸": 1.5,
        "カリ": 2.5
      }
    },
    "総コスト": 1234.56
  },
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  }
}
```

## 環境要件

- Python 3.10
- 必要なパッケージ:
  - numpy==1.24.3
  - pandas==1.5.3
  - pulp==2.7.0
