FROM python:3.8.3-slim

WORKDIR /usr/src/lol

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY  lol.py .

CMD [ "python", "lol.py" ]
