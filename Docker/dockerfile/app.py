def handler(event, context):
    #HTTP API経由で値を返すだけ(JSON形式でないと×)
    return {
        'isBase64Encoded':False,
        'statusCode': 200,
        'headers': {},
        'body': "Invoking Lambda Function with Docker image is successful."
    }