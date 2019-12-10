FROM python:3

WORKDIR /usr/src/countrys

COPY requirements.txt ./

RUN python3 -m pip install --user --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]