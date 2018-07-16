FROM bde2020/spark-submit:2.3.0-hadoop2.7

WORKDIR /app
COPY requirements.txt /app/
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY .  /app
