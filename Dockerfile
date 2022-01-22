FROM python:3.7-buster
ENV PYTHONUNBUFFERED=1
ENV export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

RUN apt-get update -y \
    && apt-get install -y libgomp1 \
    && apt-get -y clean all

RUN rm -f /usr/bin/python \
    && ln -s /usr/local/bin/python3 /usr/bin/python

RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
    && tar -xzf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib/ \
    && ./configure --prefix=/usr \
    && make \
    && make install


# [ローカル環境で実行する場合]
# サービスアカウントのjsonファイルをコピーしてパスを指定する
# COPY source_key_path destination_key_path
# ENV GOOGLE_APPLICATION_CREDENTIALS=''
# 最後にconfig/w2v.ymlのproject/is_localをtrueに変更する

COPY poetry.lock pyproject.toml ./

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry env use 3.7

RUN poetry config virtualenvs.create false \
    && poetry config virtualenvs.in-project true \
    && poetry install

COPY . ./

ENTRYPOINT ["poetry", "run", "uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
