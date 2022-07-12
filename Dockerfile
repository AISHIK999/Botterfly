FROM python:alpine

RUN mkdir /templarub
WORKDIR /templarub

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
CMD ["python3","userbot"]
