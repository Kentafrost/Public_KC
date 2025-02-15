FROM public.ecr.aws/lambda/python:3.12

# LAMBDA_TASK_ROOTはLambdaの環境変数でapp.pyをLambda関数のパスに渡す
COPY app.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Lambda起動時に実行するメソッドを指定
CMD ["app.handler"]