FROM public.ecr.aws/lambda/python:3.10

WORKDIR /app

# zipコマンドをインストール
RUN yum install -y zip

# x86_64アーキテクチャ用のパッケージをインストール
RUN pip install --platform manylinux2014_x86_64 --target . --implementation cp --python-version 3.10 --only-binary=:all: numpy==1.24.3 pandas==1.5.3 pulp==2.7.0

# Pythonファイルをコピー
COPY *.py .

# すべてのファイルをzipに含める
RUN zip -r function.zip .

CMD ["/bin/bash"]
